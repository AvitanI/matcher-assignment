from django.urls import path
from .views import candidate_finder
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('candidate/job/<int:job_id>/', candidate_finder),
    path('', get_schema_view(
            title="Candidate API",
            description="API for candidate operations",
            version="1.0.0"
        ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui')
]