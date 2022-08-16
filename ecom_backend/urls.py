from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from account.views import MyTokenObtainPairView


urlpatterns =[
    path('admin/', admin.site.urls),
    path('api/auth/', include('account.urls')),
    path('api/', include('products.urls')),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
