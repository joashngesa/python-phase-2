
#Summarize by vendor
    #vendor_id
    #vendor_name
    #record_count
    #total_return_value
    #avg_return_value
    #high_value_count
    #medium_value_count
    #low_value_count

def summarize_data(transformed):

    summary = {}

    for item in transformed:

        vendor_id = item.get("vendor_id")
        vendor_name = item.get("vendor_name")
        return_value = item.get("return_value")
        return_band = item.get("return_band")

        if vendor_id not in summary:
            summary[vendor_id] = {
                "vendor_id": vendor_id,
                "vendor_name": vendor_name,
                "record_count": 0,
                "total_return_value": 0,
                "avg_return_value": 0,
                "high_value_count": 0,
                "medium_value_count": 0,
                "low_value_count": 0
            }

        summary[vendor_id]["record_count"] += 1
        summary[vendor_id]["total_return_value"] += return_value
        
        if return_band.lower() == "high":
            summary[vendor_id]["high_value_count"] += 1
        if return_band.lower() == "medium":
            summary[vendor_id]["medium_value_count"] += 1
        if return_band.lower() == "low":
            summary[vendor_id]["low_value_count"] += 1

    for repo in summary:
        distro = summary[repo]

        if distro["record_count"] > 0:
            distro["avg_return_value"] = round(distro["total_return_value"] / distro["record_count"])
        else:
            distro["record_count"] = 0.0
    return list(summary.values())