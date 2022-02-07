#!/usr/bin/python3

import koios

network_type = "testnet"
transaction_id = "00051-003-0003"
wallet_address = "addr_test1qzn58ztr9t4eaxxzg4nxr7drzfe4gpl0rkx0rjjp70q3nzwm4uhvu74emhsyrtpqpqjt0hk2mflktqrvl3dn5hym6pes9nrq8r"
requested_amount = 6.38

print("network_type: \t\t" + network_type)
print("transaction_id: \t" + transaction_id)
print("wallet_address: \t" + wallet_address)
print("requested_amount: \t" + str(requested_amount))

koios.payment_validate(network_type, transaction_id, wallet_address, requested_amount)


