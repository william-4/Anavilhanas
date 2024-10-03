import requests

def get_access_token():
    print("in the get access token function")
    consumer_key = 'j25bJmuRY0zWWgpKGwXAVI544bbRYlhku53721OAmiuCBLsG'
    consumer_secret = '5uDG8qv6dsD7g0g1PmRo24UbMiP9IzQNkF2W9XbQzjLnEAFrjfL3CIC8DCB2TBig'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    print(response.json())
    return

get_access_token()