from database.adatabase import ADatabase
import pandas as pd

class CometRoster(ADatabase):
    
    def __init__(self,mongouser,mongokey):
        super().__init__("comet_roster",mongouser,mongokey)
    
    def get_user_trade_params(self,version,user):
        try:
            db = self.client[self.name]
            table = db[f"{version}_trading_params"]
            data = table.find({"username":user},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def get_secrets(self,user):
        try:
            db = self.client[self.name]
            table = db["coinbase_credentials"]
            data = table.find({"username":user},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def update_roster(self,user,params):
        try:
            db = self.client[self.name]
            table = db["roster"]
            data = table.update_one({"username":user},{"$set":params})
            return data
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def get_bot_status(self,user):
        try:
            db = self.client[self.name]
            table = db["roster"]
            data = table.find({"username":user},{"_id":0},show_record_id=False)
            return data
        except Exception as e:
            print(self.name,"fills",str(e))
    