from django.db import models

from widgets import GalleryForeignKeyWidget

class GalleryForeignKey(models.ForeignKey):
    """
    A field that references a Gallary, this will only work in the admin cause
    it leverages the raw_id widget.
    """

    def __init__(self, model, *args, **kwargs):
        super(GalleryForeignKey, self).__init__(model, *args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = GalleryForeignKeyWidget(self.rel, using=kwargs.get('using'))
        return super(GalleryForeignKey, self).formfield(*args, **kwargs)

    def south_field_triple(self):
        """
        Return a suitable description of this field for South.
        """
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.related.ForeignKey"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)