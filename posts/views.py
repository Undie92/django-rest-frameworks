from django.db.models import Count
from rest_framework import generics, filters, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostsSerializer


class PostList(generics.ListCreateAPIView):
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at',
    ]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class Postdetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostsSerializer
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')