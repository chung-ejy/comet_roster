from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/roster/",include("roster.urls")),
    path("api/trade_params/",include("trade_params.urls")),
    path("api/treasure/",include("treasure.urls")),
]
