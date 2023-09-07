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
var safe64 = require('urlsafe-base64');
var lzma = require('lzma');

function tx_encode(tx_json) {
    // Pack message 
    var tx_msgpack_encoded = msgpack.encode(tx_json);

    // LZMA compress 
    result = lzma.compress(tx_msgpack_encoded, 9);
    buf = Buffer.from(result)

    tx_safe64_encoded = safe64.encode(buf);
    console.log(tx_safe64_encoded)
    return tx_safe64_encoded
}

//var gcscript = {"type":"tx","title":"Demo","description":"created with gamechanger-dapp-cli","metadata":{"123":{"message":"Hello World!"}}}
var gcscript = JSON.parse(process.argv[2]);

//console.log(gcscript);
tx_encode(gcscript);


