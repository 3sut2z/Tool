import json

def mask_sensitive_data(json_data):
    sensitive_keys = {"UGPHONE-Token", "access_key", "access_secret", "mqtt_password"}
    
    for key in sensitive_keys:
        if key in json_data:
            json_data[key] = "***MASKED***"
    
    if "UGPHONE-MQTT" in json_data:
        try:
            mqtt_data = json.loads(json_data["UGPHONE-MQTT"])
            for key in sensitive_keys:
                if key in mqtt_data:
                    mqtt_data[key] = "***MASKED***"
            json_data["UGPHONE-MQTT"] = json.dumps(mqtt_data)
        except json.JSONDecodeError:
            print("Error decoding MQTT data")
    
    return json_data

# Đọc dữ liệu JSON từ file
with open("ug_zzzzzzzzzzzzzzzzfdsw00202.txt", "r") as file:
    data = json.load(file)

# Ẩn thông tin nhạy cảm
data_secured = mask_sensitive_data(data)

# Ghi dữ liệu đã ẩn vào file mới
with open("secured_data.json", "w") as file:
    json.dump(data_secured, file, indent=4)

print("Dữ liệu đã được xử lý và lưu vào secured_data.json")
