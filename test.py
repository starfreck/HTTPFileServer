import requests

headers1 = {
    'Accept': 'application/xml',
}

headers2 = {
    'Accept': 'text/html',
}

header3 = {
    'Content-Type': 'application/json',
}

data1 = '{"login":"my_login","password":"my_password"}'

response0 = requests.get('http://localhost:8080')
response1 = requests.get('http://localhost:8080/', headers=headers1)
response2 = requests.get('http://localhost:8080/', headers=headers2)
# the error one
response3 = requests.get('http://localhost:8080/foo')

response4 = requests.get('http://localhost:8080/Yun')
response5 = requests.post('http://localhost:8080/xyz.txt', headers=header3, data=data1)


print(response0.headers)
# print(response4.text)

# print(resForAX.text)

# with open('./data/COMP 352 A1.txt', 'r') as f:
#     print(f.read())
