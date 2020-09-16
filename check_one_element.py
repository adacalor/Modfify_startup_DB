# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:53:04 2020

@author: Collabcap
"""


import requests
import datetime 
import json
import time
import re 

from multiprocessing import Pool, current_process
from pymongo import MongoClient
from bs4 import BeautifulSoup

from random import randint

import codecs
import pandas as pd

import pprint

import coloredlogs, logging

coloredlogs.install()

logger = logging.getLogger("check")
#logger.setLevel(logging.INFO)
logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.DEBUG)



########################################################
############## connexion to mongo db


infos_mongo = infos_counterparts = pd.read_json( codecs.open("mongodb_connection_parameters.json", 'r', 'utf-8') , orient="index" )
    
client = MongoClient( infos_mongo[0]["name_connection"],
                         infos_mongo[0]["port_connection"])
db = client[ infos_mongo[0]["name_database"] ]
collection = db[ infos_mongo[0]["name_collection"] ]



############################""""

print( db.collection_names() )

elt_1 = collection.find_one({})

pprint.pprint(elt_1["web_infos"] )




client.close()