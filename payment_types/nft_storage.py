import requests
import json

def nft_storage_upload(data):
    print("================= NFT storage upload ================")
    url = "https://api.nft.storage/upload"

    headers = {'accept': 'application/json',
            'Content-Type': 'image/*',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDlGZDNkYjM5NDJiZUYyNURhYWE4NzdkNTY4MDM0MTkyODI0MERkNGEiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY5Mzk4NzU5MDU5MCwibmFtZSI6Ik0ydGVjIn0.X_zIKxYGZbaL32Jx1iC-hYtA8VYwNW5IuNUhT0Ld0-0'
            }

    # with open('./m2tec_logo_github.png', 'rb') as f:
    #     data = f.read()

    r = requests.post(
        url,
        headers=headers,
        data=data)

    print("Reason:".ljust(15) + str(r.reason))
    print("Status code:".ljust(15) + str(r.status_code))
    print("Text:".ljust(15) + str(r.text))

    cid = json.loads(r.text)["value"]["cid"]
    ipfs_url = "ipfs://" + cid

    return ipfs_url