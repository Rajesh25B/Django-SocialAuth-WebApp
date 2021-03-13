from django.urls import path, include
from django.views.generic.base import TemplateView

from users.views import UserLoginView, SetPasswordView, UserDetailsView, \
                        UsersListView, UserSearchView


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html', name='home'), name='user_login'),
    path('login/', include('django.contrib.auth.urls')),
    path('social_auth/', include('social_django.urls', namespace='social')),
    path('normal_login/', UserLoginView.as_view(), name='user-login'),
    path('set_password/', SetPasswordView.as_view(), name='set-password'),
    path(r'user/<int:user_id>/', UserDetailsView.as_view(), name='user-details'),
    path('user/search/', UserSearchView.as_view(), name='user-search'),
]