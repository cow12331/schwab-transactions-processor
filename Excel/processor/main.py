import excel
import analyst
import processor.data
import traceback
import chart

if __name__ == '__main__':
    excelProcessor = excel.ExcelProcessor()
    dataStore = processor.data.DataStore()
    #transactions = excelProcessor.process("F:\Download\XXXX5163_Transactions_20181228-172604.CSV")
    
    #stock_dict = analyst.get_stock_dict(transactions)
    #dataStore.download_data("I:\workspace\schwab-transactions-processor\Excel\data", stock_dict.keys(), override=False)
    
    #analyst.create_transaction_json("I:\workspace\schwab-transactions-processor\Excel\data", transactions, override=True)
      
#     for k in analyst.get_max_profit_map(transactions):
#         try:
#             print "{}".format(k)
#             c = chart.Chart()
#             stock = k[0]
#             days = dataStore.get_data_from_json("I:\workspace\schwab-transactions-processor\Excel\data", stock, 700)
#             history = dataStore.get_history_from_json("I:\workspace\schwab-transactions-processor\Excel\data", stock)
#             c.draw_kline(days, history, "I:\workspace\schwab-transactions-processor\Excel\charts\{}.html".format(stock))
#         except Exception:
#             traceback.print_exc()
#             pass
    
        #robinhood
    transactions = dataStore.get_robinhood_transactions("F:\\Download\\robinhoodhistory")
    stock_dict = analyst.get_stock_dict(transactions)
    dataStore.download_data("I:\workspace\schwab-transactions-processor\Excel\data", stock_dict.keys(), override=False)
    analyst.create_transaction_json(r"I:\workspace\schwab-transactions-processor\Excel\data\robinhood", transactions, override=True)
    for k in analyst.get_max_profit_map(transactions):
        try:
            print "{}".format(k)
            c = chart.Chart()
            stock = k[0]
            days = dataStore.get_data_from_json("I:\workspace\schwab-transactions-processor\Excel\data", stock, 700)
            history = dataStore.get_history_from_json(r"I:\workspace\schwab-transactions-processor\Excel\data\robinhood", stock)
            c.draw_kline(days, history, r"I:\workspace\schwab-transactions-processor\Excel\charts\robinhood\{}.html".format(stock))
        except Exception:
            traceback.print_exc()
            pass