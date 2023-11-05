"""
NOTE: Since the initials datas may change from a project to another, those tests try
to make the less assumptions possible on initial datas.
"""
import logging

from django.contrib.sites.models import Site

from project_utils.initial_loader import InitialDataLoader
from project_utils.user import safe_get_user_model


def test_cms_demomaker_blank(caplog, db):
    """
    Without pages involved there is no requirement.
    """
    caplog.set_level(logging.DEBUG, logger="project-utils")

    maker = InitialDataLoader()
    maker.create({})

    User = safe_get_user_model()

    assert User.objects.count() == 0


def test_cms_demomaker_success(caplog, db):
    """
    InitialDataLoader should correctly create all objects from given structure.
    """
    caplog.set_level(logging.DEBUG, logger="project-utils")

    maker = InitialDataLoader()
    maker.create({
        "global_author": "admin",
        "site": {
            "name": "Demo",
            "domain": "127.0.0.8001",
        },
        "users": {
            "guest": {},
            "superuser": {
                "status": "superuser",
            },
            "admin": {
                "status": "admin",
                "first_name": "Admin",
                "last_name": "Staff",
                "email": "support@mail.com",
                "password": "ok",
            },
        },
    })

    site = Site.objects.get_current()
    assert site.name == "Demo"
    assert site.domain == "127.0.0.8001"

    # All user have been created with their respected staff level
    User = safe_get_user_model()
    assert User.objects.count() == 3
    assert User.objects.filter(is_staff=True).count() == 2
    assert User.objects.filter(is_superuser=True).count() == 1


def test_cms_demomaker_fixture(caplog, db, load_initials):
    """
    The Pytest fixture should load the initial data.

    We just check some content have been created with success but without to check the
    contents themselves.

    This assumes there is at least a created user and page, nothing more so the
    initials data may be changed.

    NOTE: This won't be safe for project without CMS.
    """
    caplog.set_level(logging.DEBUG, logger="project-utils")

    User = safe_get_user_model()
    assert User.objects.count() > 0
