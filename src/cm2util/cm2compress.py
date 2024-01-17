import requests

def Compress(saveCode):
    data = {"content": saveCode, "syntax": "text", "expiry_days": 1}
    headers = {"User-Agent": "CM2 IMAGE"}
    r = requests.post("https://dpaste.org/api/", data=data, headers=headers)
    return r.text.strip("\"") + "/raw"