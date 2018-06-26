from demo.sample import views
from rest_framework import routers

app_name = 'sample'

router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewSet)

urlpatterns = router.urls
