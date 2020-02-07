# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

import json, time, random, hmac, hashlib, base64
from .utils import access
from django.conf import settings

C = lambda n: access(settings, 'QCLOUD.VOD.%s' % n)
SECRET_ID = C('SECRET_ID') or 'SECRET_ID'
SECRET_KEY = C('SECRET_KEY') or 'SECRET_KEY'
AP = C('AP') or "ap-guangzhou"


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
        Original += "&" + extra_params
    Hmac = hmac.new(bytes(SecretKey), bytes(Original), hashlib.sha1)
    Sha1 = Hmac.digest()
    Signature = bytes(Sha1) + bytes(Original)
    Signature2 = base64.b64encode(Signature)
    return Signature2


def get_media_info(file_ids, ap=AP):
    from tencentcloud.vod.v20180717 import models, vod_client
    from tencentcloud.common import credential
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    client = vod_client.VodClient(cred, ap)
    req = models.DescribeMediaInfosRequest()
    req.FileIds = file_ids.split(',') if isinstance(file_ids, (str, unicode)) else file_ids
    resp = client.DescribeMediaInfos(req)
    return json.loads(resp.to_json_string())
