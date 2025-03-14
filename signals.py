import matplotlib.pyplot as plt
import pandas

def find_signals(MACD: pandas.Series, 
                SIGNAL: pandas.Series, 
                data: pandas.DataFrame, 
                y_axis = None
                ) -> pandas.Series:

    # Find Buy/Sell signals
    buy_signals = (MACD.shift(1) < SIGNAL.shift(1)) & (MACD > SIGNAL)
    sell_signals = (MACD.shift(1) > SIGNAL.shift(1)) & (MACD < SIGNAL)
            
    # Add the signals to the chart 
    if y_axis is not None:
        plt.scatter(data["Date"][buy_signals], y_axis[buy_signals], marker='^', color="green", label='Buy', s=100)
        plt.scatter(data["Date"][sell_signals], y_axis[sell_signals], marker='v', color="red", label='Sell', s=100)

    return buy_signals, sell_signals