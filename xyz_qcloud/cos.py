# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from .utils import get_setting
from .sts import Sts

A = lambda c: get_setting('COS', c)
SECRET_ID = A('SECRET_ID')
SECRET_KEY = A('SECRET_KEY')
AP = A('AP') or "ap-guangzhou"
BUCKET = A('BUCKET')


def gen_signature(SecretId=SECRET_ID, SecretKey=SECRET_KEY, expire=None, bucket=BUCKET, allow_prefix=None):
    config = {
        # 临时密钥有效时长，单位是秒
        'duration_seconds': expire or 1800,
        'secret_id': SecretId,
        # 固定密钥
        'secret_key': SecretKey,
        # 设置网络代理
        # 'proxy': {
        #     'http': 'xx',
        #     'https': 'xx'
        # },
        # 换成你的 bucket
        'bucket': bucket,
        # 换成 bucket 所在地区
        'region': AP,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': allow_prefix,
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # 简单上传
            'name/cos:PutObject',
            'name/cos:PostObject',
            # 分片上传
            'name/cos:InitiateMultipartUpload',
            'name/cos:ListMultipartUploads',
            'name/cos:ListParts',
            'name/cos:UploadPart',
            'name/cos:CompleteMultipartUpload'
        ],

    }

    sts = Sts(config)
    d = sts.get_credential()
    d['bucket'] = bucket
    return d
