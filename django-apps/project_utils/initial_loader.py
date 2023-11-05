"""

Expected data structure
***********************

    {
        "global_author": "emencia",
        "site": {
            "name": "Demo",
            "domain": "127.0.0.8001"
        },
        "users": {
            "emencia": {
                "first_name": "Anne",
                "last_name": "Nonymous",
                "email": "my@email.com",
                "password": "ok"
            },
        }
    }


Structure description
*********************

Site, users are not required.

global_author
    The username to retrieve from created users and that will be assigned to every
    objects which depends from a User object. This is required.
site
    An optional dictionnary with items ``name`` and ``domain`` to update the current
    Site object. Both items are strings and optionals.
users
    A dictionnary of user items to create. Each item is an user, user keyname will be
    used for the username and user values ``first_name``, ``last_name``, ``email`` and
    ``password`` are all strings and optional to fill the User object. Empty user
    values are automatically filled with random content. Default password is
    ``secret``.

    Additionally, user item can have a ``status`` value that is either ``admin`` or
    ``superuser`` to set its status level, any other value assume the user is a basic
    user without any staff level.


Flexbility note
***************

Currently this is hardly coupled to Django site, Django auth and CMS. This is not
really flexible and will be broken if CMS is not enabled.

This could be improved by splitting InitialDataLoader into application parts managed by
project-composer.

"""
import json
from pathlib import Path

from django.conf import settings
from django.core.validators import slug_re
from django.contrib.sites.models import Site

from .exceptions import InitialDataLoaderException
from .factories import UserFactory
from .logger import BaseOutput


class InitialDataLoader:
    """
    Helper class that will create implemented objects from a given structure.

    All objects that need a language code are created using the default project
    language from ``settings.LANGUAGE_CODE``. No multilingual objects are supported.

    Keyword Arguments:
        output_interface (class): Class to manage logging output. It must implement
            an interface like ``project_utils.logger.BaseOutput``. Default is to use
            ``BaseOutput`` which use Python logging.

    Attributes:
        log (object): Logging output manager as defined from ``output_interface``.
    """
    def __init__(self, output_interface=None):
        self.log = output_interface or BaseOutput()

    def validate_global_author(self):
        """
        Validate global author value is valid.
        """
        if not self.global_author:
            msg = "No 'global_author' have been given despite it is required."
            raise InitialDataLoaderException(msg)

        if isinstance(self.global_author, str):
            msg = "Unable to find created user for global author username '{}'."
            raise InitialDataLoaderException(msg.format(self.global_author))

        return True

    def site_update(self, data):
        """
        Update current site fields

        Arguments:
            data (dict): Site data.
        """
        if data.get("domain") or data.get("name"):
            self.log.info("- Editing site object")
            site = Site.objects.get_current()
            site.name = data.get("name") or site.name
            site.domain = data.get("domain") or site.domain
            site.save()

        return site

    def user_creation(self, data):
        """
        Create all user items and assign an user as the global author if it match
        username from 'global_author'.

        Arguments:
            data (dict): User item data.
        """
        created = []

        for username, fields in data.items():
            self.log.info("- Creating user: {}".format(username))
            payload = {"username": username}

            status = fields.pop("status", "user")
            if status == "superuser":
                payload["flag_is_superuser"] = True
            elif status == "admin":
                payload["flag_is_admin"] = True

            payload.update(fields)
            user = UserFactory(**payload)
            created.append(user)

            if user.username == self.global_author:
                self.global_author = user

        return created

    def create(self, structure):
        """
        Create all objects from given data structure.

        Arguments:
            structure (dict): Dictionnary of data structure. See *Expected data
                structure* and *Structure description* documentation for details.
        """
        self.global_author = structure.get("global_author")

        site = None
        users = None

        if structure.get("site"):
            site = self.site_update(structure["site"])

        if structure.get("users"):
            users = self.user_creation(structure["users"])
            self.log.info("* Created {} user(s)".format(len(users)))

        return {
            "site": site,
            "users": users,
        }

    def load(self, path):
        """
        Load data structure from a JSON file as given in argument and create its
        objects.

        Arguments:
            path (string or pathlib.Path): Path to the JSON file to load.

        Returns:
            dict: Dictionnary of created objets as returned
            by ``InitialDataLoader.create()``.
        """
        return self.create(
            json.loads(Path(path).read_text())
        )
