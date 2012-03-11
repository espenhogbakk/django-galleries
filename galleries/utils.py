from galleries.settings import ADMIN_THUMBNAIL_SIZE

from easy_thumbnails.files import get_thumbnailer

def thumbnail(image_path, cropping=None):
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'size': ADMIN_THUMBNAIL_SIZE,
        'crop': True,
        'box': cropping
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb.url

def croppable(image_path):
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'size': (500, 500),
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb.url