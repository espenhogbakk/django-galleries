from setuptools import setup

execfile('galleries/version.py')

setup(
    name = 'django-galleries',
    version = __version__,
    description = "Django Galleries is a photo gallery app with support for cropping.",
    long_description = open('README.md').read(),
    author = "Espen Høgbakk",
    author_email = "espen@hogbakk.no",
    url = "http://github.com/espenhogbakk/django-galleries",
    packages = ['galleries'],
    include_package_data = True,
    install_requires = [
        'easy_thumbnails', 
        'django-respite',
        'easy_thumbnails',
        'PIL',
        'django-orderable',
        'image_cropping'
    ],
    dependency_links = [
        'https://github.com/tkaemming/django-orderable/tarball/master#egg=orderable-dev',
        'https://github.com/jonasundderwolf/django-image-cropping/tarball/master#egg=image_cropping-dev'
    ]
)
