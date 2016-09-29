import os
import time
from datetime import datetime

path = "../../data/intraQuarter"  # location of data from part 3


# same as part 4
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        # added ticker variable
        ticker = each_dir.split("\\")[1]  # windows needs double back slashes
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                # print(date_stamp, unix_time)

                full_file_path = each_dir + '/' + file  # access the file
                print(full_file_path)
                source = open(full_file_path, 'r').read()  # save full source code HTML contents to source variable
                # print(source)
                #search for "gather" term - feature we want
                #split by opening and closing table data tags
                value = source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
                print(ticker + ":", value)

            time.sleep(15)


Key_Stats()
