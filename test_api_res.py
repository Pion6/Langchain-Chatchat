import requests

# url = "http://10.12.54.64:5000/school/sheet/王小明/明天"
# response = requests.get(url)
# print(response.text)
# print("------------returnData----------------")
# # print(data)
# print("------------returnData----------------")
sttr = "{'name': '王小明','time': '明天'}"
dict_obj = eval(sttr)
print(dict_obj['name'])
print(dict_obj['time'])


