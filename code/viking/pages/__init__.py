import blanc_pages

default_app_config = 'viking.pages.apps.PagesConfig'


class StandardLayout(blanc_pages.BlancPageLayout):
    template_name = 'blanc_pages/standard.html'
    title = 'Standard'
    columns = {
        'Heading': {
            'width': 945,
            'image_width': 945,
        },
        'Main Content': {
            'width': 640,
            'image_width': 625,
        },
        'Side': {
            'width': 320,
            'image_width': 305,
        },
    }


class HomeLayout(blanc_pages.BlancPageLayout):
    template_name = 'blanc_pages/home.html'
    title = 'Home'
    columns = {
        'Heading': {
            'width': 945,
            'image_width': 945,
        },
        'Main Content': {
            'width': 465,
            'image_width': 465,
        },
        'Side': {
            'width': 465,
            'image_width': 465,
        },
        'Related 1': {
            'width': 305,
            'image_width': 305,
        },
        'Related 2': {
            'width': 305,
            'image_width': 305,
        },
        'Related 3': {
            'width': 305,
            'image_width': 305,
        },
    }


class AltPageLayout(blanc_pages.BlancPageLayout):
    template_name = 'blanc_pages/alt.html'
    title = 'Included Sidebar'
    columns = {
        'Heading': {
            'width': 945,
            'image_width': 945,
        },
        'Main Content': {
            'width': 625,
            'image_width': 625,
        },
        'Side': {
            'width': 284,
            'image_width': 284,
        },
    }


blanc_pages.register_template(HomeLayout)
blanc_pages.register_template(StandardLayout)
blanc_pages.register_template(AltPageLayout)
