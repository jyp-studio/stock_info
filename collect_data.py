#%%
import yfinance as yf
from pandas_datareader import data
from datetime import datetime
from setting import PATH
import os

# override yf as pandas_datareader's format
yf.pdr_override()


def collect_stock(target, start, end):
    """
    First find if the stock data is exist or not,
    if the data is not exist, then get it from yf.
    """
    t_name = target.replace(".", "")
    s_name = ""
    e_name = ""
    for i in range(3):
        s_name += str(start[i]).zfill(2)
        e_name += str(end[i]).zfill(2)
    # define path
    path = PATH
    # if directory is not exist, make one
    if not os.path.isdir(path):
        os.mkdir(path)
    filename = os.path.join(path, f"{t_name}_{s_name}_{e_name}.csv")

    if not os.path.isfile(filename):
        # define date
        start_date = datetime(start[0], start[1], start[2])
        end_date = datetime(end[0], end[1], end[2])
        # put data into dataframe
        df = data.get_data_yahoo([target], start_date, end_date)
        # df.reset_index(inplace=True)
        # define filename and save it
        df.to_csv(filename)
    else:
        print("file exist")


# %%
