from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from account.views import MyTokenObtainPairView
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Ecommerce API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns =[
    path('admin/', admin.site.urls),
    path('api/auth/', include('account.urls')),
    path('api/admin/', include('admin_management.urls')),
    path('api/', include('products.urls')),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
