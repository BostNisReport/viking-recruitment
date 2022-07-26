#!/bin/bash
set -e -x

./manage.py dbshell << EOF
BEGIN;
UPDATE django_content_type SET app_label='viking_pages' WHERE app_label='pages';
UPDATE django_content_type SET app_label='pages' WHERE app_label='blanc_pages';
UPDATE django_content_type SET app_label='viking_auth' WHERE model IN ('vikinguser', 'bannedip');
UPDATE django_content_type SET app_label='viking_news' WHERE model='latestnewspostsblock';
UPDATE django_content_type SET app_label='viking_events' WHERE model='latesteventsblock';

DELETE FROM auth_permission WHERE content_type_id=(SELECT id FROM django_content_type WHERE app_label='pages' AND model='note');
DELETE FROM django_content_type WHERE app_label='pages' AND model='note';
COMMIT;

---

BEGIN;
DROP TABLE
    "south_migrationhistory"
    CASCADE;

ALTER TABLE "assets_imagecategory"
    ADD CONSTRAINT "assets_imagecategory_title_key" unique (title);
DROP INDEX "assets_imagecategory_title";
ALTER TABLE "assets_filecategory"
    ADD CONSTRAINT "assets_filecategory_title_key" unique (title);
DROP INDEX "assets_filecategory_title";

---

ALTER TABLE "auth_bannedip"
    RENAME TO "viking_auth_bannedip";
ALTER TABLE "auth_vikinguser"
    RENAME TO "viking_auth_vikinguser";
ALTER TABLE "auth_vikinguser_groups"
    RENAME TO "viking_auth_vikinguser_groups";
ALTER TABLE "auth_vikinguser_rejected_positions"
    RENAME TO "viking_auth_vikinguser_rejected_positions";
ALTER TABLE "auth_vikinguser_user_permissions"
    RENAME TO "viking_auth_vikinguser_user_permissions";

ALTER TABLE "auth_bannedip_id_seq"
    RENAME TO "viking_auth_bannedip_id_seq";
ALTER TABLE "auth_vikinguser_id_seq"
    RENAME TO "viking_auth_vikinguser_id_seq";
ALTER TABLE "auth_vikinguser_groups_id_seq"
    RENAME TO "viking_auth_vikinguser_groups_id_seq";
ALTER TABLE "auth_vikinguser_rejected_positions_id_seq"
    RENAME TO "viking_auth_vikinguser_rejected_positions_id_seq";
ALTER TABLE "auth_vikinguser_user_permissions_id_seq"
    RENAME TO "viking_auth_vikinguser_user_permissions_id_seq";

---

ALTER TABLE "pages_footerimage"
    RENAME TO "viking_pages_footerimage";
ALTER TABLE "pages_footerlink"
    RENAME TO "viking_pages_footerlink";
ALTER TABLE "pages_menuitem"
    RENAME TO "viking_pages_menuitem";
ALTER TABLE "pages_headerlink"
    RENAME TO "viking_pages_headerlink";
ALTER TABLE "pages_largebanner"
    RENAME TO "viking_pages_largebanner";
ALTER TABLE "pages_smallbanner"
    RENAME TO "viking_pages_smallbanner";

ALTER TABLE "pages_footerimage_id_seq"
    RENAME TO "viking_pages_footerimage_id_seq";
ALTER TABLE "pages_footerlink_id_seq"
    RENAME TO "viking_pages_footerlink_id_seq";
ALTER TABLE "pages_menuitem_id_seq"
    RENAME TO "viking_pages_menuitem_id_seq";
ALTER TABLE "pages_headerlink_id_seq"
    RENAME TO "viking_pages_headerlink_id_seq";
ALTER TABLE "pages_largebanner_id_seq"
    RENAME TO "viking_pages_largebanner_id_seq";
ALTER TABLE "pages_smallbanner_id_seq"
    RENAME TO "viking_pages_smallbanner_id_seq";

---

ALTER TABLE "events_latesteventsblock"
    RENAME TO "viking_events_latesteventsblock";
ALTER TABLE "news_latestnewspostsblock"
    RENAME TO "viking_news_latestnewspostsblock";


ALTER TABLE "events_latesteventsblock_id_seq"
    RENAME TO "viking_events_latesteventsblock_id_seq";
ALTER TABLE "news_latestnewspostsblock_id_seq"
    RENAME TO "viking_news_latestnewspostsblock_id_seq";

---

ALTER TABLE "news_post"
    ADD COLUMN "image_id" integer REFERENCES "assets_image" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "news_post_image_id"
    ON "news_post" ("image_id");

ALTER TABLE "news_post" ADD COLUMN "date_url" date;
COMMIT;

---

BEGIN;
UPDATE "news_post" SET date_url=date(date);

INSERT INTO "assets_imagecategory" (title)
    VALUES ('News');
INSERT INTO "assets_image" (category_id,title,file,image_height,image_width)
    SELECT (SELECT id FROM assets_imagecategory WHERE title='News'),title,image,image_height,image_width FROM news_post WHERE image != '';

UPDATE "news_post"
    SET image_id=subquery.assets_image_id
    FROM (SELECT news_post.id AS news_post_id,assets_image.id AS assets_image_id FROM news_post LEFT JOIN assets_image ON news_post.image=assets_image.file WHERE news_post.image != '') AS subquery
    WHERE news_post.id=subquery.news_post_id;
COMMIT;

---

BEGIN;
ALTER TABLE "news_post" ALTER COLUMN date_url SET not null;

CREATE INDEX "news_post_date_url"
    ON "news_post" ("date_url");
ALTER TABLE "news_post"
    DROP COLUMN "image",
    DROP COLUMN "image_height",
    DROP COLUMN "image_width";

CREATE INDEX "viking_pages_menuitem_url"
    ON "viking_pages_menuitem" ("url");
CREATE INDEX "viking_pages_menuitem_url_like"
    ON "viking_pages_menuitem" ("url" varchar_pattern_ops);

ALTER TABLE "jobs_jobnote" ALTER COLUMN "user_id" DROP NOT NULL;
COMMIT;

---

BEGIN;

DELETE FROM "profiles_marinecertification"
    WHERE "id" IN (SELECT profiles_marinecertification.id FROM "profiles_marinecertification" LEFT JOIN viking_auth_vikinguser ON viking_auth_vikinguser.id=profiles_marinecertification.user_id WHERE viking_auth_vikinguser.id IS NULL);

DELETE FROM "profiles_othercertification"
    WHERE "id" IN (SELECT profiles_othercertification.id FROM "profiles_othercertification" LEFT JOIN viking_auth_vikinguser ON viking_auth_vikinguser.id=profiles_othercertification.user_id WHERE viking_auth_vikinguser.id IS NULL);

DELETE FROM "profiles_languageproficiency"
    WHERE "id" IN (SELECT profiles_languageproficiency.id FROM "profiles_languageproficiency" LEFT JOIN viking_auth_vikinguser ON viking_auth_vikinguser.id=profiles_languageproficiency.user_id WHERE viking_auth_vikinguser.id IS NULL);

DELETE FROM "jobs_jobnote"
    WHERE "id" IN (SELECT jobs_jobnote.id FROM "jobs_jobnote" LEFT JOIN jobs_job ON jobs_job.id=jobs_jobnote.job_id WHERE jobs_job.id IS NULL);

UPDATE "jobs_jobnote"
    SET user_id=NULL WHERE "id" IN (SELECT jobs_jobnote.id FROM "jobs_jobnote" LEFT JOIN viking_auth_vikinguser ON viking_auth_vikinguser.id=jobs_jobnote.user_id WHERE viking_auth_vikinguser.id IS NULL);

DELETE FROM "profiles_previouswork"
    WHERE "id" IN (SELECT profiles_previouswork.id FROM "profiles_previouswork" LEFT JOIN viking_auth_vikinguser ON viking_auth_vikinguser.id=profiles_previouswork.user_id WHERE viking_auth_vikinguser.id IS NULL);

DELETE FROM "jobs_jobcandidate"
    WHERE "id" IN (SELECT jobs_jobcandidate.id FROM "jobs_jobcandidate" LEFT JOIN viking_auth_vikinguser ON viking_auth_vikinguser.id=jobs_jobcandidate.user_id WHERE viking_auth_vikinguser.id IS NULL);

DELETE FROM "jobs_jobcandidate"
    WHERE "id" IN (SELECT jobs_jobcandidate.id FROM "jobs_jobcandidate" LEFT JOIN jobs_job ON jobs_job.id=jobs_jobcandidate.job_id WHERE jobs_job.id IS NULL);

COMMIT;

EOF

./manage.py migrate --noinput --fake auth 0001
./manage.py migrate --noinput --fake viking_auth 0001
./manage.py migrate --noinput --fake jobs 0002
./manage.py migrate --noinput --fake profiles 0002
./manage.py migrate --noinput --fake easy_thumbnails 0002
./manage.py migrate --noinput

pg_dump --data-only --disable-triggers --exclude-table-data="django_migrations" --exclude-table-data="django_migrations_id_seq" viking_django > viking_django.dump

./manage.py dbshell << EOF
BEGIN;
DROP TABLE assets_file,
    assets_filecategory,
    assets_image,
    assets_imagecategory,
    auth_group,
    auth_group_permissions,
    auth_permission,
    blanc_pages_image_block_imageblock,
    blanc_pages_redactor_block_redactorblock,
    django_admin_log,
    django_content_type,
    django_migrations,
    django_redirect,
    django_session,
    django_site,
    downloads_category,
    downloads_file,
    easy_thumbnails_source,
    easy_thumbnails_thumbnail,
    easy_thumbnails_thumbnaildimensions,
    events_category,
    events_event,
    events_recurringevent,
    events_recurringeventexclusion,
    forms_cadetapplicationformblock,
    forms_contactformblock,
    forms_requestquoteformblock,
    homepage_banner,
    jobs_certificateofcompetency,
    jobs_classificationsociety,
    jobs_company,
    jobs_department,
    jobs_job,
    jobs_jobapplication,
    jobs_jobattachment,
    jobs_jobcandidate,
    jobs_jobnote,
    jobs_jobsector,
    jobs_location,
    jobs_marinecertificate,
    jobs_othercertificate,
    jobs_rank,
    jobs_rankgroup,
    jobs_trade,
    jobs_vessel,
    jobs_vesseltype,
    jobs_vikingmanagedcompany,
    latest_tweets_photo,
    latest_tweets_tweet,
    news_category,
    news_post,
    page_assets_largebannerblock,
    page_assets_latesttweetsblock,
    page_assets_relatedlink,
    page_assets_relatedlinklistblock,
    page_assets_smallbannerblock,
    pages_contentblock,
    pages_html,
    pages_page,
    pages_pageversion,
    profiles_advertreference,
    profiles_candidatemessage,
    profiles_candidatemessage_users,
    profiles_competencycertificate,
    profiles_country,
    profiles_curriculumvitae,
    profiles_document,
    profiles_language,
    profiles_languageproficiency,
    profiles_marinecertification,
    profiles_message,
    profiles_nationalitygroup,
    profiles_nationalitygroup_countries,
    profiles_newcandidate,
    profiles_newjob,
    profiles_othercertification,
    profiles_previouswork,
    profiles_recruitermessage,
    profiles_recruiternote,
    profiles_statusupdate,
    profiles_timelinelogentry,
    searches_searchpreference,
    team_contactblock,
    team_contactprofile,
    team_group,
    team_profile,
    viking_auth_bannedip,
    viking_auth_vikinguser,
    viking_auth_vikinguser_groups,
    viking_auth_vikinguser_rejected_positions,
    viking_auth_vikinguser_user_permissions,
    viking_events_latesteventsblock,
    viking_news_latestnewspostsblock,
    viking_pages_footerimage,
    viking_pages_footerlink,
    viking_pages_headerlink,
    viking_pages_largebanner,
    viking_pages_menuitem,
    viking_pages_smallbanner
    CASCADE;
COMMIT;
EOF

./manage.py migrate

./manage.py dbshell << EOF
BEGIN;
TRUNCATE auth_permission, django_content_type, django_site CASCADE;
COMMIT;
EOF

./manage.py dbshell < viking_django.dump
rm -f viking_django.dump
