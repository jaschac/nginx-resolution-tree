from distutils.core import setup
from json import loads
from os.path import dirname, realpath

setup(
    author = 'Jascha Casadio',
    author_email = 'jaschacasadio@lostinmalloc.com',
    description = 'Nginx configuration resolution tree.',
    license = 'LICENSE',
    long_description = 'A Python package that resolves Nginx\'s listening ports, server names and locations into proper configuration files.',
    name = 'nginx-resolution-tree',
    packages =[
                'nrt',
                'nrt.tests',
                ],
    scripts = [],
    url = 'https://github.com/jaschac/nginx-resolution-tree',
    version = loads(open("%s/metadata.json" % (dirname(realpath(__file__))), "r").read()).get("version"),
)
