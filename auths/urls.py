from rest_framework import routers
from .views import UserViewSet, DepartmentViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = router.urls

'''
Basic router url provides these endpoints:

GET /users/: Retrieve a list of all users
POST /users/: Create a new user
GET /users/{pk}/: Retrieve a single user by primary key
PUT /users/{pk}/: Update a single user by primary key
PATCH /users/{pk}/: Partially update a single user by primary key
DELETE /users/{pk}/: Delete a single user by primary key

'''