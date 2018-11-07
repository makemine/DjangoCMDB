#!/usr/bin/python
# -*- coding:utf-8 -*-
from config import settings
from src.client import AutoSSH
import platform
os = platform.system()


def client():
    if settings.MODE == "ssh":
        if os == "linux":
            res = AutoSSH()
        elif os == "Darwin":
            res = AutoSSH()

        elif os == "windows":
            pass
        else:
            print("Only these three operating systems are supported")
        pass

    elif settings.MODE == "agent":
        if os == "linux":
            pass
        elif os == "Darwin":
            pass
        elif os == "windows":
            pass
        else:
            print("Only these three operating systems are supported")
        pass
    elif settings.MODE == 'slat':
        if os == "linux":
            pass
        elif os == "Darwin":
            pass
        elif os == "windows":
            pass
        else:
            print("Only these three operating systems are supported")
        pass
    else:
        print("Does not support")
    pass
    res.proess()