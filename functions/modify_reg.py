import winreg

class regKey:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

def list_registry(base_key, sub_key): # listing subkeys and values
    values = []
    subkeys = []
    try:
        with winreg.OpenKey(base_key, sub_key) as key:
            print(f"Listing subkeys of {key}:")
            subkey_count = 0
            while True:
                try:
                    subkey = winreg.EnumKey(key, subkey_count)
                    # print(f"  Subkey: {subkey}")
                    subkeys.append(subkey)
                    subkey_count += 1
                except OSError:
                    break

            print(f"Listing values of {key}:")
            value_count = 0
            while True:
                try:
                    value_name, value_data, value_type = winreg.EnumValue(key, value_count)
                    print(f"  Value Name: {value_name}, Data: {value_data}, Type: {value_type}")
                    values.append(regKey(value_name, value_data, value_type))
                    value_count += 1
                except OSError:
                    break
        return values, subkeys
    
    except FileNotFoundError as e:
        raise e

def find_value(base_key, sub_key, name): # get value
    try:
        with winreg.OpenKey(base_key, sub_key) as key:
            print(f"Listing values of {key}:")
            while True:
                try:
                    value_data, value_type = winreg.QueryValueEx(key, name)
                    return regKey(name, value_data, value_type)

                except OSError:
                    break
        return None

    except FileNotFoundError as e:
        raise e

def set_value(base_key, sub_key, name, k):
    try:
        with winreg.OpenKey(base_key, sub_key) as key:
            winreg.SetValueEx(key, k.name, 0, k.type, k.value)
            return True
    except FileNotFoundError as e:
        raise e

# if __name__ == "__main__":
#     base_key = winreg.HKEY_LOCAL_MACHINE
#     sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\StillImage"

