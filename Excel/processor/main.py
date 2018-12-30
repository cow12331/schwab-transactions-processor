import excel
import analyst
import processor.data
import action
import chart

if __name__ == '__main__':
    excelProcessor = excel.ExcelProcessor()
    dataStore = processor.data.DataStore()
    #transactions = excelProcessor.process("F:\Download\XXXX5163_Transactions_20181228-172604.CSV")
#     for k in analyst.get_max_profit_map(transactions):
#         print "{}".format(k)
#    stock_dict = analyst.get_stock_dict(transactions)
#    dataStore.download_data("I:\workspace\schwab-transactions-processor\Excel\data", stock_dict.keys(), override=False)
    
    #analyst.create_transaction_json("I:\workspace\schwab-transactions-processor\Excel\data", transactions, override=True)
    
    stock = "NVDA"
    days = dataStore.get_data_from_json("I:\workspace\schwab-transactions-processor\Excel\data", stock, 700)
    history = dataStore.get_history_from_json("I:\workspace\schwab-transactions-processor\Excel\data", stock)
    c = chart.Chart()
    c.draw_kline(days, history)