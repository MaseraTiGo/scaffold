# coding=UTF-8

import random
import base64
import json
from Crypto.Cipher import AES


# 随机字符串
def get_nonce_str(length = 32):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    nonce_str = ""
    for i in range(length):
        tmp_len = random.randint(0, len(chars) - 1)
        nonce_str += chars[tmp_len:tmp_len + 1]
    return nonce_str


def get_urlparam(kwargs):
    keys = sorted(kwargs)
    paras = ['{}={}'.format(key, kwargs[key]) for key in keys]  # and kwargs[key] != '']
    url_str = '&'.join(paras)
    return url_str


# AES-256-ECB解密（PKCS7Padding）
def decrypt(enc, key):
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    return unpad(cipher.decrypt(enc)).decode('utf8')


def decrypt_iv(enc, key, iv):
    sessionKey = base64.b64decode(key)
    encryptedData = base64.b64decode(enc)
    iv = base64.b64decode(iv)
    cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    decrypted = json.loads(unpad(cipher.decrypt(encryptedData)).decode('utf8'))
    return decrypted
