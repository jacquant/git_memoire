from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)

from accounts.models.user import User
from accounts.serializers.user import UserSerializer, UpdateUserSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def get_custom_queryset(this):
    """Override method to have cache management.

    :return: the requested user(mail filter)
    :rtype: User
    """
    key = "users_id_{id}".format(id=this.request.user.mail)
    key_all = "users_all"
    if key in cache:
        return cache.get(key)
    elif key_all in cache:
        users = cache.get(key_all)
        user = users.filter(mail=this.request.user.mail)
        cache.set(key, user, timeout=CACHE_TTL)
        return user
    users = User.objects.all()
    cache.set(key_all, users, timeout=CACHE_TTL)
    user = users.filter(mail=this.request.user.mail)
    cache.set(key, user, timeout=CACHE_TTL)
    return user


def get_custom_object(this):
    """Override method to be able to filter with mail.

    :raises a: if the user has not the permission for the object
    :return: the requested user
    :rtype: User
    """
    queryset = this.filter_queryset(this.get_queryset())
    filter_kwargs = {"mail": this.request.user.mail}
    requested_obj = get_object_or_404(queryset, **filter_kwargs)

    # May raise a permission denied
    this.check_object_permissions(this.request, requested_obj)

    return requested_obj


class CreateUser(CreateAPIView):
    """An Api View which provides a method to save a new user.

     # Request: POST

     ## Parameters

     ### Body parameters

     - mail: string of an address email [1..255] char
     - last_name: string [1..40] char
     - first_name: string [1..30] char

     ## Permissions

     ### Token: Bearer

     - The user must be **authenticated**, so the given token must be valid

     ### User: IsAdminUser

     - The user must be an administrator

     ## Return

     - The return is the created object

     ## Cache:

    - No caching
    """

    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    model = User
    serializer_class = UserSerializer


class GetUserInfo(RetrieveAPIView):
    """An Api View which provides a method to get the user information.

    # Request: GET

    ## Parameters

    None

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a UserSerializer object corresponding of the user token

    ## Cache:

    - The list of users is saved if not existing
    - The requested user is saved
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_custom_queryset(self)

    def get_object(self):
        return get_custom_object(self)


class UpdateUser(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_queryset(self):
        return get_custom_queryset(self)

    def get_object(self):
        return get_custom_object(self)
