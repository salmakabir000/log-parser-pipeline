from datetime import datetime

# correcting data types
def clean_types(record):
    # float conversion
    def to_float(x):
        try:
            return float(x) if x is not None else None
        except:
            return None
    #int conversion
    def to_int(x):
        try:
            return int(x) if x is not None else None
        except:
            return None
    # timestamp conversion
    def to_timestamp(x):
        try:
            if x:
                return datetime.fromisoformat(x.replace("Z", "+00:00"))
            return None
        except:
            return None
        
    record["retn"] = to_int(record.get("retn"))
    record["amount"] = to_float(record.get("amount"))
    record["vat"] = to_float(record.get("vat"))
    record["units"] = to_float(record.get("units"))
    record["debtAmount"] = to_float(record.get("debtAmount"))
    record["time"] = to_int(record.get("time"))
    record["success"] = bool(record.get("success"))
    record["created"] = to_timestamp(record.get("created"))
    record["confirmationTime"] = to_timestamp(record.get("confirmationTime"))
    record["initiationTime"] = to_timestamp(record.get("initiationTime"))
    return record



# remove duplicates using ref
def deduplicate_by_ref(data):
    deduplicated_data = {}
    for record in data:
        ref = record.get("ref")
        if ref not in deduplicated_data:
            deduplicated_data[ref] = record
        else:
            if record.get("created") > deduplicated_data[ref].get("created"):
                deduplicated_data[ref] = record

    deduplicated_data = list(deduplicated_data.values())
    return deduplicated_data