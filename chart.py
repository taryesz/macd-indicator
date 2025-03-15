import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas

from signals import find_signals

def __create_history_chart(DATA: pandas.DataFrame, label: str, initial_capital: int) -> None:
    plt.plot(DATA["Date"], DATA["Close"], label=label, color="blue", linewidth=2.0)

    if initial_capital:
        plt.axhline(y=initial_capital, color="red", linestyle="--", label="Initial capital")


def __set_date_restrictions(DATA: pandas.DataFrame, start_date: str, end_date: str) -> pandas.DataFrame:

    data_filtered = DATA.copy()

    data_filtered["Date"] = pandas.to_datetime(data_filtered["Date"])

    if start_date:
        start_date = pandas.to_datetime(start_date)
        data_filtered = data_filtered[data_filtered["Date"] >= start_date]

    if end_date:
        end_date = pandas.to_datetime(end_date)
        data_filtered = data_filtered[data_filtered["Date"] <= end_date]

    return data_filtered


def __set_metadata(title: str, history: bool) -> None:

    plt.title(title, fontsize=10)
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.legend(loc="upper left", fontsize=10)
    plt.xlabel("Date", fontsize=10)
    plt.ylabel("Close" if history else "MACD", fontsize=10)
    plt.tight_layout()
    plt.show()


def create_chart(DATA: pandas.DataFrame, 
                 MACD: pandas.Series = None, 
                 SIGNAL: pandas.Series = None, 
                 title: str = "", 
                 start_date: str = None, 
                 end_date: str = None, 
                 history: bool = False,
                 buy_date: str = None,  
                 sell_date: str = None,
                 history_label: str = "EUR price in UAH",
                 initial_capital: int = None
                 ) -> None:

    # Show only specifically determined part of the data, timewise
    data_filtered = __set_date_restrictions(DATA, start_date, end_date)

    # Create a window
    plt.figure(figsize=(12, 6))

    # If creating a history chart ...
    if history:

        __create_history_chart(data_filtered, history_label, initial_capital)

        # If Buy/Sell signals wanted on this chart ...
        if MACD is not None and SIGNAL is not None:

            find_signals(MACD, SIGNAL, data_filtered, data_filtered["Close"])

    # If creating a MACD/SIGNAL chart ...
    else:

        if MACD is not None and SIGNAL is not None:
            
            # Add the values to the chart
            plt.plot(data_filtered["Date"], MACD.loc[data_filtered.index], label='MACD', color="blue", linewidth=2.0)
            plt.plot(data_filtered["Date"], SIGNAL.loc[data_filtered.index], label='SIGNAL', color="orange", linewidth=2.0)

            find_signals(MACD, SIGNAL, data_filtered, MACD.loc[data_filtered.index])

    # Add signatures to the chosen signals
    if buy_date:

        buy_date = pandas.to_datetime(buy_date)
        buy_point = data_filtered[data_filtered["Date"] == buy_date]

        if not buy_point.empty:

            buy_value = buy_point["Close"].values[0] if history else MACD.loc[buy_point.index].values[0]
            
            plt.scatter(buy_date, buy_value, marker='^', color="green", s=100)
            plt.annotate(f'Buy: {buy_value:.2f}', (buy_date, buy_value), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='green')

    if sell_date:

        sell_date = pandas.to_datetime(sell_date)
        sell_point = data_filtered[data_filtered["Date"] == sell_date]

        if not sell_point.empty:

            sell_value = sell_point["Close"].values[0] if history else MACD.loc[sell_point.index].values[0]
            
            plt.scatter(sell_date, sell_value, marker='v', color="red", s=100)
            plt.annotate(f'Sell: {sell_value:.2f}', (sell_date, sell_value), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8, color='red')
            
    __set_metadata(title, history)
    