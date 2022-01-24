from django.shortcuts import render
from django.http.response import JsonResponse
import pickle
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import requests
from pymongo import MongoClient
from database.comet_roster import CometRoster
import os
from dotenv import load_dotenv
load_dotenv()
mongouser = os.getenv("MONGOUSER")
mongokey = os.getenv("MONGOKEY")
comet_roster = CometRoster(mongouser,mongokey)
@csrf_exempt
def tradeParamsView(request):
    try:
        comet_roster.cloud_connect()
        key = comet_roster.retrieve("roster_key").iloc[0]["key"]
        if request.method == "GET":
            info = json.loads(request.body.decode("utf-8"))
            if info["key"] == key:
                user = info["username"]
                trade_params = comet_roster.retrieve_user_test_trade_params(user)
                complete = {"test_trade_params":trade_params.to_dict("records")}
            else:
                complete = {"roster":[],"errors":"incorrect key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            info = json.loads(request.body.decode("utf-8"))
            if info["key"] == key:
                result = {}
                if info["live"]:
                    prefix = ""
                else:
                    prefix = "test_"
                for key in info.keys():
                    if key not in ["key"]:
                        result[key] = info[key]
                result["date"] = datetime.now()
                comet_roster.store(f"{prefix}trade_params",pd.DataFrame([result]))
                complete = result
            else:
                complete = {}
        else:
            complete = {}
        comet_roster.disconnect()
    except Exception as e:
        complete = {"roster":[],"errors":str(e)}
    return JsonResponse(complete,safe=False)