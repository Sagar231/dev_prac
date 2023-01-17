import requests
import hashlib

def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code !=200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again ')
    return res

def get_pass_leak_count(hashes,hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h==hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1password[:5],sha1password[5:]
    responese=request_api_data(first5_char)
    return get_pass_leak_count(responese,tail)

def main(args):
        count = pwned_api_check(args)
        if count:
            print(f"{args} was found {count} times, you should change it.")
        else:
            print(f"{args} was not found, Carry on!")
        return "done!"

data = input("enter the password you want to check for: ")
main(data)
