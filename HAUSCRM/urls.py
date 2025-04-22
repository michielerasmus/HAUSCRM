from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from leads.views import SignupView, custom_logout_view, LandingPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('leads/', include('leads.urls', namespace="leads")),
    path('agents/', include('agents.urls', namespace="agents")),
    path('clients/', include('clients.urls', namespace="clients")),
    path('sales/', include('sales.urls', namespace="sales")),
    path('rentals/', include('rentals.urls', namespace="rentals")),
    path('tracker/', include('tracker.urls', namespace="tracker")),
    path('documents/', include('documents.urls', namespace="documents")),
    path('signup/', SignupView.as_view(), name="signup"),
    path('reset-password/', PasswordResetView.as_view(), name="reset-password"),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'), 
    path('password-reset-somplete/', PasswordResetDoneView.as_view(), name="password_reset_complete"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', custom_logout_view, name="logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
