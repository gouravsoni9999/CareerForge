from django.urls import path

from .views import (
    OpportunityListView,
    OpportunityDetailView,
    RecruiterOpportunityListCreateView,
    RecruiterOpportunityDetailView,
    PublishOpportunityView,
    RecruiterOpportunityApplicationsView,
)

urlpatterns = [
    path(
        "",
        OpportunityListView.as_view(),
        name="opportunity-list",
    ),
    path(
        "manage/",
        RecruiterOpportunityListCreateView.as_view(),
        name="recruiter-opportunity-list",
    ),
    path(
        "manage/<int:pk>/",
        RecruiterOpportunityDetailView.as_view(),
        name="recruiter-opportunity-detail",
    ),
    path(
        "manage/<int:pk>/publish/",
        PublishOpportunityView.as_view(),
        name="recruiter-opportunity-publish",
    ),
    path(
        "manage/<int:pk>/applications/",
        RecruiterOpportunityApplicationsView.as_view(),
        name="recruiter-opportunity-applications",
    ),
    path(
        "<int:pk>/",
        OpportunityDetailView.as_view(),
        name="opportunity-detail",
    ),
]
