import json
import subprocess
import requests
from pprint import pprint

def cardano_transaction_json(transaction_id, wallet_address, amount):
    metadata_dict = {
        '123': {'message': transaction_id}
    }

    amounts_dict_1 = {
        'quantity': str(int(amount * 1000000)),
        'policyId': 'ada',
        'assetName': 'ada'
    }

    amounts_list = [amounts_dict_1]

    outputs_dict = {
        wallet_address: amounts_list
    }

    transaction_dict = {
        'type': 'tx',
        'title': transaction_id,
        'description' : 'M2tec POS transaction',
        'outputs': outputs_dict,
    }

    print(json.dumps(transaction_dict, indent=4, sort_keys=True))

    return json.dumps(transaction_dict)


def qr_code(qr_code_file_name, transaction_id, wallet_address, amount):
    tx_json = cardano_transaction_json(transaction_id, wallet_address, amount)

    print(qr_code_file_name)

    cardano_net = 'testnet'
    gc_cli = '/home/maarten/cardano-src/m2_kiosk_app/node_modules/gamechanger-dapp-cli/cli.js'
    command_list = [gc_cli, cardano_net, 'build', 'qr', '-a', tx_json, '-o', qr_code_file_name]
    result = subprocess.run(command_list, stdout=subprocess.PIPE)
    





  
    
