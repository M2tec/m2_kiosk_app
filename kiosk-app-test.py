#!/usr/bin/python3

#
# This file is part of the m2-kiosk-app distribution (https://github.com/M2tec/m2_kiosk_app).
# Copyright (c) 2023 Maarten Menheere.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import requests

url = "http://localhost:9090/payment-request"
network_type = "testnet"
title = '00051-003-0003'
token_name = 'ADA'
token_policyID = 'ada'
wallet_address = 'addr_test1qzn58ztr9t4eaxxzg4nxr7drzfe4gpl0rkx0rjjp70q3nzwm4uhvu74emhsyrtpqpqjt0hk2mflktqrvl3dn5hym6pes9nrq8r'
pay_amount = '6.38'
r = requests.post(
    url,
    json={
        "network_type": network_type,
        "transaction_id": title,
        "token_name": token_name,
        "token_policyID": token_policyID,
        "wallet_address": wallet_address,
        "amount": pay_amount})
print(r.status_code)

input("Press Enter to continue...")

url = "http://localhost:9090/clear-display"
# r = requests.post(url, json={"transaction_id": "12313-113", "wallet_address": 12345, "pay_amount": 11111})
print(r.status_code)
