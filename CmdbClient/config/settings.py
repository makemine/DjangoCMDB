#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE = 'ssh'

plugins_dict = {
    "disk": "src.plugins.disk.AutoDisk",
    "cpu": "src.plugins.cpu.AutoCpu",
}

hosts_path = os.path.join(BASEDIR, 'src', 'hosts')

cmd_shell = {
    "ip": "ip a | grep eth0 | grep inet| awk '{print $2}'| awk -F'\/' '{print $1}'",
    "hostname": 'hostname',
    "free": "free -h| grep Swap|awk '{print $2}'",

}