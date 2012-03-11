from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField

from galleries.settings import IMAGE_CROPPING_RATIO

from orderable.models import OrderableModel

from django.utils.translation import ugettext as _
from utils import thumbnail, croppable

class Gallery(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __unicode__(self):
        return self.title
    
    @property
    def num_images(self):
        return self.images.all().count()
    
    def serialize(self):
        context = {
            'id': self.id,
            'title': self.title,
            'num_images': self.num_images,
            'images': self.images.all()
        }
        return context

class Image(OrderableModel):
    gallery = models.ForeignKey(Gallery, related_name="images")
    title = models.CharField(_('title'), max_length=100, blank=True)
    caption = models.TextField(_('caption'), blank=True)
    image = ImageCropField(blank=True, null=True, upload_to='uploads/galleries/images/')
    cropping = ImageRatioField('image', IMAGE_CROPPING_RATIO) # size is "width x height"
    
    class Meta(OrderableModel.Meta):
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __unicode__(self):
        return '%s' % (self.title or self.id)
    
    @property
    def thumbnail(self):
        return thumbnail(self.image, self.cropping)

    @property
    def croppable(self):
        return croppable(self.image)

    
    def serialize(self):
        context = {
            'id': self.id,
            'gallery': self.gallery.id,
            'title': self.title,
            'caption': self.caption,
            'image': self.image,
            'cropping': self.cropping,
            'thumbnail': self.thumbnail,
            'croppable': self.croppable,
            'org_width': self.image.width,
            'org_height': self.image.height,
            'order': self.order
        }
        return context
