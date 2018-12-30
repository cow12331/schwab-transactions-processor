import os
import json

def get_max_profit_map(transactions):
    dict = {}
    for t in transactions:
        if t.symbol in dict:
            dict[t.symbol] = dict[t.symbol] + t.amount
        else:
            dict[t.symbol] = t.amount
    return sorted(dict.iteritems(), key=lambda (k,v) : (v,k))

def get_stock_dict(transactions):
    dict = {}
    for t in transactions:
        if t.symbol in dict:
            dict[t.symbol].append(t)
        else:
            dict[t.symbol] = []
            dict[t.symbol].append(t)
    return dict

def create_transaction_json(path, transactions, override=False):
    dict = get_stock_dict(transactions)
    for k, v in dict.iteritems():
        items = []
        for transaction in v:
            item = {}
            file_path = "{}\{}_history.json".format(path, transaction.symbol)
            item["date"] = transaction.date
            item["symbol"] = transaction.symbol
            item["action"] = transaction.action.value
            item["price"] = transaction.price
            item["quantity"] = transaction.quantity
            item["type"] = transaction.type
            item["description"] = transaction.description
            item["mark"] = transaction.mark.value
            item["real_price"] = transaction.real_price
            items.append(item)
            
        if not os.path.exists(file_path) or override:
            with open(file_path, "w+") as outfile:
                json.dump(items, outfile)
                print "Created {}".format(outfile)
        else:
            print "{} exist".format(file_path)