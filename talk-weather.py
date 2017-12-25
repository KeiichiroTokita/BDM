import urllib.request as req
import json, subprocess

# 天気予報のJSONデータをダウンロード
id = "130010" # 東京
url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=" + id
savename = "tenki.json"
req.urlretrieve(url, savename)

# JSONファイルを解析
data = json.load(open(savename, "r", encoding="utf-8"))
#print(data)

today_weather = data['forecasts'][0]['telop']
print('雨' in today_weather)

#text = data['description']['text']
#text = text.replace("\n", "")


"""

# 読み上げ
def exec(cmd):
    r = subprocess.check_output(cmd, shell=True)
    return r.decode("utf-8").strip()
# 一文ずつ読み上げる
lines = text.split("。")
for s in lines:
    if s == "": continue
    print(s)
    exec('./mei.sh "' + s + '"')

"""
