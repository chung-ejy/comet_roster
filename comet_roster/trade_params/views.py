from django.shortcuts import render
from django.http.response import JsonResponse
import pickle
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import requests
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
        header_key = request.headers["x-api-key"]
        if request.method == "GET":
            user = request.GET.get("username")
            version = request.GET.get("version")
            if key == header_key:
                if version == "live":
                    prefix = ""
                    trade_params = comet_roster.get_user_trade_params(user)
                else:
                    prefix = "test_"
                    trade_params = comet_roster.get_user_test_trade_params(user)
                trade_params["date"] = pd.to_datetime(trade_params["date"])
                trade_params.sort_values("date",inplace=True)
                complete = {f"trade_params":trade_params.to_dict("records")[0]}
            else:
                complete = {"roster":[],"errors":"incorrect key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            info = json.loads(request.body.decode("utf-8"))
            if header_key == key:
                result = {}
                if info["version"]=="live":
                    prefix = ""
                else:
                    prefix = "test_"
                for info_key in info.keys():
                    if key not in ["key","version"]:
                        result[info_key] = info[info_key]
                result["date"] = datetime.now()
                comet_roster.store(f"{prefix}trading_params",pd.DataFrame([result]))
                complete = result
            else:
                complete = {}
        else:
            complete = {}
        comet_roster.disconnect()
    except Exception as e:
        complete = {"roster":[],"errors":str(e)}
    return JsonResponse(complete,safe=False)