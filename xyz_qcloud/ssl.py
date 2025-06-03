from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models
import os

SECRET_ID = os.getenv('SECRET_ID')
SECRET_KEY = os.getenv('SECRET_KEY')

def upload_ssl_certificate(cert_name, cert_file, key_file, secret_id=SECRET_ID, secret_key=SECRET_KEY,  cert_type="SVR"):
    """
    上传SSL证书到腾讯云

    参数:
        secret_id: 腾讯云API密钥ID
        secret_key: 腾讯云API密钥Key
        cert_name: 证书名称
        cert_file: 证书文件路径(PEM格式)
        key_file: 私钥文件路径(PEM格式)
        cert_type: 证书类型，默认为"SVR"(服务器证书)
    """
    try:
        # 初始化认证对象
        cred = credential.Credential(secret_id, secret_key)

        # 配置HTTP和客户端
        http_profile = HttpProfile()
        http_profile.endpoint = "ssl.tencentcloudapi.com"

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        # 创建SSL客户端
        client = ssl_client.SslClient(cred, "", client_profile)

        # 读取证书和私钥文件内容
        if '-----' in cert_file:
            certificate_content = cert_file
        else:
            with open(cert_file, 'r') as f:
                certificate_content = f.read()

        if '-----' in key_file:
            private_key_content = key_file
        else:
            with open(key_file, 'r') as f:
                private_key_content = f.read()

        # 构造请求参数
        req = models.UploadCertificateRequest()
        req.CertificatePublicKey = certificate_content
        req.CertificatePrivateKey = private_key_content
        req.Alias = cert_name
        req.CertificateType = cert_type

        # 发起请求
        resp = client.UploadCertificate(req)

        # 返回响应
        return {
            "CertificateId": resp.CertificateId,
            "RequestId": resp.RequestId
        }

    except TencentCloudSDKException as err:
        print(f"上传SSL证书失败: {err}")
        return None
