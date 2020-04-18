# coding=utf-8
import binascii

import rsa


def generator(public_file, private_file):
    (public_key, private_key) = rsa.newkeys(1024)

    pub = public_key.save_pkcs1()
    with open(public_file, 'wb+') as f:
        f.write(pub)

    pri = private_key.save_pkcs1()
    with open(private_file, 'wb+') as f:
        f.write(pri)

    return


def load_public(public_file):
    with open(public_file, 'rb') as public_file:
        p = public_file.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)
    return pubkey


def load_private(private_file):
    with open(private_file, 'rb') as private_file:
        p = private_file.read()
    private_key = rsa.PrivateKey.load_pkcs1(p)
    return private_key


def encrypt(public_file='data/public.pem', code=u'helwf2e22eavlo'):
    public_key = load_public(public_file)
    original_text = code.encode('utf8')
    crypt_text = rsa.encrypt(original_text, public_key)
    # print(crypt_text)
    # to binary code
    h = binascii.b2a_hex(crypt_text)
    b = bin(int(h, 16))
    b= b.replace('0b', '')
    return b

def pad_encrypt(b):
    len_b = len(b)
    res = len_b % 8
    if res == 0:
        return b
    b = b + '0' * (8-res)
    return b

def del_pad(b, len_b):
    return b[:len_b]


def decrypt(private_file='data/private.pem', b='', origin_code=''):
    private_key = load_private(private_file)
    # to hex code
    h = hex(int(b, 2))
    h = h.replace('0x', '')  # 去掉'0x'
    if len(h) != 256:
        h = (256 - len(h)) * '0' + h

    crypt_text = binascii.a2b_hex(h)
    # print(crypt_text)
    code = rsa.decrypt(crypt_text, private_key)
    # decode()
    return code


if __name__ == '__main__':
    public_file = 'data/public.pem'
    private_file = 'data/private.pem'
    # generator(public_file, private_file)
    code = 'swfiaefieiifafn'
    decrypt(private_file, encrypt(public_file, code), code)
