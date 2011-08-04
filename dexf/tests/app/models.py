#
from django.utils.unittest.case import TestCase

__author__ = 'sax'

class OverrideSettingsTestCase(TestCase):
    #TODO: Maybe this class could be taken to a generic library.

    def setUp(self):
        if hasattr(self, 'settings_override'):
            for (key, value) in self.settings_override.items():
                if hasattr(settings, key):
                    setattr(self, '_old_%s' % key, getattr(settings, key)) # Back up the setting
                setattr(settings, key, value) # Override the setting

        # since django's r11862 templatags_modules and app_template_dirs are cached
        # the cache is not emptied between tests
        # clear out the cache of modules to load templatetags from so it gets refreshed
        template.templatetags_modules = []

        # clear out the cache of app_directories to load templates from so it gets refreshed
        app_directories.app_template_dirs = []
        # reload the module to refresh the cache
        reload(app_directories)



    def tearDown(self):
        # Restore settings
        if hasattr(self, 'settings_override'):
            for (key, value) in self.settings_override.items():
                if hasattr(self, '_old_%s' % key):
                    setattr(settings, key, getattr(self, '_old_%s' % key))



class BlugTestsBase(OverrideSettingsTestCase):
    urls = 'blogtools.tests.urls'

    settings_override = {
        'BLOG_NAME': 'Not another Wordpress blog',
        'INSTALLED_APPS': list(settings.INSTALLED_APPS) + ['blogtools.tests.blug'],
        'TEMPLATE_DIRS': (os.path.join(os.path.dirname(__file__), 'templates'),),
    }

    def setUp(self):
        super(BlugTestsBase, self).setUp()

        # Install test app -----------------------------------------------------

        load_app('blogtools.tests.blug')
        call_command('flush', verbosity=0, interactive=False)
        call_command('syncdb', verbosity=0, interactive=False)

        # Create test data -----------------------------------------------------

        # Users
        self.jon = User.objects.create_superuser('jon', 'jon@example.com', 'testpw')
        self.bob = User.objects.create_user('bob', 'bob@example.com', 'testpw')

        # Entries
        self.entry_cool = BlugEntry.objects.create(author=self.jon, status=1, excerpt='I won\'t spoil the content of this post', title="Supa cool title",
                                          body="Today I did something really cool!",
                                          slug="supa-cool-title",
                                          pub_date='2009-12-04',
                                          is_featured=True)
        self.entry_cool.tags = 'cool stuff'
        self.entry_cool.save()
        self.entry_hype = BlugEntry.objects.create(author=self.jon, status=1, title="Another blog post",
                                          body="I can't help but be the coolest guy wherever I go. Oh yeah, I'm so cool.",
                                          slug="another-blog-post",
                                          pub_date='2009-06-05',
                                          is_featured=True)
        self.entry_hype.tags = 'cool hype'
        self.entry_hype.save()
        self.entry_unpublished1 = BlugEntry.objects.create(author=self.jon, title="Can't publish this yet",
                                          body="This post isn't cool enough, so I won't publish it",
                                          slug="cant-publish-yet",
                                          pub_date='2009-06-05')
        self.entry_unpublished2 = BlugEntry.objects.create(author=self.jon, title="Can't publish this one either",
                                          body="This post is just crap. Don't publish it!",
                                          slug="cant-publish-either",
                                          pub_date='2008-09-15')
        self.entry_boring = BlugEntry.objects.create(author=self.jon, status=1, title="My life is boring",
                                          body="Please, subscribe to my blog and be my friend. Yawn.",
                                          slug="my-life-boring",
                                          pub_date='2008-10-14',
                                          is_featured=True)
        self.entry_initial = BlugEntry.objects.create(author=self.jon, status=1, title="Welcome to our blog",
                                          body="This is our new blog, and it's made with Django!",
                                          slug="welcome-our-blog",
                                          pub_date='2007-02-22')



