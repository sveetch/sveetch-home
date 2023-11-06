from django.urls import path, include

from project_composer.marker import EnabledApplicationMarker


class DjangoDeoviUrls(EnabledApplicationMarker):
    """
    DjangoDeovi urls
    """
    def load_urlpatterns(self, urlpatterns):
        """
        Mount application urls
        """
        urlpatterns = super().load_urlpatterns(urlpatterns)

        return [
            path("deovi/", include("django_deovi.urls")),
        ] + urlpatterns
