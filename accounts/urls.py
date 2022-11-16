from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import SignUpView, AccountView, AccountUpdateView

app_name = 'accounts'

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('<int:account_id>/', AccountView.as_view()),
    path('update/', AccountUpdateView.as_view())

]
