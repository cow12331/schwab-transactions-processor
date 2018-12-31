from action import Attitude, Action

stock_dict = {""}
class Transaction():
    def __init__(self):
        self.date = None
        self.symbol = None
        self.action = None
        self.price = None
        self.quantity = None
        self.type = None
        self.amount = None
        self.description = None
        self.mark = None
        self.real_price = None
        
    def output(self):
        print "date: {} symobol: {} action: {} price: {} quantity: {} type: {} amount: {} description: {}, mark: {}, real_price: {}".format(self.date, self.symbol, self.action, self.price, self.quantity, self.type, self.amount, self.description, self.mark, self.real_price)
        
    def find_mark(self): 
        if self.type == "PUT":
            if self.action == Action.SELL_TO_OPEN or self.action == Action.SELL_TO_CLOSE:
                self.mark = Attitude.BULL
            elif self.action == Action.BUY_TO_OPEN or self.action == Action.BUY_TO_CLOSE:
                self.mark = Attitude.BEAR
            else:
                self.mark = Attitude.UNKNOWN
        elif self.type == "CALL":
            if self.action == Action.SELL_TO_OPEN or self.action == Action.SELL_TO_CLOSE:
                self.mark = Attitude.BEAR
            elif self.action == Action.BUY_TO_OPEN or self.action == Action.BUY_TO_CLOSE:
                self.mark = Attitude.BULL
            else:
                self.mark = Attitude.UNKNOWN
        elif self.type == "STOCK":
            if self.action == Action.BUY:
                self.mark = Attitude.BULL
            elif self.action == Action.SELL or self.action == Action.SELL_SHORT:
                self.mark = Attitude.BEAR
            else:
                self.mark = Attitude.UNKNOWN   
        else:
            self.mark = Attitude.UNKNOWN
            print "unknown option type {}".format(self.output())