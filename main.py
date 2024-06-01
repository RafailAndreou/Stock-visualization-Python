import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf


def plot_stock_data(symbol, start_date, end_date):
    # Fetching stock data
    stock_data = yf.download(symbol, start=start_date, end=end_date)

    # Plotting the closing prices
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data['Close'], label='Close Price', color='blue')
    ax.set_title(f'{symbol} Stock Closing Prices ({start_date} to {end_date})')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    ax.grid(True)

    return fig


def plot():
    symbol = symbol_var.get()
    start_date = start_date_var.get()
    end_date = end_date_var.get()

    try:
        plot_figure = plot_stock_data(symbol, start_date, end_date)
        plot_canvas = FigureCanvasTkAgg(plot_figure, master=plot_frame)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def on_start_date_select(event=None):
    start_date = cal_start.selection_get().strftime('%Y-%m-%d')
    start_date_var.set(start_date)


def on_end_date_select(event=None):
    end_date = cal_end.selection_get().strftime('%Y-%m-%d')
    end_date_var.set(end_date)


root = tk.Tk()
root.title("Stock Price Visualization")

# Main Frame
mainframe = ttk.Frame(root, padding="20")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.N, tk.E, tk.S))

# Stock Selection
ttk.Label(mainframe, text="Choose a stock:").grid(column=1, row=1, sticky=tk.W)
symbol_var = tk.StringVar()
symbol_combobox = ttk.Combobox(mainframe, textvariable=symbol_var, values=['AAPL', 'GOOG', 'MSFT', 'AMZN'])
symbol_combobox.grid(column=2, row=1, sticky=tk.W)

# Calendar for Start Date Selection
ttk.Label(mainframe, text="Start Date:").grid(column=1, row=2, sticky=tk.W)
start_date_var = tk.StringVar()
start_date_entry = ttk.Entry(mainframe, textvariable=start_date_var, state='readonly')
start_date_entry.grid(column=2, row=2, sticky=tk.W)
cal_start = Calendar(mainframe, selectmode='day', date_pattern='yyyy-mm-dd', command=on_start_date_select)
cal_start.grid(column=2, row=3, sticky=tk.W)
cal_start.bind("<<CalendarSelected>>", on_start_date_select)

# Calendar for End Date Selection
ttk.Label(mainframe, text="End Date:").grid(column=1, row=4, sticky=tk.W)
end_date_var = tk.StringVar()
end_date_entry = ttk.Entry(mainframe, textvariable=end_date_var, state='readonly')
end_date_entry.grid(column=2, row=4, sticky=tk.W)
cal_end = Calendar(mainframe, selectmode='day', date_pattern='yyyy-mm-dd', command=on_end_date_select)
cal_end.grid(column=2, row=5, sticky=tk.W)
cal_end.bind("<<CalendarSelected>>", on_end_date_select)

# Plot Button
plot_button = ttk.Button(mainframe, text="Plot", command=plot)
plot_button.grid(column=2, row=6, sticky=tk.W)

# Frame for Plot
plot_frame = ttk.Frame(root)
plot_frame.grid(column=1, row=0, sticky=(tk.W, tk.N, tk.E, tk.S))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
