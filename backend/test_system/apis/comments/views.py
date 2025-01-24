from django.shortcuts import get_object_or_404
from .serializers import CommentsGetOrCreateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from test_system.apps.comments.models import Comment


class CommentsCreateView(APIView):
    
    def post(self, request, format=None):
        """ create a comment under a single media object """
        serializer = CommentsGetOrCreateSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentGetUpdateDeleteView(APIView):
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

    def get(self, request, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        return Response(CommentsGetOrCreateSerializer(comment, context={"request": request}).data)

    def put(self, request, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentsGetOrCreateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return Response(CommentsGetOrCreateSerializer(comment).data)