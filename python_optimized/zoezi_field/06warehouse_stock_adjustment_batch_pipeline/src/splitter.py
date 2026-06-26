
from src.validator import validate_data

def get_invalids_valids(converted):

    invalids = []
    valids = []

    for stock in converted:
        
        is_valids, reason = validate_data (stock)

        if not is_valids:
            inaccurates = stock.copy()
            inaccurates["error_reasons"] = ": ".join(reason)
            invalids.append(inaccurates)

        else:
            valids.append(stock.copy())

    return invalids, valids