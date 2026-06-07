
from src.validator import validator

def get_valids_invalids(converted):

    valids_raw = []
    invalids = []

    for stock in converted:
        is_valid, reasons = validator(stock)

        if not is_valid:
            invalid_data = stock.copy()
            invalid_data["error_reason"] = reasons
            invalids.append(invalid_data)
        
        else:
            valids_raw.append(stock)

    return invalids, valids_raw

#in the invalids output, the error reasons table shows twice, help 
#me understand why and how to solve it