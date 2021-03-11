---
title: Generate HMAC SHA256 signature in Python
date: 2019-05-30
category: Python
tags: encoding, hash, hmac, security, sha256
authors: Gaurav Jain
summary: 
coverimage: /images/sha256.png
---

SHA256 encoded strings can be used to secure payment gateway.

For this problem, there is a popular function written in C#, `CreateSHA256Signature()`,
which you can find here [Azadehkhojandi’s Gist](https://gist.github.com/Azadehkhojandi/50eaae4cf20b21faef186f2c8ee97873).

Recently, In one of the project, I was asked to convert this function into Python. After minutes of searching on google, I had no success so decided to convert it by myself and after few minutes of hit and trial, I got this -

```python
import hmac
import hashlib 
import binascii

def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", "TEST STRING")
```

Also, hosted on Github: [Gaurav Jain’s GIST](https://gist.github.com/gauravvjn/172a4a9933626bd507e00ae6245e33a1)
