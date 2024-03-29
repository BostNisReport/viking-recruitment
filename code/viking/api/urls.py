from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register(r'jobs', views.JobViewSet)

urlpatterns = router.urls
