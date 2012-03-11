from respite.urls import resource, routes

from views import GalleryViews, ImageViews

urlpatterns = resource(
    prefix = '/galleries/',
    views = GalleryViews,
    routes = [
        routes.route(
            regex = r'^(?:$|index(?:\.[a-zA-Z]+)?$)',
            view = 'create',
            method = 'POST',
            name = 'galleries',
        ),
        routes.route(
            regex = r'^(?:$|index(?:\.[a-zA-Z]+)?$)',
            view = 'index',
            method = 'GET',
            name = 'galleries',
        ),
        routes.route(
            regex = r'^(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$',
            view = 'show',
            method = 'GET',
            name = 'gallery',
        )
    ]
)

urlpatterns += resource(
    prefix = '/galleries/',
    views = ImageViews,
    routes = [
        routes.route(
            regex = r'^(?P<gallery_id>[0-9]+)/images/(?:$|index(?:\.[a-zA-Z]+)?$)',
            view = 'index',
            method = 'GET',
            name = 'images',
        ),
        routes.route(
            regex = r'^(?P<gallery_id>[0-9]+)/images/(?:$|index(?:\.[a-zA-Z]+)?$)',
            view = 'create',
            method = 'POST',
            name = 'images',
        ),
        routes.route(
            regex = r'^(?P<gallery_id>[0-9]+)/images/new(?:$|index(?:\.[a-zA-Z]+)?$)',
            view = 'new',
            method = 'GET',
            name = 'new_image',
        ),
        routes.route(
            regex = r'^(?P<gallery_id>[0-9]+)/images/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$',
            view = 'show',
            method = 'GET',
            name = 'image',
        ),
        routes.route(
            regex = r'^(?P<gallery_id>[0-9]+)/images/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$',
            view = 'replace',
            method = 'PUT',
            name = 'image',
        ),
        routes.route(
            regex = r'^(?P<gallery_id>[0-9]+)/images/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$',
            view = 'destroy',
            method = 'DELETE',
            name = 'image',
        )
    ]
)