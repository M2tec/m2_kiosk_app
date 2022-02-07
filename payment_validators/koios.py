import json
import requests
from pprint import pprint

# Check payment with the dandelion / koios - api node 
def payment_validate(network_type, transaction_id, wallet_address, requested_amount):

    payment_status = "not_received"

    base_url = "https://d.koios-api." + network_type + ".dandelion.link/rpc"
    headers = {'Content-type': 'application/json'}                    
    
    koios_hash_cache_old = ''

    # Get transaction data for current wallet adress
    print("\n------- Koios tip -------")    
    url = base_url + "/tip"
    r = requests.post(url)    
    print(r.text)
    print(json.loads(r.text)[0]["block_no"])
    block_tip = json.loads(r.text)[0]["block_no"]
    
    try:
        with open('/tmp/m2_koios_hash.json') as f:
            file_content = f.readline()
            if not file_content == "":
                koios_hash_cache_old = json.loads(file_content)
            #print(type(koios_hash_cache_old))
            print("\n------Old hashes ------- ")
            pprint(((koios_hash_cache_old)))
    except FileNotFoundError:
        pass
    
    # Get transaction data for current wallet adress
    # Limit number of transactions from current block 1 day ~ 2500 blocks
    json_data = {"_addresses":[wallet_address],
                 "_after_block_height": block_tip - 5000 }
                 
    url = base_url + "/address_txs"
    r = requests.post(url, headers=headers, json=json_data)
    #print(type(r.text))
    
    print("\n------- Koios response -------")
    koios_new_hash = json.loads(r.text)
    pprint((koios_new_hash))
   
    # Are there new hashes?
    new_hash = list(set(koios_new_hash) - set(koios_hash_cache_old))
  
    print("\nnew hash: " + str(new_hash))  
    
    if new_hash:
        print("==== New hash ====")
        with open('/tmp/m2_koios_hash.json', 'w') as f:
            f.write(r.text)      

        json_data = {"_tx_hashes": new_hash}

        url = base_url + "/tx_metadata"
        headers = {'Content-type': 'application/json'}                    
        r = requests.post(url, headers=headers, json=json_data)

        json_response_meta = json.loads(r.text)
        
        for tx_meta in json_response_meta:
            
            print("\ntx_meta: " + str(tx_meta))
            
            metadata = tx_meta["metadata"]
            for metadata_key in metadata:
                print(metadata[metadata_key]["type"])
                print(metadata[metadata_key]["title"])
                
                metadata_type = metadata[metadata_key]["type"]
                metadata_title = metadata[metadata_key]["title"]
                               
                if metadata_type == "tx" and metadata_title == transaction_id: 
                    
                    print(tx_meta["tx_hash"])
                    
                    print("\n-----confirm value-----")
                    url = base_url + "/tx_utxos"
                    headers = {'Content-type': 'application/json'}                    
                    r = requests.post(url, headers=headers, json={"_tx_hashes": [tx_meta["tx_hash"]]})
                    
                    tx_utxos = json.loads(r.text)
                    #print(tx_utxos)
                    print()
                    
                    if len(tx_utxos) == 1:
                        print("1 outputs")
                            
                        for tx in tx_utxos:       
                            utxo_output = tx["outputs"]
                            pprint(utxo_output)

                            for u in utxo_output:
                                payment_addr = u["payment_addr"]["bech32"]
                                
                                if wallet_address == payment_addr:               
                                    utxo_pay_amount = float(u["value"])/1000000
                            
                            print(requested_amount)
                            print(utxo_pay_amount)

                            if utxo_pay_amount >= requested_amount:
                                payment_status = "success"  
                                with open('/tmp/m2_koios_hash.json', 'w') as f:
                                    f.write('') 
              
    print("\nPayment status: " + payment_status)
    
    return payment_status   

