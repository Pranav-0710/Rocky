import urllib.request, json
req = urllib.request.Request('https://rocky-azure.vercel.app/api/chat', data=b'{"message":"hello"}', headers={'Content-Type': 'application/json'}, method='POST')
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code, e.read().decode())
