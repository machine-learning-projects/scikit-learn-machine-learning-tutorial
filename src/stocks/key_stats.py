from matplotlib import style

style.use('dark_background')
import pandas as pd
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import re

path = "../../data/input/intraQuarter"  # location of data from part 3


def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'  # path to stats directory
    stock_list = [x[0] for x in os.walk(statspath)]  # list all contents in dir
    # print(stock_list)
    # store the creation of a new "DataFrame" object from Pandas,
    # where we specify the columns to be date, unix, ticker, and DE ratio
    df = pd.DataFrame(
        columns=['Date',
                 'Unix',
                 'Ticker',
                 'DE Ratio',
                 'Price',
                 'stock_p_change',
                 'SP500',
                 'sp500_p_change',
                 'Difference',  # difference between stock and market
                 'Status'])  # stock's performance
    sp500_df = pd.DataFrame.from_csv("../../data/input/YAHOO-INDEX_GSPC.csv")

    ticker_list = []

    for each_dir in stock_list[1:25]:  # go through every dir (each ticker)
        each_file = os.listdir(each_dir)  # list each file in that stock's dir
        ticker = each_dir.split("\\")[1]  # windows needs double back slashes
        ticker_list.append(ticker)

        # Want to calculate % change as we go
        # Need to start over with the % change each time the stock changes
        starting_stock_value = False
        starting_sp500_value = False

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
                    try:
                        # redefine DataFrame object as the previous DataFrame object with the new data appended to it
                        value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except:
                        value = float(
                            source.split(gather + ':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])

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
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                        # print("stock_price:",stock_price,"ticker:", ticker)
                    except:
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            # print(stock_price)

                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)

                            stock_price = float(stock_price.group(1))
                            # print(stock_price)
                        except:
                            try:
                                stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                                # print(stock_price)

                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)

                                stock_price = float(stock_price.group(1))
                                # print(stock_price)

                            except:
                                print("stock price", ticker, file, value)

                    # set starting value if there isn't one
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    # calculate % change (new - old) / old * 100
                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    location = len(df['Date'])

                    difference = stock_p_change - sp500_p_change
                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"

                    df = df.append({'Date': date_stamp,
                                    'Unix': unix_time,
                                    'Ticker': ticker,
                                    'DE Ratio': value,
                                    'Price': stock_price,
                                    'stock_p_change': stock_p_change,
                                    'SP500': sp500_value,
                                    'sp500_p_change': sp500_p_change,
                                    ############################
                                    'Difference': difference,
                                    'Status': status},
                                   ignore_index=True)

                except Exception as e:
                    # print(ticker,e,file, value)
                    pass

    # print(ticker_list)
    # print(df)

    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]

            plot_df = plot_df.set_index(['Date'])

            if plot_df['Status'][-1] == 'underperform':
                color = 'r'
            else:
                color = 'g'

            plot_df['Difference'].plot(label=each_ticker, color=color)
            plt.legend()
        except Exception as e:
            print(str(e))

    plt.show()

    # specify custom name for the csv file
    # then using pandas to_csv capability to output the Data Frame to an actual CSV file
    save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv("../../data/output/" + save)


Key_Stats()
