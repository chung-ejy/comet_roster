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
def rosterView(request):
    try:
        comet_roster.cloud_connect()
        key = comet_roster.retrieve("roster_key").iloc[0]["key"]
        header_key = request.headers["x-api-key"]
        if request.method == "GET":
            if header_key == key:
                roster = comet_roster.retrieve("roster")
                complete = {"roster":roster.to_dict("records")}
            else:
                complete = {"roster":[],"errors":"incorrect key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            info = json.loads(request.body.decode("utf-8"))
            if header_key == key:
                user = info["username"]
                update= comet_roster.update_roster(user,info)
                complete = update
            else:
                complete = {}
        elif request.method == "POST":
            info = json.loads(request.body.decode("utf-8"))
            if header_key == key:
                result = {}
                result["username"] = info["username"]
                result["live"] = False
                result["test"] = False
                comet_roster.store("roster",pd.DataFrame([result]))
                complete = result
            else:
                complete = {}
        else:
            complete = {}
        comet_roster.disconnect()
    except Exception as e:
        complete = {"roster":[],"errors":str(e)}
    return JsonResponse(complete,safe=False)