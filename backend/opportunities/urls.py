from django.urls import path

from .views import (
    OpportunityListView,
    OpportunityDetailView,
)

urlpatterns = [
    path(
        "",
        OpportunityListView.as_view(),
        name="opportunity-list",
    ),
    path(
        "<int:pk>/",
        OpportunityDetailView.as_view(),
        name="opportunity-detail",
    ),
]