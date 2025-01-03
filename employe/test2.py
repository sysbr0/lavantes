import requests

# Define the API endpoint
api_url = 'https://api.yapikredi.com.tr/api/payments/bill/v1/billDataSimulation'

# Define headers
headers = {
    'User-Agent': 'Python/3.8',
}

# Send a GET request to the API
response = requests.get(api_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Print the parsed data
    print("Bill Data Simulation Response:")
    for bill in data.get('response', {}).get('return', {}).get('billPaymentList', []):
        print(f"Product: {bill.get('product')}")
        print(f"Subscriber No: {bill.get('subscriberNo')}")
        print(f"Agent Code: {bill.get('agentCode')}")
        print(f"Bill Issue Date: {bill.get('billIssueDate')}")
        print(f"Institution: {bill.get('institution')}")
        print(f"Bill Amount: {bill.get('billAmount')}")
        print(f"Provision Code: {bill.get('provisionCode')}")
        print(f"Subscriber Name: {bill.get('subscriberName')}")
        print(f"Currency: {bill.get('currency')}")
        print(f"ID: {bill.get('id')}")
        print(f"Bill Due Date: {bill.get('billDueDate')}")
        print(f"Bill No: {bill.get('billNo')}")
        print(f"Channel Code: {bill.get('channelCode')}")
        print(f"Commission Amount: {bill.get('commissionAmount')}")
        print(f"Status: {bill.get('status')}")
        print("-" * 40)
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)  # Print the response body for debugging
