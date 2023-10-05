from django.urls import include, path

from app.api.autodiscover import autodiscover
from app.api.v0_1.routers import router as v0_1

autodiscover()

urlpatterns = [
    path("v0_1/", include(v0_1.urls)),
]
