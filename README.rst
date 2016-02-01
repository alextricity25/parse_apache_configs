# parse_apache_configs
A simple python library that will parse apache configs and convert them to a python data structure.

====================
parse_apache_configs
====================
A simple python library that will parse apache configs and convert them to a python data structure.
This will then allow the configs to be manipulated programatically.


==============
Main Functions
==============

To use:

.. code-block:: python
  
    from parse_apache_configs import parse_config

Parse the apache config via file path, and return a python object representation:

.. code-block:: python

    apache_parse_obj = parse_config.ParseApacheConfig(apache_config_path="/some/path/to/file")
    apache_config = apache_parse_obj.parse_config()

or to parse the apache config as a string:

.. code-block:: python

    apache_parse_obj = parse_config.ParseApacheConfig(apache_file_as_string=apache_string_obj)
    apache_config = apache_parse_obj.parse_config()

Now you can use the apache_config object to manipulate the apache config.

To add or override an existing directive and return the result:

.. code-block:: python

    apache_config = apache_parse_obj.add_directive(apache_config, "SomeDirectiveName", "SomeDirectiveArguments", "<VirtualHost *:80>")


The code above will add the line "SomeDirectiveName SomeDirectiveArguments" under <VirtualHost \*:80>. If the directive
is already there, then it's arguments will be overridden.
Keep in mind that directives in nested tags can also be added/overridden, but their full "path" must be fed into
add_directive. For example, given the following apache file:

.. code-block:: apache

    <VirtualHost *:80>
      ServerName example.org
      ServerAlias *.example.org
      ErrorLog /var/log/httpd/example.err
      DocumentRoot /var/www/example.org
      <Directory "/var/www/example.org">
        Order allow,deny
        Allow from all
      </Directory>
    </VirtualHost>

To override the "Order" directive under <Directory "/var/www/example.org">, the invocation to add_directive would look like this:

.. code-block:: python

    apache_config = apache_parse_obj.add_directive(apache_config, "Order", "deny,allow", "<VirtualHost *:80>", "<Directory "/var/www/example.org">")


To convert the apache_config object into a printable string:

.. code-block:: python

    apache_config_string = apache_parse_obj.get_apache_config(apache_config)
    print apache_config_string

