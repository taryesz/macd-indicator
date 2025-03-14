def ema(period: int, records: list, record_index: int) -> float:
 
    # Define crucial variables
    smoothing_factor = 2 / (period + 1) 
    numerator = 0                                            
    denumerator = 0
    exponent = 0

    # Iteration number depends on the record's index, NOT ON THE PERIOD
    for _ in range(record_index + 1):

        # Calculate a coefficient for the i-th record
        factor = (1 - smoothing_factor) ** exponent

        # Update the numerator and denumerator according to the EMA formula
        numerator += records[record_index] * factor         
        denumerator += factor                               

        # Each record's factor is powered to a corresponding to the record's index ???
        exponent += 1

        # Move on to the previous record
        record_index -= 1

    # return EMA for the specific day
    return numerator / denumerator
