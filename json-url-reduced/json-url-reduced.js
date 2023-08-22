// 
// This file is part of the m2-kiosk-app distribution (https://github.com/M2tec/m2_kiosk_app).
// Copyright (c) 2023 Maarten Menheere.
// 
// This program is free software: you can redistribute it and/or modify  
// it under the terms of the GNU General Public License as published by  
// the Free Software Foundation, version 3.
//
// This program is distributed in the hope that it will be useful, but 
// WITHOUT ANY WARRANTY; without even the implied warranty of 
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
// # General Public License for more details.
//
// You should have received a copy of the GNU General Public License 
// along with this program. If not, see <http://www.gnu.org/licenses/>.
//

var msgpack = require('msgpack5')() // namespace our extensions
var lzw = require("node-lzw");
var safe64 = require('urlsafe-base64');
var lzma = require('lzma');
const crypto = require('crypto');
const fs = require('fs');

function tx_encode(tx_json) {
    // Pack message 
    var tx_msgpack_encoded = msgpack.encode(tx_json);

    function on_finish(result, error) {
      return Buffer.from(result)
    }

    // LZW compress 
    tx_lzw_encoded = lzw.encode(tx_msgpack_encoded.toString('binary'));
    buf = Buffer.from.call(Buffer, tx_lzw_encoded)

    // LZMA compress 
    //tx_lzma_encoded = my_lzma.compress(tx_msgpack_encoded, 9, on_finish, on_progress)
    //buf = Buffer.from(result)
      
    tx_safe64_encoded = safe64.encode(buf);
    console.log(tx_safe64_encoded.toString())
    return tx_safe64_encoded
}

function create_url(network_type, gcscript) {

    //console.log(network_type)
    //console.log(gcscript)
    var gcscript = tx_encode(gcscript);

    let url;
    if (network_type === 'mainnet')
	    url = 'https://wallet.gamechanger.finance/api/1/tx/' + gcscript;
    else if (network_type === 'testnet')
	    url = 'https://testnet-wallet.gamechanger.finance/api/1/tx/' + gcscript;
    
    console.log('\n')
    console.log(url.toString())
    
    process.stdout.write(url)
    return url
}

var network_type = process.argv[2]
var json_file_name = process.argv[3]
//var json_file_name = "/tmp/shop_data-00051-003-0003.json"

var gcscript = ''

//try {
//  gcscript = JSON.parse(fs.readFileSync(json_file_name, 'utf8'));
//} catch (err) {
//  console.error(err);
//}
//var gcscript = process.argv[2]
var gcscript = {
  "type": "tx",
  "title": "230509-1711-5557",
  "description": "M2tec POS transaction",
  "outputs": {
    "addr_test1qz759fg46yvp28wrcmnxn87xq30yj6c8mh7y40zjnrg9h546h0qr3avqde9mumdaf4gykrtjz58l30g7mpy3r8nxku7q3dtrlt": [
      {
        "quantity": "11000000",
        "policyId": "tada",
        "assetName": "tADA"
      }
    ]
  }
}

var gcscript = {"type":"tx","title":"Demo","description":"created with gamechanger-dapp-cli","metadata":{"123":{"message":"Hello World!"}}}

var network_type = 'testnet'
//console.log(typeof gcscript)
//console.log(gcscript)

//console.log(network_type + '\n')
tx_encode(gcscript);


