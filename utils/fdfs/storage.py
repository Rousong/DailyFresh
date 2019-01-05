# -*- coding:utf-8 -*-
from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client

class FDFSStorage(Storage):
    '''文件存储类'''
    def __init__(self, client_conf = None, nginx_url = None):
        """初始化"""
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if nginx_url is None:
            nginx_url = settings.FDFS_NGINX_URL
        self.nginx_url = nginx_url

    def _open(self,name,mode='rb'):
        '''打开文件时使用'''
        pass
    def _save(self,name,content):
        '''保存文件时使用'''
        # name是选择的上传文件的名字
        # content是File的对象,包含你上传文件内容的File对象
        # content： 包含上传文件内容的File对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client('./utils/fdfs/client.conf')

        # 上传到fdfs的服务器中
        res =client.upload_by_buffer(content.read())
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }

        # 判断是否上传成功
        if res['Status'] != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fdfs失败')

        # 获取文件的id
        file_id = res['Remote file_id']

        # 返回文件的id

        return file_id

    def exists(self, name):
        """判断文件在本地文件系统中是否存在"""
        # 因为我们的文件是保存在fdfs中的,所有默认所有名字可用
        return False

    def url(self, name):
        """返回可访问到name文件的URL路径"""

        return self.nginx_url+name


