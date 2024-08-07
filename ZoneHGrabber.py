"""
                  _________-----_____
       _____------           __      ----_
___----             ___------              \
   ----________        ----                 \
               -----__    |             _____)
                    __-                /     \
        _______-----    ___--          \    /)\
  ------_______      ---____            \__/  /
               -----__    \ --    _          /\
                      --__--__     \_____/   \_/\
                              ----|   /          |
                                  |  |___________|
                                  |  | ((_(_)| )_)
                                  |  \_((_(_)|/(_)
                                  \             (
                                   \_____________) Coded By MachineGun @undergroundcy


"""
import requests
from bs4 import BeautifulSoup
import re
import os
import sys
from tld import get_tld
from time import sleep
from urllib.parse import urlparse
import argparse
from remove_duplicates import DuplicatorRemover
#from database import *

parser = argparse.ArgumentParser(description="Zone-H Grabber")
epilog = "Example: python3 zoneh.py -n undergroundcy"
parser.add_argument("-p", "--phpsessid", required=True, help="The PHPSESSID after verifying the captcha e.g => iqhg1hpl6u3h9pramlkjaur1s3")
parser.add_argument("-z", "--zhe", required=True, help="zhe Token After Veryfying the captcha : e.g => a78656eb0643e749d79808e64eade4f7")
parser.add_argument("-n", "--notifier", help="Name of the notifier like (undergroundcy or urlencoded username)")
parser.add_argument("-l", "--list", help="List of Notifiers To check for Defacement")
args = parser.parse_args()

name = args.notifier
phpsessid = args.phpsessid
zhetoken = args.zhe
path = os.getcwd()
input_file = os.path.join(path, "urls.txt")
output_file = os.path.join(path, "Results", "output.txt")

def remove_dup():
    remover = DuplicatorRemover(input_file, output_file)
    remover.remove_duplicates()

def number_of_lines(file_path):
    with open(file_path, "r") as File:
        line_count = sum(1 for line in File)
    return line_count

def check_notifier(defacer_username):
    cookies = {'PHPSESSID': phpsessid, 'ZHE': zhetoken}
    user_browser = "User-Agent"
    header = {user_browser: "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"}
    page_number = 1
    counter = 1
    url = f"http://www.zone-h.org/archive/notifier={defacer_username}"
    while True:
        response = requests.get(url, headers=header, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        pages = re.findall(r'page=(\d+)', response.text)
        pages = len(pages) + 1
        with open(input_file, "a+") as File:
            for tag in soup.find_all(re.compile("td")):
                try:
                    url = "http://" + tag.string
                    tld_name = get_tld(url)
                    if tld_name and tld_name.lower() != "date":
                        url = urlparse(url)
                        File.write(url.hostname.strip() + "\n")
                except:
                    continue

        counter += 1
        if counter > pages:
            print(f"Numbers Of Lines {number_of_lines(input_file)}")
            break
        else:
            page_number += 1
            url = f"http://www.zone-h.org/archive/notifier={defacer_username}/page={str(page_number)}"
            print(f"Numbers Of Lines {number_of_lines(input_file)}")
            sleep(2)

if (args.notifier is None or not args.notifier.strip()) and (args.list is None or not args.list.strip()):
    print("Please Enter a Notifier Or A list of notifiers")
    sys.exit()


elif args.list.strip():
    list_file = os.path.join(path, args.list.strip())
    with open(list_file, "r") as File:
        usernames = [username.strip() for username in File.readlines()]
    for defacer in usernames:
        print(f"Defacer #> {defacer}")
        try:
            check_notifier(defacer)
        except NameError as e:
            print(f"Couldn't Catch Defacements of {defacer}")
            print(e)
            continue
else:
    print(f"Defacer #> {name}")
    check_notifier(name)

remove_dup()
number_of_lines_output = number_of_lines(output_file)
print(f"Numbers Of Results {number_of_lines_output}")

sleep(3)

#os.system("cls")
#print("ADDING URLS TO DATABASE")

#ADDING URLS.txt TO DATABASE
path_to_url_files = r"C:\Users\machinegun\Desktop\powershell\zone-h Grabber\MyZoneHGrabber\urls.txt"
#push_to_db()
