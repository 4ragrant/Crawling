# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:26:31 2024

@author: DS
"""

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import re
from selenium import webdriver
from pandas import DataFrame

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager