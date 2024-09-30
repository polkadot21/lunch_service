from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuViewSet, EmployeeViewSet, VoteViewSet

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet)
router.register(r"menus", MenuViewSet)
router.register(r"employees", EmployeeViewSet)
router.register(r"votes", VoteViewSet)

urlpatterns = router.urls
