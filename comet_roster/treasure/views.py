from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from database.comet_roster import CometRoster
import os
from dotenv import load_dotenv
load_dotenv()
mongouser = os.getenv("MONGOUSER")
mongokey = os.getenv("MONGOKEY")
comet_roster = CometRoster(mongouser,mongokey)
@csrf_exempt
def treasureView(request):
    try:
        comet_roster.cloud_connect()
        key = comet_roster.retrieve("roster_key").iloc[0]["key"]
        header_key = request.headers["x-api-key"]
        user = request.GET.get("username")
        if request.method == "GET":
            if header_key == key:
                roster = comet_roster.get_secrets(user)
                complete = roster.to_dict("records")[0]
            else:
                complete = {"roster":[],"errors":"incorrect key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            complete = {}
        else:
            complete = {}
        comet_roster.disconnect()
    except Exception as e:
        complete = {"errors":str(e)}
    return JsonResponse(complete,safe=False)