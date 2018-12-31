import requests
import json
import traceback
import os.path
import processor.model
import processor.action

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
        
    def get_robinhood_transactions(self, path):
    # "Date","Action","Symbol","Description","Quantity","Price","Fees & Comm","Amount",
        transactions = []
        with open(path) as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                if "Dividend" in lines[i] or "Deposit" in lines[i]:
                    i += 3
                    continue
                if "Canceled" in lines[i + 2] or "Failed" in lines[i + 2]:
                    i += 3
                    continue;
                items0 = lines[i].split(" ")
                symbol = items0[0]
                type = "STOCK"
                if "Call" in lines[i]:
                    type = "CALL"
                elif "Put" in lines[i]:
                    type = "PUT"
                if "Buy" in lines[i]:
                    if type == "STOCK":
                        action = "Buy"
                    else:
                        action = "Buy to Open"
                elif "Sell" in lines[i]:
                    if type == "STOCK":
                        action = "Sell"
                        mark = processor.action.Attitude.BEAR
                    else:
                        action = "Sell to Close"
                elif "Expiration" in lines[i]:
                    action = "Expired"
                else:
                    print "Found unknown line: {}".format(lines[i])
                    
                description = lines[i]
                
                date = self._from_rdate_date(lines[i + 1])
                
                amount = float(lines[i + 2].replace("$", "").replace(",", ""))
                if "Buy" in action:
                    amount *= -1
                items3 = lines[i + 3].split(" ")
                if action != "Expired":
                    quantity = items3[0]
                else:
                    quantity = "0"
                    
                price = items3[-1].replace("$", "")
                
                transaction = processor.model.Transaction()
                transaction.symbol = symbol.strip()
                transaction.action = processor.action.Action(action)
                transaction.amount = amount
                transaction.date = date.strip()
                transaction.description = description.strip()
                transaction.quantity = quantity.strip()
                transaction.type = type.strip()
                transaction.find_mark()
                transaction.real_price = price.strip()
                transaction.price = price.strip()
                if type != "STOCK":
                    transaction.real_price = float(items0[1].replace("$", "").replace(",", ""))
                transaction.output()
                transactions.append(transaction)
                if action == "Expired":
                    i += 3
                else:
                    i += 4
        return transactions
            
    def _from_rdate_date(self, line):
        line = line.replace(",", "")
        items = line.split(" ")
        year = "2018"
        month_dict = {"Dec":"12", "Nov":"11","Oct":"10","Sep":"09","Aug":"08","Jul":"07","Jun":"06","May":"05","Apr":"04","Mar":"03","Feb":"02","Jan":"01",}
        day_dict = {"1":"01","2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":"09"}
        if "2017" in line:
            year = "2017"
        month = month_dict[items[0]]
        day = items[1]
        if day in day_dict:
            day = day_dict[day]
        return "{}{}{}".format(year, month, day)