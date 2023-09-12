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

import json
import subprocess
import requests
from pprint import pprint
import os

import qrcode
import qrcode.image.svg

import json
import brotli
import base64

# import nft_storage


def base64_encode(string):
    """
    Removes any `=` used as padding from the encoded string.
    """
    encoded = base64.urlsafe_b64encode(string)
    return encoded.rstrip(b"=").rstrip(b"\n")


def base64_decode(string):
    """
    Adds back in the required padding before decoding.
    """
    padding = 4 - (len(string) % 4)
    string = string + (b"=" * padding)
    return base64.urlsafe_b64decode(string)


def json_deindent(data):
    # data = json.loads(data)
    data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return data


def gc_encode_brotli(gc_script):
    json_string = json_deindent(gc_script)
    brotli_data = brotli.compress(json_string.encode())
    url_string = base64_encode(brotli_data)
    return url_string.decode()


def gc_decode_brotli(url_string):
    brotli_data = base64_decode(url_string.encode())
    json_string = brotli.decompress(brotli_data)
    return json_string.decode()


def gc_encode_lzw(gc_script):
    ROOT_DIR = os.path.dirname(os.path.abspath(
        __file__))  # This is your Project Root
    p = subprocess.Popen(['node', ROOT_DIR + '/../json-url-reduced/json-url-lzw.js',
                         json.dumps(gc_script)], stdout=subprocess.PIPE)
    out = p.stdout.read().decode("utf-8").replace("\n", "")
    # print("Result:" + repr(out))
    return out


def gc_encode_lzma(gc_script):
    ROOT_DIR = os.path.dirname(os.path.abspath(
        __file__))  # This is your Project Root
    p = subprocess.Popen(['node', ROOT_DIR + '/../json-url-reduced/json-url-lzma.js',
                         json.dumps(gc_script)], stdout=subprocess.PIPE)
    out = p.stdout.read().decode("utf-8").replace("\n", "")
    # print("Result:" + repr(out))
    return out


def cardano_transaction_json(json_dict):

    wallet_address = json_dict["wallet_address"]
    transaction_id = str(json_dict["transaction_id"])
    token_policyID = json_dict["token_policyID"]
    token_name = json_dict["token_name"]
    requested_amount = float(json_dict["amount"]) * 1000000

    amounts_dict_1 = {
        'quantity': str(int(requested_amount)),
        'policyId': token_policyID,
        'assetName': token_name
    }

    amounts_list = [amounts_dict_1]

    outputs_dict = {
        wallet_address: amounts_list
    }

    transaction_dict = {
        'type': 'tx',
        'title': transaction_id,
        'description': 'M2tec POS transaction',
        'outputs': outputs_dict,
    }

    # print(json.dumps(transaction_dict, indent=4, sort_keys=True))

    return transaction_dict


def cardano_transaction_json_v2(json_dict):

    wallet_address = json_dict["wallet_address"]
    transaction_id = str(json_dict["transaction_id"])
    token_policyID = json_dict["token_policyID"]
    token_name = json_dict["token_name"]
    requested_amount = float(json_dict["amount"]) * 1000000

    assets_list = [{
        'quantity': str(int(requested_amount)),
        'policyId': token_policyID,
        'assetName': token_name
    }]

    outputs_dict = {
        'type': 'buildTx',
        'tx': {
            'outputs': [
                {
                    'address': wallet_address,
                    'assets': assets_list
                }
            ]
        }
    }

    sign_dict = {
        "type": "signTxs",
        "detailedPermissions": False,
        "txs": [
                "{get('cache.0.txHex')}"
        ]
    }

    submit_dict = {
        "type": "submitTxs",
        "txs": "{get('cache.1')}"
    }

    transaction_dict = {
        'type': 'script',
        'title': transaction_id,
        'description': 'M2tec POS transaction',
        'run': [outputs_dict, sign_dict, submit_dict]
    }

    # print(json.dumps(transaction_dict, indent=4, sort_keys=True))

    return transaction_dict


def cardano_transaction_json_gcfs(json_dict):

    wallet_address = json_dict["wallet_address"]
    transaction_id = str(json_dict["transaction_id"])
    requested_amount = float(json_dict["amount"]) * 1000000

    transaction_dict = {
        "type": "script",
        "run": {
            "A": {
                "type": "importAsScript",
                "args": {
                    "txId": transaction_id,
                    "ada": str(int(requested_amount)),
                    "wallet": wallet_address
                },
                "from": [
                    "gcfs://76897e6636ea9eefd37aaab82a8670394f84f2db29854bef8801552a.m2@latest://pay.gcscript"
                ]
            }
        }
    }

    # print(json.dumps(transaction_dict, indent=4, sort_keys=True))

    return transaction_dict


def cardano_mint_json_v2(json_dict):

    transaction_dict = {
        "type": "script",
        "title": "Minting",
        "description": "Mint your loyaly token",
        "exportAs": "MintingDemo",
        "return": {
            "mode": "last"
        },
        "run": {
            "dependencies": {
                "type": "script",
                "run": {
                    "address": {
                        "type": "getCurrentAddress"
                    },
                    "addressInfo": {
                        "type": "macro",
                        "run": "{getAddressInfo(get('cache.dependencies.address'))}"
                    },
                    "assetName": {
                        "type": "data",
                        "value": json_dict["name"]
                    },
                    "quantity": {
                        "type": "data",
                        "value": json_dict["amount"]
                    },
                    "currentSlotNumber": {
                        "type": "getCurrentSlot"
                    },
                    "deadlineSlotNumber": {
                        "type": "macro",
                        "run": "{addBigNum(get('cache.dependencies.currentSlotNumber'),'86400')}"
                    },
                    "mintingPolicy": {
                        "type": "nativeScript",
                        "script": {
                            "all": {
                                "issuer": {
                                    "pubKeyHashHex": "{get('cache.dependencies.addressInfo.paymentKeyHash')}"
                                }
                            }
                        }
                    }
                }
            },
            "build": {
                "type": "buildTx",
                "name": "build-Mint-Fungible",
                "title": "Mint fungible token",
                "tx": {
                    "ttl": {
                        "until": "{get('cache.dependencies.deadlineSlotNumber')}"
                    },
                    "mints": [
                        {
                            "policyId": "{get('cache.dependencies.mintingPolicy.scriptHashHex')}",
                            "assets": [
                                {
                                    "assetName": "{get('cache.dependencies.assetName')}",
                                    "quantity": "{get('cache.dependencies.quantity')}"
                                }
                            ]
                        }
                    ],
                    "outputs": {
                        "exampleDrop01": {
                            "address": "{get('cache.dependencies.address')}",
                            "assets": [
                                {
                                    "policyId": "ada",
                                    "assetName": "ada",
                                    "quantity": "2000000"
                                },
                                {
                                    "policyId": "{get('cache.dependencies.mintingPolicy.scriptHashHex')}",
                                    "assetName": "{get('cache.dependencies.assetName')}",
                                    "quantity": "{get('cache.dependencies.quantity')}"
                                }
                            ]
                        }
                    },
                    "witnesses": {
                        "nativeScripts": {
                            "mintingScript": "{get('cache.dependencies.mintingPolicy.scriptHex')}"
                        }
                    },
                    "auxiliaryData": {
                        "721": {
                            "{get('cache.dependencies.mintingPolicy.scriptHashHex')}": {
                                "{get('cache.dependencies.assetName')}": {
                                    "name": "{get('cache.dependencies.assetName')}",
                                    "image": json_dict["logo_ipfs_cid"],
                                    "version": "1.0",
                                    "mediaType": "image/png"
                                }
                            }
                        }
                    }

                }
            },
            "sign": {
                "type": "signTxs",
                "namePattern": "signed-Mint",
                "detailedPermissions": False,
                "txs": [
                    "{get('cache.build.txHex')}"
                ]
            },
            "submit": {
                "type": "submitTxs",
                "namePattern": "submitted-Mint",
                "txs": "{get('cache.sign')}"
            },
            "finally": {
                "type": "script",
                "run": {
                    "txHash": {
                        "type": "macro",
                        "run": "{get('cache.build.txHash')}"
                    },
                    "assetName": {
                        "type": "macro",
                        "run": "{get('cache.dependencies.assetName')}"
                    },
                    "policyId": {
                        "type": "macro",
                        "run": "{get('cache.dependencies.mintingPolicy.scriptHashHex')}"
                    },
                    "canMintUntilSlotNumber": {
                        "type": "macro",
                        "run": "{get('cache.dependencies.deadlineSlotNumber')}"
                    },
                    "mintingScript": {
                        "type": "macro",
                        "run": "{get('cache.dependencies.mintingPolicy.scriptHex')}"
                    }
                }
            }
        }
    }

    return transaction_dict


def qr_code(json_dict):
    print('-------- qr_code ----------')
    print(json_dict)
    network_type = json_dict["network_type"]
    transaction_id = str(json_dict["transaction_id"])

    if network_type == 'Mainnet':
        tx_json = cardano_transaction_json(json_dict)
        gcscript = gc_encode_lzw(tx_json)
        url = "https://wallet.gamechanger.finance/api/1/tx/" + gcscript

    elif network_type == 'Preprod':
        tx_json = cardano_transaction_json(json_dict)
        gcscript = gc_encode_lzw(tx_json)
        url = 'https://preprod-wallet.gamechanger.finance/api/1/tx/' + gcscript

    elif network_type == "Beta":
        tx_json = cardano_transaction_json_v2(json_dict)
        gcscript = gc_encode_lzma(tx_json)
        url = "https://beta-preprod-wallet.gamechanger.finance/api/2/run/" + gcscript

    elif network_type == "Beta-gcfs":
        tx_json = cardano_transaction_json_gcfs(json_dict)
        gcscript = gc_encode_lzma(tx_json)
        url = "https://beta-preprod-wallet.gamechanger.finance/api/2/run/" + gcscript

    elif network_type == "Beta-brotli":
        tx_json = cardano_transaction_json_v2(json_dict)
        gcscript = gc_encode_brotli(tx_json)
        url = "https://beta-preprod-wallet.gamechanger.finance/api/2/run/" + gcscript

    print("\n" + url)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=16,
        border=1,
        image_factory=qrcode.image.svg.SvgPathFillImage
    )

    qr.add_data(url)
    qr.make()
    img = qr.make_image(back_color="white")

    # with open('qr.svg', 'w') as f:
    #    f.write(img.to_string().decode())

    image = img.to_string()
    # print(image)
    return image


def url_mint_code(network_type, json_dict):
    print('-------- qr_code ----------')
    print(json_dict)
    
    if network_type == "Beta":
        tx_json = cardano_mint_json_v2(json_dict)
        gcscript = gc_encode_lzma(tx_json)
        url = "https://beta-preprod-wallet.gamechanger.finance/api/2/run/" + gcscript

    print("\n" + url)

    return url
