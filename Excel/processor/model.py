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
        print "date: {} symobol: {} action: {} price: {} quantity: {} type: {} amount: {}".format(self.date, self.symbol, self.action, self.price, self.quantity, self.type, self.amount)
        
        
class Stock():
    def __init__(self):
        self.cost = None
        self.current = None;
        self.number = None;
        
class Holding():
    def __init__(self):
        self.stocks = []