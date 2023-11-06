.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/
.. _Node.js: https://nodejs.org/dist/latest-v16.x/docs/api/
.. _NPM: https://docs.npmjs.com/
.. _Bootstrap: https://getbootstrap.com/docs/
.. _project-composer: https://github.com/sveetch/project-composer
.. _Webpack: https://webpack.js.org/
.. _django-configurations: https://django-configurations.readthedocs.io/
.. _Django Deovi: https://github.com/sveetch/django-deovi

============
Sveetch Home
============

*Generated from cookiecutter-bireli==0.3.9*

My home webserver with useful apps.


Main stack components
*********************

* `Python`_ >=3.10;
* `Django`_ >=4.0,<4.1;
* `project-composer`_ >=0.7.0,<0.8.0;
* `django-configurations`_ >=2.3.2;
* `Node.js`_ >=18.0.0;
* `NPM`_ >=8.0.0;
* `Bootstrap`_ 5.2.0;
* `Django Deovi`_ >=0.6.1;


Install
*******

First ::

    make install

Then: ::

    make frontend

Finally you will need a super user to login into admin: ::

    make superuser

Usage
*****

::

    make run

There is a lot of useful Makefile commands to manage your project, read the Makefile
help: ::

    make help
