# coding=UTF-8
import time
import os
import base64
import requests
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from infrastructure.utils.common.signature import unique_parms, generate_signature


class SsoBase(object):

    def __init__(self):
        self._flag = ""
        self._priv_key = ""
        self._version = "1"
        self._token_start = "Basic"

    def _get_current_time(self):
        return int(time.time() * 1000)

    def _get_priv_key(self):
        if self._priv_key == "":
            cur_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(cur_path, 'rsa-pkcs1.pem')
            with open(file_path) as f:
                self._priv_key = f.read()
        return self._priv_key

    def rsa_long_decrypt(self , data):
        priv_key_str = self._get_priv_key()
        key = RSA.importKey(priv_key_str)
        h = SHA.new(data.encode("utf-8"))
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        sign = base64.b64encode(signature).decode()
        return sign

    def _pack(self, **param):
        param.update({
            "flag": self._flag,
            "timestamp": self._get_current_time(),
            "version":self._version,
            "proType":"ss"
        })
        sign = self._get_sign(**param)
        param.update({"sign": sign})
        return param

    def _get_sign(self, **param):
        sign_param = {}
        for k, v in param.items():
            if v or v == 0:
                sign_param[k.lower()] = v
        sign = ""
        unique_string , length = unique_parms(sign_param)
        if sign_param["signtype"] == "rsa":
            sign = self.rsa_long_decrypt(unique_string)
        elif sign_param["signtype"] == "sha":
            sign = generate_signature(unique_string, length)
        return sign

    def _request_api(self, **param):
        param = self._pack(**param)
        result = self.send(self.get_url(), None, **param)
        return result

    def send(self, url, headers, **body):
        result = requests.post(url, data=body, headers=headers)
        return result.json()

    def get_url(self):
        raise NotImplementedError("server need to implement get_url function")
