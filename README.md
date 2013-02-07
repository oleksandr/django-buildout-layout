Django-based Project Layout using Buildout
===================

Project layout is based on the file-uploads-server buildout layout:
<https://github.com/oleksandr/file-uploads-server>

It's a good practice based on my experience to use buildout for python projects deployments.
The main idea is to create a development environment as close to production as possible. Thus you avoid
lots of initial deployment pains and have more chances to roll back your release after it fails on the staging.

After several projects this layout has been generalized and shared here as a hopefully good practice to be re-used in my projects and hopefully by someone else as well.

**Assumptions**
* You have Postgres installed (in fact the layout does not depend on it, configurable)
* Python / Django 1.5 (this layout include 1.5c1 included in the download cache)
* gunicorn as WSGI-server
* nginx as uploads handler and as a web-frontend (proxy)
* Supervisor for processes orchestration

*NB: You can still use virtualenv and completely isolate from your system, but this is not necessary.
A buildout will take care of this.*

Development Installation
-------------

You need a Postgres database system. For OSX you can either install one with brew, or try to use
the Postgres.app (http://postgresapp.com). Additionally a pgAdmin application will help you
to manage your local Postgres installation.

Typical buildout procedure:

    $ touch buildout.cfg
    $ nano buildout.cfg

Specify the following in the buildout.cfg (this will inherit from the development profile):

    [buildout]
    extends = profiles/development.cfg

Additionally you need to extend the *project-env* section in buildout.cfg to override the settings specific for your machine.
Do not modify the original configuration files. Just include the corresponding section in the buildout.cfg you've just created:

    [project-env]
    db-host = <host of your db>
    db-port = <your custom port>
    db-user = <your custom user>
    db-pass = <your password>
    db-name = <name of your database>
    django-debug = True

Create the buildout directory structure (initialize buildout):

    $ python boostrap.py

This will created a standard buildout directory structure. Now it's time to run the buildout:

    $ bin/buildout -D

After the successful execution of this command you should have a working development environment.
Now start the services with supervisord command and check their status:

    $ bin/supervisord
    $ bin/supervisorctl status
    backend                          RUNNING    pid 54959, uptime 0:00:02
    nginx                            RUNNING    pid 54958, uptime 0:00:02
    watchmedo                        RUNNING    pid 54960, uptime 0:00:02

As you can see we have a *backend* process running, which is a Django application served via gunicorn.
The *nginx* process is a web-frontend that proxies requests to *backend* and handles the uploads using
a nginx uploads module (<http://www.grid.net.ru/nginx/upload.en.html>).
The *watchmedo* process is listening for changes in the <root>/src/project folder filtering *.py files and
restarts the backend if the code if modified. In this way we have a *reloadable* behavior of Django's *runserver*
command.

Of course you need to initialize your Django application:

    $ bin/django syncdb
    $ bin/django migrate

And then open the following link in your browser to access your application: <http://localhost:8080>
Additionally the SSL support is configured for your application if required: <https://localhost:8443>

