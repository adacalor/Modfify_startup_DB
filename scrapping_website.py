# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 13:50:49 2020

@author: Collabcap
"""

############################################################
####### import library
from pymongo import MongoClient
import pandas as pd
import unicodedata
import codecs
import time
import datetime 
from multiprocessing import Pool, current_process

import re

import coloredlogs, logging
coloredlogs.install()


from stop_words import get_stop_words

import pprint
############################################
############ import script on scraping

from requests_scraping import requests_scraping
from selenium_scraping_bis import crawl_website_ter
from cleaner import cleaner


########################################################
############## connexion to mongo db

infos_mongo = infos_counterparts = pd.read_json( codecs.open("mongodb_connection_parameters.json", 'r', 'utf-8') , orient="index" )
    
client = MongoClient( infos_mongo[0]["name_connection"],
                         infos_mongo[0]["port_connection"])
db = client[ infos_mongo[0]["name_database"] ]
collection = db[ infos_mongo[0]["name_collection"] ]

############################""""

Max_nb_characters = 6000

def scrapping_website(id_item) :
    old_element = collection.find_one({"id": id_item})
    try :
        website = old_element["web_infos"]["website_url"]
        description_web = requests_scraping(website )
        description_web = crawl_website_ter(description_web)[0 : Max_nb_characters]
    except :
        description_web = " "
    try :
        description_linkedin = old_element["web_infos"]["description"]
        description_linkedin_sans_accent = cleaner( description_linkedin ) 
    except :
        description_linkedin_sans_accent = " "

    collection.update_one({'id': id_item},
                          {"$set": {"web_infos.normalized_description" : description_linkedin_sans_accent,
                                    "web_infos.description_web" :description_web ,
                                    }
                           } )
###################################"
    
def launch_updating() :
    t1 = time.time()
    
    id_list_full = [item["id"] for item in collection.find({})]
    id_list = id_list_full
    
    pos = 0
    avance = 2000
    while pos < len( id_list ) :
        print( pos )
        
        
        nb_core = 7
        with Pool(nb_core) as p:
            p.map(scrapping_website, id_list[pos : pos + avance ])
        pos = avance + pos

    print("updating global ok")
    t2 = time.time()
    print( "durée :" , (t2-t1)/60, " min")
    
    client.close()
    print("Program finished")





###############################


if __name__ == '__main__':
    
    t1 = time.time()

    launch_updating()
    
    t2 = time.time()
    print( "durée :" , (t2-t1)/60, " min")
    
    elt_1 = collection.find_one({})

    pprint.pprint(elt_1["web_infos"] )
else :
    pass
client.close()
print("Program finished")



