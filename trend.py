from ema import ema

def create_trend(records: list, type: str) -> list:

    # Get the number of records present in the CSV file
    records_amount = len(records)

    TREND = []

    for record_index in range(records_amount):

        if type == "MACD":

            # Fill the MACD Series with data calculated from EMA
            TREND.append(ema(12, records, record_index) - ema(26, records, record_index))

        elif type == "SIGNAL":

            # Fill the SIGNAL Series with data calculated from EMA
            TREND.append(ema(9, records, record_index))

        else: break

    return TREND
