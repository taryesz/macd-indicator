import pandas

from chart import create_chart
from signals import find_signals

def __gather_signals(MACD: pandas.Series, 
                     SIGNAL: pandas.Series, 
                     data: pandas.DataFrame
                     ) -> pandas.DataFrame:

    # Create Series containing Buy/Sell signals
    buy_signals, sell_signals = find_signals(MACD, SIGNAL, data)

    # Unify the signals into a DataFrame
    # Set a date for each signal
    # 0 - nothing happened
    # 1 - buy
    # -1 - sell
    signals = pandas.DataFrame({
        "Date": data["Date"],
        "Signal": 0                 
    })

    signals.loc[buy_signals, "Signal"] = 1
    signals.loc[sell_signals, "Signal"] = -1

    return signals


def simulate_investing(MACD: pandas.Series, 
                       SIGNAL: pandas.Series, 
                       data: pandas.DataFrame
                       ) -> int:

    BUY: int = 1
    SELL: int = -1

    signals: pandas.DataFrame = __gather_signals(MACD, SIGNAL, data)

    capital: int = 1000     # Initial amount of EUR
    money: int = 0          # Initial amount of UAH
    wallet = []             # Data for a chart

    INITIAL_CAPITAL_UAH: int = 1000 * data["Close"][0]

    # Variables to track transaction results
    profitable_transactions = 0
    losing_transactions = 0
    total_transactions = 0

    for i in signals.index:
        
        # Current price of EUR in UAH and a corresponding date
        price = data["Close"][i]  
        date = data["Date"][i]
        
        # If Euro is now cheap and is going to become more expensive ...
        if signals["Signal"][i] == BUY:

            # If we have any money, buy EUR
            if money > 0:  
                capital = money / price
                money = 0 
        
        # If Euro is now expensive and is going to become cheaper ...
        elif signals["Signal"][i] == SELL:

            # If we have any capital, sell EUR
            if capital > 0:  
                money = capital * price
                capital = 0  

                # Calculate profit/loss of the transaction
                transaction_value = money - INITIAL_CAPITAL_UAH

                if transaction_value > 0: profitable_transactions += 1
                else: losing_transactions += 1

                total_transactions += 1

        # Update wallet change history
        wallet.append({"Date": date, "Close": money + (capital * price)})

    # Calculate effectiveness of MACD
    success_rate = (profitable_transactions / total_transactions) * 100

    print(f"Posiadane jednostki: {capital} EUR")
    print(f"Liczba transakcji zakończonych zyskiem: {profitable_transactions}")
    print(f"Liczba transakcji zakończonych stratą: {losing_transactions}")
    print(f"Skuteczność: {success_rate}%")

    # Show the wallet change chart
    create_chart(pandas.DataFrame(wallet), 
                 MACD=MACD,
                 SIGNAL=SIGNAL,
                 title="Wallet Change", 
                 history=True,
                 history_label="Wallet value in UAH",
                 initial_capital=INITIAL_CAPITAL_UAH
                 )

    return capital
