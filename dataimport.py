from contextlib import nullcontext
import time, os

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values
global gra, data
gra = None
data = None
def getdetails(gra,data):
    try:
        game = str(gra)
        info = str(data)
        import json
        with open("C:\\Users\\Borys\\Desktop\\AllegroChecker\\konta.json") as f:
            data = f.read()
            xd = json.loads(data)
            formula = xd["game"][game][info]
            return formula
    #Just Cause: justcause3
    #Dying Light 2: dyinglight2
    #Borderlands 3: borderlands3
    #Sniper Elite 5: sniperelite5
    except Exception as e:
        print("Error in dataimport.py" + str(e))
        return None


if __name__ != "__main__":
    os.system("cls")
    print('\033[92;1;1m' +"Dataimport.py has been imported correctly!"+'\033[0m')
    time.sleep(1)

