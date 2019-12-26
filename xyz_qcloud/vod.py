# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

import time
import random
import hmac
import hashlib
import base64
from .utils import A
from django.conf import settings

C = lambda n: A('QCLOUD.VOD.%s' % n).resolve(settings, quiet=True)
SECRET_ID = C('SECRET_ID') or 'SECRET_ID'
SECRET_KEY = C('SECRET_KEY') or 'SECRET_KEY'

def gen_signature(SecretId=SECRET_ID, SecretKey=SECRET_KEY, expire=3600, extra_params=None):
    TimeStamp = int(time.time())
    # TimeStamp = 1571215095
    ExpireTime = TimeStamp + expire
    Random = random.randint(0, 999999)
    # Random = 220625

    Original = "secretId=" + SecretId \
               + "&currentTimeStamp=" + str(TimeStamp) \
               + "&expireTime=" + str(ExpireTime) \
               + "&random=" + str(Random)
    if extra_params:
        Original += "&"+extra_params
    Hmac = hmac.new(bytes(SecretKey), bytes(Original), hashlib.sha1)
    Sha1 = Hmac.digest()
    Signature = bytes(Sha1) + bytes(Original)
    Signature2 = base64.b64encode(Signature)
    return Signature2
