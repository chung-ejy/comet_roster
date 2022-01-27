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
            data_request = request.GET.get("data_request")
            if header_key == key:
                if data_request == "bot_status":
                    user = request.GET.get("username")
                    bot_status = comet_roster.get_bot_status(user)
                    complete = {"bot_status":bot_status.to_dict("records")[0]}
                else:
                    roster = comet_roster.retrieve("roster")
                    complete = {"roster":roster.to_dict("records")}
            else:
                complete = {"errors":"incorrect key"}
        elif request.method == "DELETE":
            complete = {}
        elif request.method == "PUT":
            if header_key == key:
                info = json.loads(request.body.decode("utf-8"))
                user = info["username"]
                if info["data_request"] == "keys":
                    update = comet_roster.update_roster(user,info)
                    info["acknowledge"] = update.acknowledged
                    complete = info[["username","acknowledge"]]
                elif info["data_request"] == "bot_status":
                    update = comet_roster.update_roster(user,info)
                    info["acknowledge"] = update.acknowledged
                    complete = info
            else:
                complete = {"error":"wrong key"}
        elif request.method == "POST":
            info = json.loads(request.body.decode("utf-8"))
            if header_key == key:
                result = {}
                result["username"] = info["username"]
                result["live"] = False
                result["test"] = False
                keys = {}
                keys["username"] = info["username"]
                keys["apikey"] = ""
                keys["passphrase"] = ""
                keys["secret"] = ""
                keys["adnboxapikey"] = ""
                keys["sandboxpassphrase"] = ""
                keys["sandboxsecret"] = ""
                trade_params = {
                    "signal":5
                    ,"req":5
                    ,"retrack_days":1
                    ,"value":True,
                    "conservative":False,
                    "entry_strategy":"standard"
                    ,"exit_strategy":"hold"
                    ,"positions":5
                    ,"username":info["username"]
                    ,"version":"live"
                    ,"whitelist_symbols":["BTC","ETH"]
                }
                test_trade_params = {
                    "signal":5
                    ,"req":5
                    ,"retrack_days":1
                    ,"value":True,
                    "conservative":False,
                    "entry_strategy":"standard"
                    ,"exit_strategy":"hold"
                    ,"positions":5
                    ,"username":info["username"]
                    ,"version":"live"
                    ,"whitelist_symbols":["BTC"]
                }
                comet_roster.store("roster",pd.DataFrame([result]))
                comet_roster.store("coinbase_credentials",pd.DataFrame([keys]))
                comet_roster.store("live_trading_params",pd.DataFrame([trade_params]))
                comet_roster.store("test_trading_params",pd.DataFrame([test_trade_params]))
                complete = result
            else:
                complete = {}
        else:
            complete = {}
        comet_roster.disconnect()
    except Exception as e:
        complete = {"roster":[],"errors":str(e)}
    return JsonResponse(complete,safe=False)