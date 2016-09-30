import os  # os for directory interaction
import time  # time information
from datetime import datetime  # date information

import pandas as pd

path = "../../data/input/intraQuarter"  # location of data from part 3


def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'  # path to stats directory
    stock_list = [x[0] for x in os.walk(statspath)]  # list all contents in dir
    # print(stock_list)
    # store the creation of a new "DataFrame" object from Pandas,
    # where we specify the columns to be date, unix, ticker, and DE ratio
    df = pd.DataFrame(columns=['Date', 'Unix', 'Ticker', 'DE Ratio'])
    sp500_df = pd.DataFrame.from_csv("../../data/input/YAHOO-INDEX_GSPC.csv")

    for each_dir in stock_list[1:25]:  # go through every dir (each ticker)
        each_file = os.listdir(each_dir)  # list each file in that stock's dir
        ticker = each_dir.split("\\")[1]  # windows needs double back slashes
        if len(each_file) > 0:  # dir not empty
            for file in each_file:
                # files are stored under their ticker with a file name of the date and time their information was pulled
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')  # get date_stamp for each file
                unix_time = time.mktime(date_stamp.timetuple())  # convert date-time to unix timestamp
                # print(date_stamp, unix_time)

                full_file_path = each_dir + '/' + file  # access the file
                # print(full_file_path)

                source = open(full_file_path, 'r').read()  # save full source code HTML contents to source variable
                # print(source)
                # search for "gather" term - feature we want
                # split by opening and closing table data tags
                try:
                    # redefine DataFrame object as the previous DataFrame object with the new data appended to it
                    value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    # print(ticker + ":", value)

                    # try-catch because some data may have been pulled on weekend, where S&P dataset is not complete
                    try:
                        # hunting for the value of the S&P 500 index at the same time as the date for our stock file
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])

                    # stock price to compare to S&P value
                    stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])

                    df = df.append({'Date': date_stamp,
                                    'Unix': unix_time,
                                    'Ticker': ticker,
                                    'DE Ratio': value,
                                    'Price': stock_price,
                                    'SP500': sp500_value}, ignore_index=True)

                except Exception as e:
                    pass

    # specify custom name for the csv file
    # then using pandas to_csv capability to output the Data Frame to an actual CSV file
    save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv("../../data/output/" + save)


Key_Stats()
