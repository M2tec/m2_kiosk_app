#!/usr/bin/python3
import requests

url = "http://localhost:9090/payment-request"
title = '00051-003-0003'
wallet_address = 'addr_test1qzn58ztr9t4eaxxzg4nxr7drzfe4gpl0rkx0rjjp70q3nzwm4uhvu74emhsyrtpqpqjt0hk2mflktqrvl3dn5hym6pes9nrq8r'
pay_amount = '6.38'
r = requests.post(
    url,
    json={
        "transaction_id": title,
        "wallet_address": wallet_address,
        "amount": pay_amount})
print(r.status_code)

input("Press Enter to continue...")

url = "http://localhost:9090/clear-display"
# r = requests.post(url, json={"transaction_id": "12313-113", "wallet_address": 12345, "pay_amount": 11111})
print(r.status_code)
