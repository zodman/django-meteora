
from setuptools import setup, find_packages
setup(
    name = "django-meteora",
    version = "0.1",
    packages = find_packages(),
    package_data = {"":["templates/meteora/*.html"]},
    author = "Andres Vargas",
    author_email = "zodman@gmail.com",
    description = "A package for use meteora toolkit",
    url = "http://github.com/zodman/django-meteora",
   
)