from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view

from backbone.models import User 
from backbone.api.serializers import UserSerializer

@api_view(['POST',]) 
def api_detail_User(request):
  
  if request.method=="POST": 
    serializer=UserSerializer(data=request.data) 
    data={} 
    if serializer.is_valid(): 
      serializer.save()
      return Response(serializer.data,status.HTTP_201_CREATE) 
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
  
