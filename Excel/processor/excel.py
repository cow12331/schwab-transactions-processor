import csv
import model
from action import Action, Attitude

class ExcelProcessor:
    def process(self, location): 
        result = []
        with open(location) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                if self.is_stock_action(row):
                    transcation = model.Transaction()
                    transcation.date = self.get_date(row)
                    transcation.symbol = self.get_symbol(row)
                    transcation.quantity = self.get_quantity(row)
                    transcation.price = self.get_price(row)
                    transcation.amount = self.get_amount(row)
                    transcation.description = self.get_description(row)
                    transcation.action = Action(row[1])
                    
                    if self.is_option(row):
                        if "PUT" in transcation.description:
                            transcation.type = "PUT"
                            if transcation.action == Action.SELL_TO_OPEN or transcation.action == Action.SELL_TO_CLOSE:
                                transcation.mark = Attitude.BULL
                            elif transcation.action == Action.BUY_TO_OPEN or transcation.action == Action.BUY_TO_CLOSE:
                                transcation.mark = Attitude.BEAR
                            else:
                                transcation.mark = Attitude.UNKNOWN
                        elif "CALL" in transcation.description:
                            transcation.type = "CALL"
                            if transcation.action == Action.SELL_TO_OPEN or transcation.action == Action.SELL_TO_CLOSE:
                                transcation.mark = Attitude.BEAR
                            elif transcation.action == Action.BUY_TO_OPEN or transcation.action == Action.BUY_TO_CLOSE:
                                transcation.mark = Attitude.BULL
                            else:
                                transcation.mark = Attitude.UNKNOWN
                        else:
                            print "unknown option type {}".format(row)
                        transcation.real_price = float(self.get_real_price(row))
                    else:
                        transcation.type = "STOCK"
                        if transcation.action == Action.BUY:
                            transcation.mark = Attitude.BULL
                        elif transcation.action == Action.SELL or transcation.action == Action.SELL_SHORT:
                            transcation.mark = Attitude.BEAR
                        else:
                            transcation.mark = Attitude.UNKNOWN
                        transcation.real_price = transcation.price
                    #transcation.output()
                    result.append(transcation)
                else:
                    print "unknow row: {}".format(row)
        return result
            
    def get_date(self, row):
        date_str = row[0]
        date_str = date_str[0:10]
        return "{}{}{}".format(date_str[6:10], date_str[0:2], date_str[3:5]) 
    
    def get_quantity(self, row):
        return row[4]
    
    def get_description(self, row):
        return row[3]
    
    def get_amount(self, row):
        amount = row[7].replace("$", "")
        if amount == "":
            return 0
        else:    
            return float(amount)
        
    def get_price(self, row):
        return row[5][1:]
        
    def get_symbol(self, row):
        return row[2].split(" ")[0]

    def get_real_price(self, row):
        return row[2].split(" ")[2]
    
    def is_stock_action(self, row):
        try:
            action = row[1]
            if action in {"Buy", "Sell", "Assigned", "Exchange or Exercise", "Expired", "Sell to Open", "Buy to Open", "Buy to Close", "Sell to Close", "Sell Short"}:
                return True
            else:
                return False
        except:
            return False
        
    def is_option(self, row):
        action = row[1]
        if action in {"Assigned", "Exchange or Exercise", "Expired", "Sell to Open", "Buy to Open", "Buy to Close", "Sell to Close"}:
            return True
        else:
            return False