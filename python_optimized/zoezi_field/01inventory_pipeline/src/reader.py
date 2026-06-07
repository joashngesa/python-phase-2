from src.config import INPUT_PATH

def read_data(file_path):

    raw = []
    try:

        with open (file_path, "r", encoding="utf-8") as file:
            next(file)
            
           
            for stock in file:
                lines = stock.strip()

                if not lines:
                    continue

                parsed = lines.split("|")

                if len(parsed) != 5:
                    raw.append({
                        "sku": parsed[0].strip() if len(parsed) > 0 else "",
                        "product": parsed[1].strip() if len(parsed) > 1 else "",
                        "warehouse": parsed[2].strip() if len(parsed) > 2 else  "",
                        "quantity": parsed[3].strip() if len(parsed) > 3 else "",
                        "unit_cost": parsed[4].strip() if len(parsed) > 4 else "",
                        "error_reason": "parse_error: rows do not have exactly 5 fields"
                    })
                    continue

                sku = parsed[0].strip()
                product = parsed[1].strip()
                warehouse = parsed[2].strip()
                quantity = parsed[3].strip()
                unit_cost = parsed[4].strip()

                data = {
                        "sku": sku,
                        "product": product,
                        "warehouse": warehouse,
                        "quantity": quantity,
                        "unit_cost": unit_cost,
                        "error_reason": ""
                }

                raw.append(data)

    except Exception as e:
        print(f"file reading error: {e}")
        return []
    
    
    return raw
