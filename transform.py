import xml.etree.ElementTree as ET

# Top Level Extraction
def extract_top_level(data):
    clean_data = []
    for record in data:
        clean_record = {
            "id": record.get("_id", {}).get("$oid"),
            "action": record.get("action"),
            "success": record.get("success"),
            "gateway": record.get("gateway"),
            "ref": record.get("ref"),
            "service": record.get("service"),
            "time": record.get("time"),
            "created": record.get("created", {}).get("$date"),
            "response": record.get("response")
        }

        clean_data.append(clean_record)
    return clean_data


# building parse_xml to turn XML script into python data
def parse_xml(xml_text):
    fields = [
        "desc",
        "retn",
        "amount",
        "confirmationTime",
        "customerAddress",
        "customerMeterNumber",
        "debtAmount",
        "initiationTime",
        "status",
        "units",
        "unitsType",
        "value",
        "vat"
    ]
    # create empty template
    parsed_data = {field: None for field in fields}

    if not xml_text:
        return parsed_data
    
    try:
        root = ET.fromstring(xml_text)
        for elem in root.iter():
            tag = elem.tag.split("}")[-1]
            if tag in parsed_data:
                parsed_data[tag] = elem.text
        return parsed_data
    except Exception:
        return parsed_data
    

def combine_data(data):
    final_data = []
    for record in data:

        xml_fields = parse_xml(record.get("response"))
        record_without_response = record.copy()
        record_without_response.pop("response", None)
        
        combined_record = {
            **record_without_response,
            **xml_fields
        }
        final_data.append(combined_record)
    return final_data