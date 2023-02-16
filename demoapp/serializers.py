from rest_framework import serializers
from demoapp.models import Examportal

class ExamportalSerializer(serializers.ModelSerializer):
   

    class Meta:
        model=Examportal
        fields='__all__'