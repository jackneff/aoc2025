# Inspired by 0xdf's genday.sh script
# https://gitlab.com/0xdf/aoc2024/

import sys
import os
import requests
from dotenv import dotenv_values
from bs4 import BeautifulSoup

env = dotenv_values(".env")

boilerplate = """
import sys

with open(sys.argv[1], 'r') as f:
    lines = list(map(str.strip(), f.readlines()))
"""


def project_name(day):
    """
    Makes sure single digit days get a leading zero prefixed on.  Ex(2 becomes 02 and 8 becomes 08).  Then slaps 'day' on the front for a name.  Super original.
    """
    day = day if len(day) > 2 else f"0{day}"
    return f"day{day}"


def fetch(url, cookie):
    """
    Fetches the input text from AOC and writes into input.txt file
    """
    s = requests.Session()
    s.cookies.set("session", cookie, domain="adventofcode.com")
    r = s.get(url)
    return r


def write_to_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)


def main(day):
    """
    Create boilerplate project for single AOC day
    """
    year = 2025  # change this each year
    name = project_name(day)
    root_url = f"https://adventofcode.com/{year}/day/{day}"
    cookie = env["MY_AOC_SESSION_COOKIE"]

    if not cookie:
        print("Need to put a cookie in the .env file named MY_AOC_SESSION_COOKIE")
        return

    os.mkdir(name)
    os.chdir(name)

    # dayXX.py
    write_to_file(f"{name}.py", boilerplate)

    # challenge.md
    res1 = fetch(root_url, cookie)
    soup = BeautifulSoup(res1.content, "html.parser")
    articles = soup.find_all("article")
    with open("challenge.md", "w") as f:
        for article in articles:
            f.write(article.get_text())

    # ex.txt
    write_to_file("ex.txt", "")

    # input.txt
    res2 = fetch(f"{root_url}/input", cookie)
    if res2:
        write_to_file("input.txt", res2.text)
    else:
        print("No input recieved")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        day = sys.argv[1]
    else:
        day = input("What day? [1-25]: ")

    main(day)
