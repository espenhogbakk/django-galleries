from django.conf import settings

ADMIN_THUMB_HEIGHT = 140
IMAGE_CROPPING_RATIO = getattr(settings, 'GALLERIES_IMAGE_CROPPING_RATIO', '16x9')

# Find the ADMIN_THUMBNAIL_SIZE based on the given IMAGE_CROPPING_RATIO
width, height = [int(i) for i in IMAGE_CROPPING_RATIO.split("x")]

ADMIN_THUMBNAIL_SIZE = getattr(settings, 'IMAGE_CROPPING_THUMB_SIZE', tuple([int((ADMIN_THUMB_HEIGHT/height)*width), int((ADMIN_THUMB_HEIGHT/height)*height)]))
