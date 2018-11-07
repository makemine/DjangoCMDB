#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms


class LoginFrom(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)