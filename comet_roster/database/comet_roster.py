from database.adatabase import ADatabase
import pandas as pd

class CometHistorian(ADatabase):
    
    def __init__(self,mongouser,mongokey):
        super().__init__("comet_roster",mongouser,mongokey)
    
    def get_user_trade_params(self,user):
        try:
            db = self.client[self.name]
            table = db["trade_params"]
            data = table.find({"username":user},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    
    def get_user_test_trade_params(self,user):
        try:
            db = self.client[self.name]
            table = db["test_trade_params"]
            data = table.find({"username":user},{"_id":0},show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.name,"fills",str(e))
    