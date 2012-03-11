Django Galleries
=======

About
-----

Django Galleries is a photo gallery app that makes it easy to include galleries in your django apps. 
It has an easy to use, drag & drop interface for managing the photos. It also includes tools for
cropping the images.

Configuration
-------------

Sadly, there is a few things that needs to be configured. I will try to make this 
list smaller with time, but for now everything is necessary. This is somewhat because 
I am utilizing a few other apps.


In your `settings` module add the following:

    from easy_thumbnails import defaults
    THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
    ) + defaults.PROCESSORS


And this to `INSTALLED_APPS`

    'orderable',
    'easy_thumbnails',
    'image_cropping',
    'galleries',

Until the `respite` app figures out how to not require this, comment out the following line 
(be aware of the security implications this might have) `'django.middleware.csrf.CsrfViewMiddleware',` 
in your `MIDDLEWARE_CLASSES`.

Make sure that you have configured your `MEDIA_ROOT` to handle file uploads. Set it to something 
like `MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')`

And then add this to `MIDDLEWARE_CLASSES`:

    'respite.middleware.HttpMethodOverrideMiddleware',
    'respite.middleware.HttpPutMiddleware',
    'respite.middleware.HttpPatchMiddleware',
    'respite.middleware.JsonMiddleware',

This is requirements from `django-respite` that 'django-galleries` utilizes.

Then in your `urls.py` file

Add `(r'^admin/galleries', include('galleries.urls', namespace='galleries', app_name='galleries')),`

If you are in development mode, remember to host your media files accordingly, add something like this

    from django.conf import settings
    # Serve media files through Django if in debug mode
    if settings.DEBUG:
        urlpatterns += patterns('django.views',
            url(r'%s(?P<path>.*)$' % settings.MEDIA_URL[1:], "static.serve", {
                'document_root': settings.MEDIA_ROOT
            })
        )

At the moment, all images in a gallery has to use the same aspect ratio, it defaults to `16/9`, but you
can override that with the setting `GALLERIES_IMAGE_CROPPING_RATIO`:

    GALLERIES_IMAGE_CROPPING_RATIO = '5/4

And at last, remember to do a syncdb to update the database.

Usage
-----

Add the GalleryForeignKey to your models.py file, e.g:

    from galleries.fields import GalleryForeignKey

    class Article(models.Model):
        title = models.CharField(max_length=255)
        gallery = GalleryForeignKey('galleries.Gallery', blank=True, null=True, on_delete=models.SET_NULL)
    
        def __unicode__(self):
            return self.title

This is just a regular `models.ForeignKey` except that is has a default widget that adds all the 
javascript and styling that makes everything work. You could of course if you wanted to, not use the 
GalleryForeignKey, but override the widget on a regular ForeignKey, if so, use `galleries.widgets.GalleryForeignKeyWidget`.

And then in you're template you can do something like this:

    {% if article.gallery %}
    <div id="gallery">
      <ul>
        {% for image in article.gallery.images.all %}
        <li><img src="{% thumbnail image.image 610x343 box=image.cropping crop detail %}" alt="" /></li>
        {% endfor %}
      </ul>
    </div>
    {% endif %}