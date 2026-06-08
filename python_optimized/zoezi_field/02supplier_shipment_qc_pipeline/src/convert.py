
def convert_data(raw):
    converted = []

    for vendor in raw:
        adapted = vendor.copy()

        units = adapted["units"]
        if units == "":
            adapted["units"] = None

        try:
            adapted["units"] = int(units)
        except ValueError:
            adapted["units"] = None

        unit_cost = adapted["unit_cost"]
        if unit_cost == "":
            adapted["unit_cost"] = None

        try:
            adapted["unit_cost"] = float (unit_cost)
        except ValueError:
            adapted["unit_cost"] = None

        converted.append(adapted)

    return converted