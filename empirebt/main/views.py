# Create your views here.
from django.http import HttpResponse
import empirebt.main.models as models
import json

def auth_general(req):
	if "token" not in req.GET or "user_id" not in req.GET:
		return HttpResponse(json.dumps({'valid': False}))
	res = models.UserCustom.objects.filter(id = req.GET["user_id"], websocket_token = req.GET["token"]).exists()
	return HttpResponse(json.dumps({'valid': res}))

def empire_auth(req):
	if "token" not in req.GET or "user_id" not in req.GET or "empire_id" not in req.GET:
		return HttpResponse(json.dumps({'valid': False}))
	res = models.UserCustom.objects.filter(id = req.GET["user_id"], websocket_token = req.GET["token"], commander = req.GET["empire_id"]).exists()
	return HttpResponse(json.dumps({'valid': res}))

