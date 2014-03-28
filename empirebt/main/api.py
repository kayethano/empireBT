# myapp/api.py
from tastypie.resources import ModelResource
from empirebt.main.models import UserCustom


class UserResource(ModelResource):
    class Meta:
        queryset = UserCustom.objects.all()
        resource_name = 'commander'