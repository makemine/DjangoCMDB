#!/usr/bin/python
# -*- coding:utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
import time
import requests
import paramiko
from config import settings
host = settings.hosts_path

def sshp(args):
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接服务器
    ssh.connect(hostname=args, port=22, username='root', password='123456')

    # 执行命令
    # self.exec_cmd()
    a_list = ['ls','du']
    for i in a_list:
        stdin, stdout, stderr = ssh.exec_command(i)

    # 获取命令结果
        result = stdout.read()
        print(result.decode('utf-8'))
    # 关闭连接
    ssh.close()


pool = ThreadPoolExecutor(50)

with open(host, "r") as f:
    for i in f.readlines():

        pool.submit(sshp, i)
