from typing import List
import requests
from os.path import exists


def get_input (day: int) -> List[str]:
    file_name = f'inputs/day{day:02}.txt'
    if exists(file_name):
        with open(file_name) as f:
            return f.readlines()
    cookie = ''
    headers = {'session': cookie}
    url = f'https://adventofcode.com/2021/day/{day}/input'
    session = requests.Session()
    resp = session.get(url, cookies=headers)
    infile=open(file_name, 'w')
    infile.write(resp.text)
    infile.close()
    return get_input (day)