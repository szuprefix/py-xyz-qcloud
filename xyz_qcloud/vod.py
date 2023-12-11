# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals, print_function

import json, time, random, hmac, hashlib, base64

from six import text_type

from .utils import get_setting

A = lambda c: get_setting('VOD', c)
SECRET_ID = A('SECRET_ID')
SECRET_KEY = A('SECRET_KEY')
AP = A('AP') or "ap-guangzhou"
SUB_APP_ID = A('SUB_APP_ID')


def gen_signature(SecretId=SECRET_ID, SecretKey=SECRET_KEY, expire=3600, sub_app_id=SUB_APP_ID, extra_params=None):
    TimeStamp = int(time.time())
    # TimeStamp = 1571215095
    ExpireTime = TimeStamp + expire
    Random = random.randint(0, 999999)
    # Random = 220625

    Original = "secretId=" + SecretId \
               + "&currentTimeStamp=" + str(TimeStamp) \
               + "&expireTime=" + str(ExpireTime) \
               + "&random=" + str(Random)
    if sub_app_id:
        Original += "&vodSubAppId=" + str(sub_app_id)
        print(sub_app_id)
    if extra_params:
        Original += "&" + extra_params
    Hmac = hmac.new(SecretKey.encode(), Original.encode(), hashlib.sha1)
    Sha1 = Hmac.digest()
    Signature = Sha1 + Original.encode()
    Signature2 = base64.b64encode(Signature)
    return Signature2.decode()


def get_media_info(file_ids, ap=AP, sub_app_id=SUB_APP_ID):
    from tencentcloud.vod.v20180717 import models, vod_client
    from tencentcloud.common import credential
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    client = vod_client.VodClient(cred, ap)
    req = models.DescribeMediaInfosRequest()
    req.FileIds = file_ids.split(',') if isinstance(file_ids, text_type) else file_ids
    if sub_app_id:
        req.SubAppId = sub_app_id
    resp = client.DescribeMediaInfos(req)
    return json.loads(resp.to_json_string())
