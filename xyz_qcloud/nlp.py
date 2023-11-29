# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from tencentcloud.nlp.v20190408 import models, nlp_client
from tencentcloud.common import credential
from .utils import get_setting
import json

A = lambda c: get_setting('NLP', c)
SECRET_ID = A('SECRET_ID')
SECRET_KEY = A('SECRET_KEY')
AP = A('AP') or "ap-guangzhou"

def keywordsExtract(text, num=20):
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    client = nlp_client.NlpClient(cred, AP)
    req = models.KeywordsExtractionRequest()
    req.Text = text
    req.Num = num
    resp = client.KeywordsExtraction(req)
    return json.loads(resp.to_json_string())
