# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals, print_function
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models
from .utils import get_setting

A = lambda c: get_setting('ASR', c)
SECRET_ID = A('SECRET_ID')
SECRET_KEY = A('SECRET_KEY')


def send_request(url, channel_num=1, engine_model_type="16k_zh"):
    try:
        cred = credential.Credential(SECRET_ID, SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = asr_client.AsrClient(cred, "", clientProfile)

        req = models.CreateRecTaskRequest()
        params = {
            "Url": url,
            "ChannelNum": channel_num,
            "EngineModelType": engine_model_type,
            "SourceType": 0,
            "ResTextFormat": 0,
            "Action": "CreateRecTask",
            "Version": "2019-06-14",
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateRecTask(req)
        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)

def request_result(task_id):
    try:
        cred = credential.Credential(SECRET_ID, SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = asr_client.AsrClient(cred, "", clientProfile)

        req = models.DescribeTaskStatusRequest()
        params = {
            "Action": 'DescribeTaskStatus',
            "Version": '2019-06-14',
            "TaskId": task_id
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeTaskStatus(req)
        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)