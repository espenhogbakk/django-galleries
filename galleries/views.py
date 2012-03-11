from respite import Views, Resource
from respite.utils import generate_form
from django.http import HttpResponse

from models import Gallery, Image

class GalleryViews(Views, Resource):
    supported_formats = ['json']
    model = Gallery

class ImageViews(Views, Resource):
    supported_formats = ['json']
    model = Image
    
    def index(self, request, gallery_id):
        """Render a list of images."""
        
        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The gallery could not be found.'
                },
                status = 404,
                prefix_template_path = False
            )
        
        images = gallery.images.all()

        return self._render(
            request = request,
            template = 'index',
            context = {
                'images': images,
            },
            status = 200
        )
    
    def new(self, request, gallery_id):
        """Render a form to create a new object."""
        
        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The gallery could not be found.'
                },
                status = 404,
                prefix_template_path = False
            )
        
        form = (self.form or generate_form(self.model))()

        return self._render(
            request = request,
            template = 'new',
            context = {
                'form': form
            },
            status = 200
        )
    
    def create(self, request, gallery_id):
        """Create a new object."""
        
        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The gallery could not be found.'
                },
                status = 404,
                prefix_template_path = False
            )

        form = (self.form or generate_form(self.model))(request.POST, request.FILES)

        if form.is_valid():
            image = form.save()
            
            # Update the gallery
            gallery.images.add(image)

            return self._render(
                request = request,
                template = 'show',
                context = {
                    'image': image
                },
                status = 201
            )
            return HttpResponse("successfull")
        else:
            return self._render(
                request = request,
                template = 'new',
                context = {
                    'form': form
                },
                status = 400
            )
    
    def show(self, request, gallery_id, id):
        """Render a single object."""

        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The gallery could not be found.'
                },
                status = 404,
                prefix_template_path = False
            )

        try:
            image = gallery.images.get(id=id)
        except self.model.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The image could not be found.'
                },
                status = 404,
                prefix_template_path = False
            )
        
        return self._render(
            request = request,
            template = 'show',
            context = {
                'image': image
            },
            status = 200
        )
    
    
    def replace(self, request, gallery_id, id):
        """Replace an object."""
        
        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The gallery could not be found.'
                },
                status = 404,
                prefix_template_path = False
            )
        
        try:
            object = self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The %s could not be found.' % self.model.__name__.lower()
                },
                status = 404,
                prefix_template_path = False
            )

        form = (self.form or generate_form(self.model))(request.PUT, instance=object)

        if form.is_valid():
            object = form.save()

            return self.show(request, gallery_id, id)
        else:
            return self._render(
                request = request,
                template = 'edit',
                context = {
                    'form': form
                },
                status = 400
            )
    
    def destroy(self, request, gallery_id, id):
        """Delete an object."""
        
        try:
            gallery = Gallery.objects.get(id=gallery_id)
        except Gallery.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The gallery could not be found.'
                },
                status = 404,
                prefix_template_path = False
            )
        
        try:
            object = self.model.objects.get(id=id)
            object.delete()
        except self.model.DoesNotExist:
            return self._render(
                request = request,
                template = '404',
                context = {
                    'error': 'The %s could not be found.' % self.model.__name__.lower()
                },
                status = 404,
                prefix_template_path = False
            )

        return self._render(
            request = request,
            template = 'destroy',
            status = 200
        )