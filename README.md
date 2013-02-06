Django-based Project Layout using Buildout
===================

Project layout is based on the file-uploads-server buildout layout:
https://github.com/oleksandr/file-uploads-server

A good practice based on my experience is to use buildout for python
projects deployments.
Main idea is to create a development environment as close to production
as possible.
After several projects this layout has been generalized and shared here
as a hopefully good practice to be re-used in my projects and hopefully
by someone else as well.



Development Installation
-------------

You need a Postgres database system. For OSX you can either install one with brew, or try to use
the Postgres.app (http://postgresapp.com). Additionally a pgAdmin application will help you
to manage your local Postgres installation.

Typical buildout procedure:

    $ python bootstrap.py
    $ touch buildout.cfg
    $ nano buildout.cfg

Specify the following in the buildout.cfg:

    [buildout]
    extends = profiles/development.cfg

Run the buildout:

    $ bin/buildout -D

TODO: Describe the layout.

Running
-------------

You can run directly 'bin/django runserver' command or the full pack of services (similar how it goes in production) using 'bin/supervisord' command.

TODO: Provide examples.

Adding project dependencies
-------------

Described where to add the eggs, etc.



-------------