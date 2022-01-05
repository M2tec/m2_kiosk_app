import requests

url = "http://localhost:9090/gamechanger-payment"
r = requests.post(url, json={"transaction_id": "12313-113", "wallet_address": 12345, "pay_amount": 11111})
print(r.status_code)

input("Press Enter to continue...")

url = "http://localhost:9090/clear-display"
r = requests.post(url, json={"transaction_id": "12313-113", "wallet_address": 12345, "pay_amount": 11111})
print(r.status_code)
