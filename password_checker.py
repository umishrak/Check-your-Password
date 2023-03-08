import requests
import hashlib
import sys

# Request API
def request_api_data(query_char):
    # Call API 
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, Check the API and try again")
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

# Check in API
def pwned_api_check(password):
    # check if this password exists in API response by encoding in Sha1  
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    
    # Adding to API Request
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main():
    with open('passwords.txt', 'r') as f:
        for password in f:
            password = password.strip()           
    
            count = pwned_api_check(password)
            if count:
             print(f'{password} was found {count} times. You should probably change your password!')
            else:
                print(f'{password} not pwned. All good!')
    return 'Check complete!'


if __name__ == '__main__':    
    sys.exit(main())
   
    
