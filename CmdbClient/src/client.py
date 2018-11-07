#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import settings
import importlib
import paramiko
from concurrent.futures import ThreadPoolExecutor


class AutoBase:
    def exec_cmd(self):
        for k,v in settings.plugins_dict.items():
            mode_path,cls_name = v.rsplit('.', 1)
            cls = getattr(importlib.import_module(mode_path),cls_name)
            cls().execute()


class AutoSSH(AutoBase):

    def proess(self):
        host = settings.hosts_path
        pool = ThreadPoolExecutor(50)
        with open(host, "r") as f:
            for i in f.readlines():
                i=i.strip('\n')
                pool.submit(self.run, i)

    def run(self,args):
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=args, port=22, username='root', password='123456')

        # 执行命令
        # self.exec_cmd()
        result_dict = {}
        cmd_shell = settings.cmd_shell
        for k,v in cmd_shell.items():
            stdin, stdout, stderr = ssh.exec_command(v)
        # 获取命令结果
            result = stdout.read()

            res = result.decode('utf-8')
            result_dict[k] = res.strip('\n')
        print(result_dict)

        # 关闭连接
        ssh.close()







