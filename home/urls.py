from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('frequently-asked-questions', views.frequentlyaskedquestions, name = "frequentlyaskedquestions"),
    path('privacy-policy', views.privacypolicy, name = "privacypolicy"),
    path('terms-and-conditions', views.termsandconditions, name = "termsandconditions"),
    path('careers/', views.careers, name = "careers"),
    path('careers/<int:jobopportunity_id>/<slug:slug>/', views.job, name = "job_detail"),
]
