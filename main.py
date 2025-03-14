import pandas
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from trend import create_trend
from chart import create_chart
from invest import simulate_investing

# Read the CSV file
DATA = pandas.read_csv('data/data.csv')

# Define periods of time to show charts of
# DATES: list[dict[str: str]] = [
#     {"start_date": "2022-01-24", "end_date": "2022-09-24", 
#     "buy_signal": "2022-05-09", "sell_signal": "2022-05-12"}, 
         
#     {"start_date": "2024-01-01", "end_date": "2025-01-01",
#     "buy_signal": "2024-07-02", "sell_signal": "2024-07-25"}
#     ]

# for period in DATES:

#     DESCRIPTION: str = f"The Exchange Rate of the Euro (EUR) Against the Ukrainian Hryvnia (UAH) from {period['start_date']}, to {period['end_date']}"

#     # Show the price change chart from date A to date B: 
#     create_chart(DATA, 
#                 title=DESCRIPTION,
#                 start_date=period['start_date'],
#                 end_date=period['end_date'],
#                 history=True
#                 )

#     # Create MACD/SIGNAL
#     MACD = create_trend(list(DATA['Close']), "MACD")
#     SIGNAL = create_trend(MACD, "SIGNAL")

#     # Show the MACD/SIGNAL
#     create_chart(DATA, 
#                 MACD=pandas.Series(MACD), 
#                 SIGNAL=pandas.Series(SIGNAL), 
#                 title="MACD/SIGNAL of " + DESCRIPTION,
#                 start_date=period['start_date'], 
#                 end_date=period['end_date']
#                 )

#     # Show the Buy/Sell signals on the original chart
#     create_chart(DATA, 
#                 MACD=pandas.Series(MACD), 
#                 SIGNAL=pandas.Series(SIGNAL),
#                 title=DESCRIPTION,
#                 start_date=period['start_date'],
#                 end_date=period['end_date'],
#                 history=True
#                 )
    
#     # Show the Buy/Sell signals on the original chart, also show stored values for chosen signals
#     create_chart(DATA, 
#                 MACD=pandas.Series(MACD), 
#                 SIGNAL=pandas.Series(SIGNAL),
#                 title=DESCRIPTION,
#                 start_date=period['start_date'],
#                 end_date=period['end_date'],
#                 history=True,
#                 buy_date=period['buy_signal'],
#                 sell_date=period['sell_signal']
#                 )

# Create MACD/SIGNAL
MACD = create_trend(list(DATA['Close']), "MACD")
SIGNAL = create_trend(MACD, "SIGNAL")

simulate_investing(pandas.Series(MACD), pandas.Series(SIGNAL), DATA)
