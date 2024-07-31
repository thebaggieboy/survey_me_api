from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from core import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'surveys', views.SurveyViewSet)
router.register(r'choices', views.ChoiceViewSet)
router.register(r'votes', views.VoteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts', include('allauth.urls')),
    path('api/', include(router.urls)),
    path('polls/', include('core.urls')),
    path('', include('rest_framework.urls', namespace='rest_framework'))


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)