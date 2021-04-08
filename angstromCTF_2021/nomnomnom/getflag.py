import requests as r
import sys

BASE_URL = 'https://nomnomnom.2021.chall.actf.co'

cookie = {'no_this_is_not_the_challenge_go_away': sys.argv[2] if len(
    sys.argv) > 2 else ''}
if __name__ == '__main__':
    response = r.get(url=f"{BASE_URL}/shares/{sys.argv[1]}", cookies=cookie)
    print(response.text)
    response.raise_for_status()
