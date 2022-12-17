#!/usr/bin/python3

from Naked.toolshed.shell import execute_js, muterun_js
import qrcode

response = muterun_js('json-url-reduced.js')

url = response.stdout.decode("utf-8").replace("\n", "")

print(url)

img = qrcode.make(url)
type(img)  # qrcode.image.pil.PilImage
img.save("gc_qrcode.png")
