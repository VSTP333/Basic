#!/usr/bin/env python
# encoding: utf-8
'''
@author: 18056678（郭海龙）
@project: ApiShopping
@file: RSA_cryption.py
@time: 2020-02-25 09:45:26
@desc:
'''
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto import Random
class RSA_crypto():
    def __init__(self):
        self.random_generator = Random.new().read
        # pass

    def RSA_encrypt(self,public_key,message):
        """
        rsa加密
        :param public_key: 公钥，存于文件中，使用前先读取
        :param message: 明文
        :return: 密文
        """
        # message = "hello client, this is a message"
        # with open("client-public.pem") as f:
        key = public_key
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(message.encode('utf-8')))
        print("加密：",cipher_text.decode('utf-8'))
        return cipher_text.decode('utf-8')
        # pass
    def RSA_decrypt(self,pritive_key,cipher_text):
        """
        rsa解密
        :param pritive_key: 私钥，与上面公钥分开存于文件中，使用前先读取
        :param cipher_text: 密文
        :return: 明文
        """
        # with open("client-private.pem") as f:
        key = pritive_key
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(cipher_text), self.random_generator)
        print("解密：",text.decode('utf-8'))
        return text.decode('utf-8')
        # pass

if __name__ == "__main__":
    message = 'hello client, this is a message'
    public_key = '''-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC26X6A0WCWiVxdxq3jtm42yDdG
    bf+99v2zyi0UMVGZfowlnkcWeMvpz8NBm2UVlrjZpnFr8wFkdHyjFFkq/ilclH3A
    N4+Xw8Ap7CGJ2jVMyS5h9RRBUyf3F4D5Og8789Ywh9HXYyvD/6J62EtbbkhGPxg3
    aa8n2kfKZ9N6Q7DqrwIDAQAB
    -----END PUBLIC KEY-----
    '''
    pritive_key = """-----BEGIN RSA PRIVATE KEY-----
    MIICXQIBAAKBgQC26X6A0WCWiVxdxq3jtm42yDdGbf+99v2zyi0UMVGZfowlnkcW
    eMvpz8NBm2UVlrjZpnFr8wFkdHyjFFkq/ilclH3AN4+Xw8Ap7CGJ2jVMyS5h9RRB
    Uyf3F4D5Og8789Ywh9HXYyvD/6J62EtbbkhGPxg3aa8n2kfKZ9N6Q7DqrwIDAQAB
    AoGBAJn5qu1D1FxE24Vxl7ZGPzdMigN227+NaPptak9CSR++gLm2KL+JBpcXt5XF
    +20WCRvnWjl2QijPSpB5s6pWdHezEa1cl6WrqB1jDJd1U99WNCL5+nfEVD9IF+uE
    ig0pnj+wAT5fu78Z0UjxD9307f9S7BLC8ou3dWVkIqob6W95AkEAuPGTNlTkquu/
    wBJTb4/+/2ZCf7Ci9qvsN3+RcrzFkKa3uTtBOa6Xk2R61zBkucUgY6cQHPbxhFLN
    TVmXdbwxTQJBAP0wGenVOq4dCPdz3NhyghkKT6SL2w/SgbrROiJ1mG9MoBq58/0g
    k85I91R7nuvOYTKTUkhWdPYITpDarmPJzesCQGRBmOMgHCHH0NfHV3Gn5rz+61eb
    IoyD4Hapceh4CsWCiyAfzhj9229sTecvdbr68Lb0zphVCdIIrQCca63IShUCQGYI
    e3jzmHlQdCudArQruWgz8pKiVf7TW7qY1O/MKkk4PRFoPP6WoVoxp5LhWtM20Y7b
    Nf628N2xzU+tAThvvE8CQQCI1C7GO3I5EMfqPbTSq2oZq8thvGlyFyI7SNNuvAHj
    hj2+0217B9CcTZqloYln01CNDVuaoUgEvFSw1OdRB1tC
    -----END RSA PRIVATE KEY-----"""
    rsa_ = RSA_crypto()
    a = rsa_.RSA_encrypt(public_key=public_key,message=message)
    rsa_.RSA_decrypt(pritive_key=pritive_key,cipher_text=a)