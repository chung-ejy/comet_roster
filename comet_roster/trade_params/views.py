from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
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
                trade_params = comet_roster.get_user_trade_params(version,user)
                trade_params["date"] = pd.to_datetime(trade_params["date"])
                trade_params.sort_values("date",ascending=False,inplace=True)
                complete = {f"trade_params":trade_params.to_dict("records")[0]}
            else:
                complete = {"trade_params":{},"errors":"incorrect key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "UPDATE":
            complete = {}
        elif request.method == "POST":
            info = json.loads(request.body.decode("utf-8"))
            if header_key == key:
                version = info["version"]
                info["date"] = datetime.now()
                comet_roster.store(f"{version}_trading_params",pd.DataFrame([info]))
                complete = info
            else:
                complete = {}
        else:
            complete = {}
        comet_roster.disconnect()
    except Exception as e:
        complete = {"roster":[],"errors":str(e)}
    return JsonResponse(complete,safe=False)