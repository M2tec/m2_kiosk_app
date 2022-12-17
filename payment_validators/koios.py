import json
import requests
from pprint import pprint

def koios_request(network_type, request_type, json_tx_filter = {}):
    # Get transaction data for current wallet adress
    #print("\n------- Koios request -------")   

    base_url = "https://d.koios-api." + network_type + ".dandelion.link/rpc"
    #base_url = "https://" + network_type + ".koios.rest/api/v0"
     
    url = base_url + "/" + request_type
    print("URL: \t\t" + url)
    headers = {
    'Accept' : 'application/json',
    'Content-type': 'application/json'} 
    
    filter_json = json.dumps(json_tx_filter)
    filter_json = json_tx_filter
    
    print("Filter: \t" + repr(filter_json))
    
    try:    
        response = requests.post(url, headers=headers, json=filter_json)    
    except requests.exceptions.ConnectionError as e:
        print(e)
        exit()
                  
    print("Response: \n")
    pprint(response.json())
    print()
    return response.json()
    

def get_block_tip(network_type):
    # Get the most recent block
    print("\n------- Koios tip -------")    
    block_tip = koios_request(network_type, 'tip')[0]["block_no"]
    print("Blocktip: \t" + str(block_tip))
    return block_tip

def get_read_old_hashes():

    koios_hash_cache_old = ''
       
    try:
        with open('/tmp/m2_koios_hash.json') as f:
            file_content = f.readline()
            if not file_content == "":
                #koios_hash_cache_old = json.loads(file_content)
                print("cash")
            #print(type(koios_hash_cache_old))
            print("\n------Old hashes ------- ")
            pprint(((koios_hash_cache_old)))
    except FileNotFoundError:
        pass
    
    return koios_hash_cache_old

def get_transactions_hashlist(network_type, json_tx_filter):
    print("\n-----Get transaction hash list-------")
    
    transaction_hash_list = []
    
    # Get transaction data for current wallet adress
    # Limit number of transactions from current block. => 1 day ~ 2500 blocks                   
    response = koios_request(network_type, 'address_txs', json_tx_filter)
   
    print(response)
    print()
    for tx in response:
        tx_hash = tx['tx_hash']
        transaction_hash_list.append(tx_hash)
        
    print(' ')  
    print('Hash list of transactions in wallet')  
    pprint((transaction_hash_list))
    
    return transaction_hash_list
    
    
def get_tx_metadata(network_type, tx_hash_list):
    print("\n-------Get transaction hash metadata--------")
    json_tx_filter = { "_tx_hashes": tx_hash_list }
    json_response_meta = koios_request(network_type, 'tx_metadata', json_tx_filter)
        
    return(json_response_meta)

def check_metadata_type_and_title(transactions_metadata, transaction_id):
    print("\n-------Check_metadata_type_and_title--------")
    
    hash_tx_type_and_title_confirmed = ''    
    print("Transaction id:\t" + transaction_id)
    for tx_meta in transactions_metadata:    
        metadata = tx_meta["metadata"]
       
        for metadata_key in metadata:
                                  
            metadata_type = metadata[metadata_key]["type"]
            metadata_title = metadata[metadata_key]["title"]
            
            print("Type:\t " + metadata_type + "\tTitle:\t" + metadata_title)
                           
            if metadata_type == "tx" and metadata_title == transaction_id: 
                print('Hash confirmed:\t' + tx_meta["tx_hash"] + '\n')
             
                hash_tx_type_and_title_confirmed = tx_meta["tx_hash"]
    
    return hash_tx_type_and_title_confirmed

def confirm_amount(network_type, wallet_address, checked_hash, requested_amount):
    print("\n-----confirm amount-----")
    
    json_tx_filter = {"_tx_hashes": [checked_hash]}
    tx_utxos = koios_request(network_type, 'tx_utxos', json_tx_filter)
                     
    payment_status = "not_received"
           
    if len(tx_utxos) == 1:           
        for tx in tx_utxos:       
            utxo_output = tx["outputs"]
            #pprint(utxo_output)

            for u in utxo_output:
                payment_addr = u["payment_addr"]["bech32"]
                
                if wallet_address == payment_addr:               
                    utxo_pay_amount = float(u["value"])/1000000
            
            print("Requested amount: " + repr(requested_amount))
            print("Utxo_pay_amount: " + repr(utxo_pay_amount))
            
            print(type(utxo_pay_amount))
            print(type(requested_amount))
            if utxo_pay_amount >= float(requested_amount):
                payment_status = "success"  
    return payment_status                
    
# Check payment with the dandelion / koios - api node 
def payment_validate(network_type, transaction_id, wallet_address, requested_amount):
                 
    block_tip = get_block_tip(network_type)
    
    json_tx_filter = {"_addresses":[wallet_address],
                      "_after_block_height": block_tip - 5000 }  
    transaction_hash_list = get_transactions_hashlist(network_type, json_tx_filter)

    transactions_metadata = get_tx_metadata(network_type, transaction_hash_list)
    
    checked_hash = check_metadata_type_and_title(transactions_metadata, transaction_id)

    print(checked_hash)
    payment_status = confirm_amount(network_type, wallet_address, checked_hash, requested_amount)
    
    print("\nPayment status: " + payment_status)
    
    return payment_status   

