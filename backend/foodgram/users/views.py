from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Follow
from api.serializers import FollowSerializer


@api_view([ 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def add_follow(request, pk):
    """Following and unfollowing authors"""
    user = get_object_or_404(User, username=request.user.username)
    author = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        try:
            Follow.objects.create(
                user=user,
                author=author
            )
        except IntegrityError:
            return Response('Невозможно дважды подписаться на того же автора',
                             status=status.HTTP_400_BAD_REQUEST)

        follows = User.objects.all().filter(username=author)
        serializer = FollowSerializer(
            follows,
            context={'request': request},
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
