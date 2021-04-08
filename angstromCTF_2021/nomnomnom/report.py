import requests as r
import sys


BASE_URL = 'https://nomnomnom.2021.chall.actf.co'
share_name = sys.argv[1]
response = r.post(url=f"{BASE_URL}/report/{share_name}")
print(response.text)
response.raise_for_status()
