import requests

BASE = "http://10.0.0.22:80/"

# data = [{"likes": 100, "name": "tim", "views":100000},
# 		{"likes": 200, "name": "tong", "views":800},
# 		{"likes": 300, "name": "tan", "views":1000}]

# for i in range(len(data)):
# 	response = requests.put(BASE + "video/" + str(i), data[i])
# 	print(response.json())

response = requests.patch(BASE + "video/2", {'views': 8000, 'likes': 10000})
print(response.json())

input()
response = requests.get(BASE + "video/2")
print(response.json())