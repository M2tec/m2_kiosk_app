var msgpack = require('msgpack5')() // namespace our extensions
var lzw = require("node-lzw");
var safe64 = require('urlsafe-base64');
const crypto = require('crypto');
const fs = require('fs');

function tx_encode(tx_json) {
    // Pack message 
    var tx_msgpack_encoded = msgpack.encode(tx_json);

    // LZW compress message
    tx_lzw_encoded = lzw.encode(tx_msgpack_encoded.toString('binary'));

    // Make string url safe 
    buf = Buffer.from.call(Buffer, tx_lzw_encoded)
    tx_safe64_encoded = safe64.encode(buf);
    
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
    
    //console.log('\n')
    console.log(url)
}

//var network_type = 'testnet'

var network_type = process.argv[2]
var json_file_name = process.argv[3]
//var json_file_name = "/tmp/shop_data-00051-003-0003.json"

var gcscript = ''

try {
  gcscript = JSON.parse(fs.readFileSync(json_file_name, 'utf8'));
} catch (err) {
  console.error(err);
}
//var gcscript = process.argv[2]

//var gcscript = {"type":"tx","title":"Demo","description":"created with gamechanger-dapp-cli","metadata":{"123":{"message":"Hello World!"}}}
//console.log(typeof gcscript)

create_url(network_type, gcscript);


