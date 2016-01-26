from setuptools import setup

setup(name='parse_apache_configs',
      version="0.0.2",
      description="A python module to parse apache config files.",
      url='http://github.com/alextricity25/parse_apache_configs',
      download_url = 'https://github.com/alextricity25/parse_apache_configs/tarball/0.0.2',
      author='Miguel Alex Cantu',
      author_email='miguel.cantu@rackspace.com',
      packages=['parse_apache_configs'],
      install_requires=[
          'pyparsing',
      ],
      zip_safe=False)
