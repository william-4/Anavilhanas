""" mpesa payment handling """

from django.http import HttpResponse, JsonResponse
import requests
from datetime import datetime
import json
import base64

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


def initiate_stk_push(request):
    access_token_response = getAccessToken(request)
    if isinstance(access_token_response, JsonResponse):
        access_token = access_token_response.content.decode('utf-8')
        access_token_json = json.loads(access_token)
        access_token = access_token_json.get('access_token')
        if access_token:
            amount = 1
            phone = "254768168060"
            process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            callback_url = 'https://kariukijames.com/pesa/callback.php'
            passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
            business_short_code = '174379'
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
            party_a = phone
            party_b = '254708374149'
            account_reference = 'UMESKIA SOFTWARES'
            transaction_desc = 'stkpush test'
            stk_push_headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            }
            
            stk_push_payload = {
                'BusinessShortCode': business_short_code,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': amount,
                'PartyA': party_a,
                'PartyB': business_short_code,
                'PhoneNumber': party_a,
                'CallBackURL': callback_url,
                'AccountReference': account_reference,
                'TransactionDesc': transaction_desc
            }

            try:
                response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                response.raise_for_status()   
                # Raise exception for non-2xx status codes
                response_data = response.json()
                checkout_request_id = response_data['CheckoutRequestID']
                response_code = response_data['ResponseCode']
                
                if response_code == "0":
                    return JsonResponse({'CheckoutRequestID': checkout_request_id})
                else:
                    return JsonResponse({'error': 'STK push failed.'})
            except requests.exceptions.RequestException as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'error': 'Access token not found.'})
    else:
        return JsonResponse({'error': 'Failed to retrieve access token.'})



def process_stk_callback(request):
    stk_callback_response = json.loads(request.body)
    log_file = "Mpesastkresponse.json"
    with open(log_file, "a") as log:
        json.dump(stk_callback_response, log)
    
    merchant_request_id = stk_callback_response['Body']['stkCallback']['MerchantRequestID']
    checkout_request_id = stk_callback_response['Body']['stkCallback']['CheckoutRequestID']
    result_code = stk_callback_response['Body']['stkCallback']['ResultCode']
    result_desc = stk_callback_response['Body']['stkCallback']['ResultDesc']
    amount = stk_callback_response['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    transaction_id = stk_callback_response['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    user_phone_number = stk_callback_response['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
    
    if result_code == 0:
        print(merchant_request_id, checkout_request_id, result_code, result_desc, amount, transaction_id, user_phone_number)

    return
        