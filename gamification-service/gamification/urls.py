from django.urls import path
from .views import UserBadgesView, UserScoreView, AssignBadgeView
from .views import UpdateScoreView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('badges/<int:user_id>/', UserBadgesView.as_view(), name='user_badges'),
    path('score/<int:utilisateur_id>/', UserScoreView.as_view(), name='user_score'),
    path('badges/assign/', AssignBadgeView.as_view(), name='assign_badge'),
    path('score/update/', UpdateScoreView.as_view(), name='update_score'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


