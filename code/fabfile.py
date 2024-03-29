# -*- coding: utf-8 -*-

import random

from fabric.api import cd, env, execute, local, parallel, roles, run, runs_once, task
from fabric.contrib.files import exists

# Changable settings
env.roledefs = {
    'web': [
        'viking@scorch.blanctools.com',
        'viking@smaug.blanctools.com',
    ],
    'demo': [
        'viking@trogdor.blanctools.com',
    ],
    'cron': [
        'viking@smaug.blanctools.com',
    ],
}

env.home = env.get('home', '/var/www/viking')
env.repo = env.get('repo', 'viking')
env.media = env.get('media', 'viking')
env.database = env.get('database', 'viking_django')
env.database_ssh = env.get('database_ssh', 'golestandt.blanctools.com')

CRONTAB = """
MAILTO=""

{daily}         /usr/local/bin/django-cron python manage.py clearsessions
{twitter}       timeout 60 /usr/local/bin/django-cron python manage.py latest_tweets_update VikingRec
"""

# Avoid tweaking these
env.use_ssh_config = True
GIT_REMOTE = 'git@github.com:blancltd/{env.repo}.git'


@task
def demo():
    env.roledefs['web'] = env.roledefs['demo']
    env.roledefs['cron'] = env.roledefs['demo']
    env.database_ssh = 'trogdor.blanctools.com'


@task
@roles('cron')
def cron(remove=None):
    """
    Crontab setup.

    Can also be removed if needed.

    fab cron
    fab cron:remove=True
    """
    # Allow quick removal if needed
    if remove:
        run('crontab -r')
        return

    # Deterministic based on hostname
    random.seed(env.host_string)

    # Several templates - can add more if needed
    def every_x(minutes=60, hour='*', day='*', month='*', day_of_week='*'):
        # Add some randomness to minutes
        start = random.randint(0, minutes - 1)
        minute = ','.join(str(x) for x in range(start, 60, minutes))

        return '{minute} {hour} {day} {month} {day_of_week}'.format(
            minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week)

    cron = CRONTAB.format(
        daily=every_x(hour=random.randint(0, 23)),
        hourly=every_x(),
        twitter=every_x(minutes=15)
    )

    run("echo '{}' | crontab -".format(cron))


@task
@roles('web')
@parallel
def clone_repo(branch='master'):
    """
    Initial site setup.

    Only intended to be run once, but can be used to switch branch.

    fab clone_repo
    fab clone_repo:branchname
    """
    with cd(env.home):
        if not exists('.git'):
            git_repo = GIT_REMOTE.format(env=env)
            run('git clone --quiet --recursive {} .'.format(git_repo))
        else:
            run('git fetch')

        run('git checkout {}'.format(branch))


@task
@roles('web')
@parallel
def update():
    """ Pull latest git repository changes and install requirements. """
    with cd(env.home):
        run('git pull')

        run('pip install --quiet --requirement requirements/production.txt')

        # Clean up any potential cruft
        run('find . -name "*.pyc" -delete')


@task
@runs_once
@roles('web')
def migrate():
    """ Migrate database changes. """
    with cd(env.home):
        run('python manage.py migrate')


@task
@roles('web')
@parallel
def static():
    """ Update static files. """
    with cd(env.home):
        # Collect static files
        run('python manage.py collectstatic --verbosity=0 --noinput')


@task(name='reload')
@roles('web')
@parallel
def reload_uwsgi(force_reload=None):
    """
    Reload uWSGI.

    fab reload
    fab reload:True
    fab reload:force_reload=True
    """
    if force_reload:
        run('killall -TERM uwsgi')
    else:
        run('killall -HUP uwsgi')


@task
def deploy(force_reload=None):
    """
    Deploy to remote server.

    Steps includes pull repo, migrate, collect static, install requirements.

    fab deploy
    fab deploy:True
    fab deploy:force_reload=True
    """
    execute(update)
    execute(migrate)
    execute(static)
    execute(reload_uwsgi, force_reload=force_reload)


@task
def get_backup(hostname=None, replace_hostname='127.0.0.1', replace_port=8000):
    """
    Get remote backup and restore database locally.

    fab get_backup
    fab get_backup:www.example.com
    fab get_backup:www.example.com,192.1.1.1
    fab get_backup:hostname=www.example.com,replace_hostname=192.1.1.1,replace_port=8000
    """
    # Recreate database
    local('dropdb --if-exists {}'.format(env.database))
    local('createdb {}'.format(env.database))

    # Connect to the server and dump database.
    commands = ['ssh -C {} sudo -u postgres pg_dump --no-owner {}'.format(
        env.database_ssh, env.database
    )]

    if hostname:
        if replace_port:
            replace_host = '{}:{}'.format(replace_hostname, replace_port)
        else:
            replace_host = replace_hostname

        # If hostname is passed replace with replace_hostname.
        commands.append('sed -e "s|{}|{}|g"'.format(hostname, replace_host))

    # Restore database.
    commands.append('psql --single-transaction {}'.format(env.database))

    local(' | '.join(commands))


@task
def get_media(directory=''):
    """
    Download remote media files. It uses credentials from ~/.aws/config.

    fab get_media
    fab get_media:assets
    """
    # Sync files from our S3 bucket/directory
    local((
        'aws s3 sync '
        's3://contentfiles-media-eu-west-1/{media}/{directory} '
        'htdocs/media/{directory}').format(media=env.media, directory=directory))
