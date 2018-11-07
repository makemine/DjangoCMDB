#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys
from src.scripts import client

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
# print(BASEDIR)
if __name__ == '__main__':

    client()