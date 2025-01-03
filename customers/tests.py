from django.test import TestCase
import requests
import json

def get_bill_details(institution, product, subscriber_no):
    url = "https://api.yapikredi.com.tr/api/payments/bill/v1/billInquiry"
    
    payload = {
        "institution": institution,
        "product": product,
        "subscriberNo1": subscriber_no
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Log the raw response for analysis
        print("Raw Response:")
        print(response.text)

        if response.status_code == 200:
            bill_data = response.json()
            return bill_data
        else:
            print(f"Error: Received status code {response.status_code}")
            print("Response:", response.text)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    institution = "ASKİ"  # Example institution
    product = "SU"  # Example product
    subscriber_no = "1524691200"  # Example subscriber number

    bill_details = get_bill_details(institution, product, subscriber_no)

    if bill_details:
        print(json.dumps(bill_details, indent=4, ensure_ascii=False))
