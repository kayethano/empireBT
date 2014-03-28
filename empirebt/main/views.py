# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from empirebt.main.models import UserCustom

@login_required
def tokenizer(request):
	"""
	Return a json in format Response: { “token” : “<token>”, “user_id”: “<userid> }
	"""
	user = request.user
	return HttpResponse(json.dumps({'token': user.websocket_token, 'user_id': user.pk }))

def general_auth(request):
	"""
	Return a json in format Response: { “valid” : true/false, “username”: “Mamsaac” }

	"""
	token = request.GET['token']
	user_id = request.GET['user_id']
	try:
		user = UserCustom.objects.get(pk=user_id)
	except UserCustom.DoesNotExist:
		return HttpResponse(json.dumps({'valid': False }))
	if user.websocket_token == token:
		return HttpResponse(json.dumps({'valid': True, 'username': user.username }))
	else:
		return HttpResponse(json.dumps({'valid': False, 'username': user.username }))



#Request: /authorization/general.json?token=<sometoken>&user_id=<someuserid>
#Response: { “valid” : true/false, “username”: “Mamsaac” }


