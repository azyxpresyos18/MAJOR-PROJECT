from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App routes
    path('api/accounts/',    include('accounts.urls')),
    path('api/clients/',     include('clients.urls')),
    path('api/products/',    include('products.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/scheduling/',  include('scheduling.urls')),
]