import requests
import json
import traceback
import os.path

class DataStore():
    def download_data(self, path, symbols, override=False):
        for symbol in symbols:
            self.download_data_by_stock(path, symbol, override)

    def download_data_by_stock(self, path, symbol, override=False):
        api_symbol = symbol
        if api_symbol == "SPXW":
            api_symbol = "SPY"
        if api_symbol == "RUTW" or api_symbol =="RUT":
            api_symbol = "IWM"
        
        url = "https://api.iextrading.com/1.0/stock/{}/chart/5y".format(api_symbol)
        try:
            r = requests.get(url)
            rj = r.json()
            file_path = "{}\{}.json".format(path, symbol)
            if not os.path.exists(file_path) or override:
                with open(file_path, "w+") as outfile:
                    json.dump(rj, outfile)
                    print "Created {}".format(outfile)
            else:
                print "{} exist".format(file_path)
        except:
            print "Can't download {} with response {}".format(symbol, r)
            
#"volume": 82255544, "changeOverTime": -0.009828976361490719, "changePercent": 1.554, "label": "Jan 21, 14", "high": 72.1199, "low": 70.8547, "date": "2014-01-21", "close": 71.9888, "vwap": 71.6677, "open": 70.9294, "unadjustedVolume": 11750792, "change": 1.1013
    def get_data_from_json(self, path, symbol, range):
        file_path = "{}\{}.json".format(path, symbol)
        days = None
        with open(file_path) as f:
            days = json.load(f)
        return days[-range:]
    
    def  get_history_from_json(self, path, symbol):
        file_path = "{}\{}_history.json".format(path, symbol)
        history = None
        with open(file_path) as f:
            history = json.load(f)
        return history