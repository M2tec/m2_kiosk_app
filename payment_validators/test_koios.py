#!/usr/bin/python3

import koios

#data = {"network_type":"testnet","name":"Order 9714185520","wallet_address":"addr_test1qzn58ztr9t4eaxxzg4nxr7drzfe4gpl0rkx0rjjp70q3nzwm4uhvu74emhsyrtpqpqjt0hk2mflktqrvl3dn5hym6pes9nrq8r","total_with_tax":2.56}
data = {"network_type":"testnet","name":"Order 9714409568","wallet_address":"addr_test1qzn58ztr9t4eaxxzg4nxr7drzfe4gpl0rkx0rjjp70q3nzwm4uhvu74emhsyrtpqpqjt0hk2mflktqrvl3dn5hym6pes9nrq8r","total_with_tax":2.59}

#network_type = "testnet"
#transaction_id = "81"
#wallet_address = "addr_test1qzn58ztr9t4eaxxzg4nxr7drzfe4gpl0rkx0rjjp70q3nzwm4uhvu74emhsyrtpqpqjt0hk2mflktqrvl3dn5hym6pes9nrq8r"
#requested_amount = 2.54



print("network_type: \t\t" + data['network_type'])
print("transaction_id: \t" + data['name'])
print("wallet_address: \t" + data['wallet_address'])
print("requested_amount: \t" + str(data['total_with_tax']))

koios.payment_validate(data['network_type'], data['name'].split(' ')[1], data['wallet_address'], data['total_with_tax'])


