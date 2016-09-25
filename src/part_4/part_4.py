import os  # os for directory interaction
import time  # time information
from datetime import datetime  # date information

path = "../../data/intraQuarter"  # location of data from part 3


def Key_Stats(gather="Total Debt/Equity (mrq)"):
    """
    Try to collect debt/equity ratio
    :param gather:
    :return:
    """
    statspath = path + '/_KeyStats'  # path to stats directory
    stock_list = [x[0] for x in os.walk(statspath)]  # list all contents in dir
    # print(stock_list)

    for each_dir in stock_list[1:]:  # go through every dir (each ticker)
        each_file = os.listdir(each_dir)  # list each file in that stock's dir
        if len(each_file) > 0:  # dir not empty
            for file in each_file:
                # files are stored under their ticker with a file name of the date and time their information was pulled
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')  # get date_stamp for each file
                unix_time = time.mktime(date_stamp.timetuple())  # convert date-time to unix timestamp
                print(date_stamp, unix_time)
                # time.sleep(15)


Key_Stats()
