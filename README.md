Project
===================

Project layout is based on the file-uploads-server buildout layout:
https://github.com/oleksandr/file-uploads-server


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

