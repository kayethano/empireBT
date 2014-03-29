# myapp/api.py
from tastypie.resources import ModelResource
from empirebt.main.models import *


class GeneralAuthorization(ModelResource):
    class Meta:
        queryset = UserCustom.objects.all()
        resource_name = 'general.json'
        filtering = {"id": [ "exact", "in" ],
        			"username" : ["exact", "in"]}