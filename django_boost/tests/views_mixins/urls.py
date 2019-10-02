from django.urls import path

from . import views

urlpatterns = [
    path('content_type_none/', views.AllowContentTypeNoneView.as_view()),
    path('content_type_allowed/', views.AllowContentTypeAllowedView.as_view()),
    path('x', views.AllowContentTypeView.as_view()),
    path('csrf_exempt/', views.CSRFExemptView.as_view()),
    path('dynamic_redirect/', views.DynamicRedirectView.as_view()),
    path('json_request/', views.JsonRequestView.as_view()),
    path('json_response/', views.JsonResponseView.as_view()),
    path('limited_term/', views.LimitedTermView.as_view()),
    path('limited_term/before/start/',
         views.LimitedTermBeforeStartView.as_view()),
    path('limited_term/before/end/', views.LimitedTermBeforeEndView.as_view()),
    path('limited_term/after/start/',
         views.LimitedTermAfterStartView.as_view()),
    path('limited_term/after/end/', views.LimitedTermAfterEndView.as_view()),
    path('re_auth/', views.ReAuthenticationRequiredView.as_view()),
    path('staff_only/', views.StaffMemberRequiredView.as_view()),
    path('super_only/', views.SuperuserRequiredView.as_view()),
    path('user_agent/', views.UserAgentView.as_view()),
    path('user_kwargs/', views.ViewUserKwargsView.as_view())
]
