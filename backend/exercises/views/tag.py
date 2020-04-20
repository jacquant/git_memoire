from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework import (
    permissions,
    viewsets,
)

from exercises.models.tag import Tag
from exercises.serializers.tag import (
    TagCUDSerializer,
    TagSerializer,
)


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class ActionsTagView(viewsets.ModelViewSet):
    """The actions possible and documents its for the api doc view."""

    def list(self, request, *args, **kwargs):
        """Provides a method to request a list of Tag objects.

        # Request: GET

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

         ## Return

        - The return is a **List** of TagSerializer objects

        ## Cache:

        - The list is saved in the redis cache if the key do not exist
        - Else return the list already saved in the cache
        - The cache is delete when a tag object is saved or deleted
        """
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Provides a method to request a specific Tag object.

        # Request: GET

        ## Parameters

        ### Query parameters

        - tag_id: the id of the tag

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a TagSerializer object

        ## Cache:

        - The requested tag object is not saved in the redis cache
        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a tag object is saved or deleted
        """
        return super().retrieve(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """An Api View which provides a method to create a Tag object.

        # Request: POST

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a TagCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a tag object is saved or deleted
        """
        return super().create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """An Api View which provides a method to update a specific Tag object.

        # Request: PUT

        ## Parameters

        ### Query parameters

        - tag_id: the id of the tag

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a TagCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a tag object is saved or deleted
        """
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Provides a method to partially_update a specific Tag object.

        # Request: PATCH

        ## Parameters

        ### Query parameters

        - tag_id: the id of the tag

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a TagCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a tag object is saved or deleted
        """
        return super().partial_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """An Api View which provides a method to delete a specific Tag object.

        # Request: DELETE

        ## Parameters

        ### Query parameters

        - tag_id: the id of the tag

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        None

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a tag object is saved or deleted
        """
        return super().destroy(self, request, *args, **kwargs)


class TagViewSet(ActionsTagView):
    """ViewSet uses for the Tag objects."""

    lookup_url_kwarg = "tag_id"
    lookup_field = "id"

    def get_queryset(self):
        """Return the query of objects needed for the lookups and the api."""
        key = "tags_all"
        if key in cache:
            return cache.get(key)
        tags = Tag.objects.all()
        cache.set(key, tags, timeout=CACHE_TTL)
        return tags

    def get_permissions(self):
        """Returns the list of permissions that this view requires."""
        if self.action in {"list", "retrieve"}:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Method to return the serializer to use in function of the action."""
        if self.action in {"list", "retrieve"}:
            return TagSerializer
        return TagCUDSerializer
