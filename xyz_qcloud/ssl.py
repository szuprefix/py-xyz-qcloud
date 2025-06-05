from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models
import os, json

SECRET_ID = os.getenv('SECRET_ID')
SECRET_KEY = os.getenv('SECRET_KEY')

RES_TYPES = ['clb',
 'cdn',
 'waf',
 'live',
 'ddos',
 'teo',
 'apigateway',
 'vod',
 'tke',
 'tcb',
 'tse',
 'cos']

def get_client(secret_id=SECRET_ID, secret_key=SECRET_KEY):
    cred = credential.Credential(secret_id, secret_key)

    http_profile = HttpProfile()
    http_profile.endpoint = "ssl.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    # 创建SSL客户端
    client = ssl_client.SslClient(cred, "", client_profile)

    return client

def get_cert(id):
    describe_req = models.DescribeCertificateDetailRequest()
    describe_req.CertificateId = id
    client = get_client()
    return client.DescribeCertificateDetail(describe_req)


def query_certs(keyword='', client=None, **kwargs):
    try:
        if not client:
            client = get_client()

        req = models.DescribeCertificatesRequest()

        params = {
            "SearchKey": keyword
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeCertificates(req)

        certificates = []
        for cert in resp.Certificates:
            d = json.loads(cert.to_json_string())
            if kwargs.items()<= d.items():
                certificates.append(d)

        return certificates

    except Exception as err:
        print(f"查询SSL证书时出错: {err}")
        return []

def read_key_file(fn):
    if '-----' in fn:
        return fn
    else:
        with open(fn, 'r') as f:
            return f.read()

def upload_cert(cert_name, cert_file, key_file,  cert_type="SVR", resource_types=RES_TYPES, **kwargs):
    try:
        client = get_client(**kwargs)

        certificate_content = read_key_file(cert_file)

        private_key_content = read_key_file(key_file)
        certs = query_certs(cert_name, Alias=cert_name)
        if certs:
            cert = certs[0]
            id = cert['CertificateId']
            print(f'update cert: {id}')
            req = models.UpdateCertificateInstanceRequest()
            req.OldCertificateId = id
            req.ResourceTypes = resource_types
            req.CertificatePublicKey = certificate_content
            req.CertificatePrivateKey = private_key_content
            resp = client.UpdateCertificateInstance(req)
            return json.loads(resp.to_json_string())
        else:
            req = models.UploadCertificateRequest()
            req.CertificatePublicKey = certificate_content
            req.CertificatePrivateKey = private_key_content
            req.Alias = cert_name
            req.CertificateType = cert_type
            resp = client.UploadCertificate(req)

        # 返回响应
        return {
            "CertificateId": resp.CertificateId,
            "RequestId": resp.RequestId
        }

    except TencentCloudSDKException as err:
        print(f"上传SSL证书失败: {err}")
        return None

