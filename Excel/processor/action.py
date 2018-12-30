import enum

class Action(enum.Enum):
    BUY = "Buy"
    SELL = "Sell"
    ASSIGNED = "Assigned"
    EXCHANGE_OR_EXERCISE = "Exchange or Exercise"
    EXPIRED = "Expired"
    SELL_TO_OPEN = "Sell to Open"
    BUY_TO_OPEN = "Buy to Open"
    BUY_TO_CLOSE = "Buy to Close"
    SELL_TO_CLOSE = "Sell to Close"
    SELL_SHORT = "Sell Short"
    
class Attitude(enum.Enum):
    BULL = "BULL"
    BEAR = "BEAR"
    UNKNOWN = "UNKNOWN"