#!/usr/bin/python3
# coding:utf-8
from flask import Flask, jsonify, request, render_template, redirect, flash, session, make_response, Blueprint
from flask_login import UserMixin, LoginManager
from hashlib import md5
import time
from common.find_spider import FindSpider
from common.my_Spider import Spider
import os
import json
import importlib
import pkgutil
import inspect
import traceback

toutiao = Blueprint('toutiao', __name__,template_folder='../templates')

