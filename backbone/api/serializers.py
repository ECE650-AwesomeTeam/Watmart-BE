from rest_framework import serializers
from backbone.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fname ', 'lname', 'birthday','gender','wat_id','occupation','phone']