import json

response =  '{"ok":1.0, "result": [{"total": 142250.0,"_id":"BC"}, {"total": 210.88999999999996, "_id": "USD"}, ' \
            '{"total": 1065600.0,"_id": "TK"}]}'

response = json.loads(response)

# for (k, v) in response.items():
#
#     print(k)
#     print(v)

for doc in response['result']:
    print(doc['total'])
    # print(doc)
# print(response)

