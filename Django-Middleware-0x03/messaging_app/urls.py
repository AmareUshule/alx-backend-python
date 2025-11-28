from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse  # <-- import HttpResponse

# Simple home view
def home(request):
    return HttpResponse("Welcome to the Messaging App API! Go to /admin/ or /api/")

# DRF router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', home),  # root URL now returns a simple message
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API routes
    path('api/', include(router.urls)),

    # DRF session login/logout
    path('api-auth/', include('rest_framework.urls')),
]

