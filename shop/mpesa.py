""" mpesa payment handling """

from django.http import HttpResponse, JsonResponse
import requests

def getAccessToken(requests):
    consumer_key = ""
    consumer_secret = ""
    access_token_url = ""
    headers = {'Content-Type': 'application/json'}
    auth = (consumer_key, consumer_secret)
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status()
        result = response.json()
        access_token = result['access token']
        return JsonResponse({'access_token': access_token})
    except requests.exception.RequestException as e:
        return JsonResponse({'error': str(e)})
