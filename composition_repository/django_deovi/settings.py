from project_composer.marker import EnabledApplicationMarker


class DjangoDeoviSettings(EnabledApplicationMarker):
    """
    DjangoDeovi settings
    """
    DEVICE_PAGINATION = 15
    """
    Device entry per page limit for pagination, set it to ``None`` to disable
    pagination.
    """

    DIRECTORY_PAGINATION = 48
    """
    Directory entry per page limit for pagination, set it to ``None`` to disable
    pagination.
    """

    MEDIAFILE_PAGINATION = 60
    """
    MediaFile entry per page limit for pagination, set it to ``None`` to disable
    pagination.
    """

    @classmethod
    def post_setup(cls):
        super(DjangoDeoviSettings, cls).post_setup()

        cls.INSTALLED_APPS.extend([
            "django_deovi",
        ])
