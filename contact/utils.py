from rest_framework import generics, status
from rest_framework.response import Response

class SingletonAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    A Reusable Base View for Singleton Models.
    """
    def get_object(self):
        return self.queryset.first()

    def post(self, request, *args, **kwargs):
        if self.queryset.exists():
            return Response({"detail": "Instance Already Exists!"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)