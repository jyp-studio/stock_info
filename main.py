#%%
import tkinter as tk
from tkinter import PhotoImage, ttk
import matplotlib
import pandas as pd
import datetime
from setting import WIDTH, HEIGHT, ICONPATH, PATH
import os

# %%
# define windows
win = tk.Tk()
# define caption
win.title("Stock info")
# set icon
photo = PhotoImage(file=ICONPATH)
win.iconphoto(False, photo)
# win.iconbitmap("./icon/stock_bmp.bmp")
# define size (WIDTH * HEIGHT)
win.geometry(f"{WIDTH}x{HEIGHT}")
# %%
"""frame_init
to get user input:
stock name, start and end time...
"""
# label
frame_init = tk.Frame(win)
target_label = tk.Label(frame_init, text="Target stock:", font=("Arial", 14))
start_label = tk.Label(frame_init, text="Start time:", font=("Arial", 14))
end_label = tk.Label(frame_init, text="End time:", font=("Arial", 14))
maximun_label = tk.Label(frame_init, text="Maximun:", font=("Arial", 14))
cash_label = tk.Label(frame_init, text="Cash:", font=("Arial", 14))
commission_label = tk.Label(frame_init, text="Commission:", font=("Arial", 14))
ma1_label = tk.Label(frame_init, text="MA1(short):", font=("Arial", 14))
ma2_label = tk.Label(frame_init, text="MA2(long):", font=("Arial", 14))

# text input
target_text = tk.Text(frame_init, width=15, height=2)
start_text = tk.Text(frame_init, width=15, height=2)
end_text = tk.Text(frame_init, width=15, height=2)
maximum_text = tk.Text(frame_init, width=15, height=2)
cash_text = tk.Text(frame_init, width=15, height=2)
commission_text = tk.Text(frame_init, width=15, height=2)
ma1_text = tk.Text(frame_init, width=15, height=2)
ma2_text = tk.Text(frame_init, width=15, height=2)

# get current year
current_time = datetime.datetime.now()
current_year = current_time.date().strftime("%Y")

# combobox
start_y_box = ttk.Combobox(
    frame_init,
    values=[i for i in range(int(current_year) - 20, int(current_year) + 1)],
    state="readonly",
    font=("Arial", 14),
    width=4,
    height=10,
)
start_m_box = ttk.Combobox(
    frame_init,
    values=[i for i in range(1, 13)],
    state="readonly",
    font=("Arial", 14),
    width=2,
)
start_d_box = ttk.Combobox(
    frame_init,
    values=[i for i in range(1, 32)],
    state="readonly",
    font=("Arial", 14),
    width=2,
    height=10,
)
end_y_box = ttk.Combobox(
    frame_init,
    values=[i for i in range(int(current_year) - 20, int(current_year) + 1)],
    state="readonly",
    font=("Arial", 14),
    width=4,
    height=10,
)
end_m_box = ttk.Combobox(
    frame_init,
    values=[i for i in range(1, 13)],
    state="readonly",
    font=("Arial", 14),
    width=2,
)
end_d_box = ttk.Combobox(
    frame_init,
    values=[i for i in range(1, 32)],
    state="readonly",
    font=("Arial", 14),
    width=2,
    height=10,
)
maximum_box = ttk.Combobox(
    frame_init,
    values=["Equity Final [$]", "SQN", "Sharpe Ratio", "Sortino Ratio", "Calmar Ratio"],
    state="readonly",
    font=("Arial", 14),
    width=12,
)
#%%
"""Threading
do multi-threading in order to maintain mainloop
when collecting stock's data on the Internet
"""
import threading


def thread(func, *args):
    # make a thread
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)  # make it daemon
    t.start()  # start it


# %%
"""
import collect stock data
and testing module
"""
from collect_data import *
from testing import *

#%%
# optimize test
def opt_test(
    stock,
    start,
    end,
    maximize,
    commission,
    cash,
    ma1,
    ma2,
):
    # path
    t_name = stock.replace(".", "")
    s_name = ""
    e_name = ""
    for i in range(3):
        s_name += str(start[i]).zfill(2)
        e_name += str(end[i]).zfill(2)
    path = PATH
    filename = os.path.join(path, f"{t_name}_{s_name}_{e_name}.csv")
    # read data
    df = pd.read_csv(filename, index_col=0)
    # if there're missing data, do interpolation
    df = df.interpolate()
    df.index = pd.to_datetime(df.index)
    """
    test data
    Backtest(data, strategy, cash, commission)
    """
    # change n1 and n2
    SmaCross.n1 = ma1
    SmaCross.n2 = ma2
    print("SMA:", SmaCross.n1, SmaCross.n2)
    test = Backtest(df, SmaCross, cash=cash, commission=commission)
    # %%
    result = test.run()
    """optimize
    n1: short MA start from 5 to 50, increase 5 everytime. 
    n2: long MA start from 10 to 120, increase 5 everytime.
    maximize: target is the max finace.
    constraint: only compute when n1 < n2.
    """
    opt_result = test.optimize(
        n1=range(5, 50, 5),
        n2=range(10, 120, 5),
        maximize=maximize,
        constraint=lambda p: p.n1 < p.n2,
    )
    return result, opt_result


#%%
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

matplotlib.use("Agg")

# graph
def draw_graph(stock, start, end):
    # path
    t_name = stock.replace(".", "")
    s_name = ""
    e_name = ""
    for i in range(3):
        s_name += str(start[i]).zfill(2)
        e_name += str(end[i]).zfill(2)
    path = PATH
    filename = os.path.join(path, f"{t_name}_{s_name}_{e_name}.csv")
    df = pd.read_csv(filename, parse_dates=True, index_col=0)
    # draw
    market_color = mpf.make_marketcolors(up="r", down="g", inherit=True)
    style = mpf.make_mpf_style(base_mpf_style="yahoo", marketcolors=market_color)
    # keywords argument for ploting
    kwargs = dict(
        type="candle",
        mav=(5, 20, 60),
        volume=True,
        figratio=(10, 8),
        figscale=1,
        title=stock,
        style=style,
        returnfig=True,
    )
    frame_graph = tk.Frame(win)
    frame_graph.grid(row=1, column=0, pady=20)
    # clear frame_graph
    for widget in frame_graph.winfo_children():
        print(widget)
        widget.destroy()
    figure, _ = mpf.plot(df, **kwargs)
    canvas = FigureCanvasTkAgg(figure, master=frame_graph)
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, frame_graph)
    toolbar.update()
    canvas._tkcanvas.pack()


#%%
# button get
def get():
    # get text
    target_input = (target_text.get("1.0", "end-1c")).replace("\n", "").replace(" ", "")
    ma1_input = int((ma1_text.get("1.0", "end-1c")).replace("\n", "").replace(" ", ""))
    ma2_input = int((ma2_text.get("1.0", "end-1c")).replace("\n", "").replace(" ", ""))
    start_list = [start_y_box.get(), start_m_box.get(), start_d_box.get()]
    end_list = [end_y_box.get(), end_m_box.get(), end_d_box.get()]
    maximum_input = maximum_box.get()
    cash_input = int(
        (cash_text.get("1.0", "end-1c")).replace("\n", "").replace(" ", "")
    )
    commission_input = float(
        (commission_text.get("1.0", "end-1c")).replace("\n", "").replace(" ", "")
    )

    # format str to int in the list
    for i in range(3):
        start_list[i] = int(start_list[i])
        end_list[i] = int(end_list[i])
    """
    # progressing label
    frame_info = tk.Frame(frame_init)
    frame_info.grid(row=3, column=0, columnspan=10)
    # clear frame_info
    for widget in frame_info.winfo_children():
        widget.destroy()
    progress_label = tk.Label(frame_info, text="Progressing", font=("Arial", 20))
    progress_label.grid(row=0, column=0)
    """
    # search
    collect_stock(target_input, start_list, end_list)
    # draw frame, graph, and toolbar
    draw_graph(target_input, start_list, end_list)

    # testing
    result, opt_result = opt_test(
        stock=target_input,
        start=start_list,
        end=end_list,
        maximize=maximum_input,
        commission=commission_input,
        cash=cash_input,
        ma1=ma1_input,
        ma2=ma2_input,
    )
    # frame_strategy for compare original and optimze one
    frame_original = tk.Frame(win)
    frame_original.grid(row=0, column=1, rowspan=2, padx=25, sticky="n")
    # clear frame_priginal
    for widget in frame_original.winfo_children():
        print(widget)
        widget.destroy()
    original_label = tk.Label(
        frame_original, text="Original strategy", font=("Arial", 14)
    )
    original_label.grid(row=0, sticky="w")

    ori_counter = 1
    for key, value in result.items():
        if ori_counter < 29:
            ori_key_label = tk.Label(frame_original, text=key, font=("Arial", 14))
            ori_key_label.grid(row=ori_counter, column=0, sticky="w")
            ori_value_label = tk.Label(frame_original, text=value, font=("Arial", 14))
            ori_value_label.grid(row=ori_counter, column=1, sticky="e")
            ori_counter += 1
        else:
            break

    frame_opt = tk.Frame(win)
    frame_opt.grid(row=0, column=2, rowspan=2, padx=20, sticky="n")
    # clear frame_opt
    for widget in frame_opt.winfo_children():
        print(widget)
        widget.destroy()
    opt_label = tk.Label(frame_opt, text="Optimize strategy", font=("Arial", 14))
    opt_label.grid(row=0, sticky="w")

    opt_counter = 1
    for key, value in opt_result.items():
        if opt_counter < 29:
            opt_key_label = tk.Label(frame_opt, text=key, font=("Arial", 14))
            opt_key_label.grid(row=opt_counter, column=0, sticky="w")

            if value != result[key]:
                opt_value_label = tk.Label(
                    frame_opt, text=value, font=("Arial", 14), fg="#1E90FF"
                )
                opt_value_label.grid(row=opt_counter, column=1, sticky="e")
            else:
                opt_value_label = tk.Label(frame_opt, text=value, font=("Arial", 14))
                opt_value_label.grid(row=opt_counter, column=1, sticky="e")
            opt_counter += 1
        else:
            break
    """
    # progressing done label
    progress_label.grid_forget()
    done_label = tk.Label(frame_info, text="Done!", font=("Arial", 20))
    done_label.grid(row=0, column=0)
    """


# button
search_button = tk.Button(
    frame_init,
    text="Search",
    font=("Arial", 14),
    width=10,
    height=2,
    command=lambda: thread(get),
)


# %%
# grid
# frame_init
frame_init.grid(row=0, column=0, sticky="nw")
target_label.grid(row=0, column=0)
target_text.grid(row=0, column=1)

start_label.grid(row=0, column=2)
start_y_box.grid(row=0, column=3)
start_m_box.grid(row=0, column=4)
start_d_box.grid(row=0, column=5)
start_y_box.current(20)
start_m_box.current(0)
start_d_box.current(0)

end_label.grid(row=0, column=6)
end_y_box.grid(row=0, column=7)
end_m_box.grid(row=0, column=8)
end_d_box.grid(row=0, column=9)
end_y_box.current(20)
end_m_box.current(0)
end_d_box.current(0)

maximun_label.grid(row=1, column=0)
maximum_box.grid(row=1, column=1)
maximum_box.current(0)

cash_label.grid(row=1, column=2)
cash_text.grid(row=1, column=3, columnspan=3)
commission_label.grid(row=1, column=6)
commission_text.grid(row=1, column=7, columnspan=3)
ma1_label.grid(row=2, column=0)
ma1_text.grid(row=2, column=1)
ma2_label.grid(row=2, column=2)
ma2_text.grid(row=2, column=3, columnspan=3)
search_button.grid(row=2, column=7, columnspan=3, pady=5, sticky="e")

# %%
# mainloop
win.mainloop()
# %%
