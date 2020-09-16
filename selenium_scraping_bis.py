# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:34:37 2020

@author: Collabcap
"""


################################################################"
#Fonctions
import random
from random import randint

#from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


from selenium import webdriver
import bs4
import lxml

import time
import math

import ast

import re

from joblib import Parallel, delayed
import time, math

import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException

import requests
from requests.exceptions import ConnectionError

import urllib.request
from urllib.request import urlopen, URLError

from cleaner import cleaner
from requests_scraping import liste_terme
import logging
#%%
#################################
    


#################################################################"
    
def open_driver() :
    """
    open browser Chrome

    Returns
    -------
    driver : webdriver.Chrome
    """
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options, executable_path="geckodriver")
    driver.set_page_load_timeout(60)
    #options.add_argument('--headless')
    #driver =  webdriver.Chrome(options=options, executable_path = "chromedriver")
    time.sleep( 3  )
    return driver

def close_driver(driver) :
    """
    Close browser

    Parameters
    ----------
    driver : webdriver.Chrome

    Returns
    -------
    None.

    """
    driver.quit()

def page_web(url, driver) :
    """
    Go in url with browser and keep this page

    Parameters
    ----------
    url : string
        
    driver :  webdriver.Chrome

    Returns
    -------
    page : string
        page with tags.
    rep : Bool
        0 if dont acces to url & 1 if no problem.

    """
    compteur = 0 
    rep = False 
    while (not rep) and (compteur < 3) :
        compteur = compteur + 1
        try :
           driver.get( url )
           page =  driver.page_source
           rep = True
        except WebDriverException:
            try :
                close_driver(driver)
            except :
                pass
            #close_driver(driver)
            driver = open_driver()
            rep = False
        except InvalidSessionIdException:
            try :
                close_driver(driver)
            except :
                pass
            driver = open_driver()
            rep = False
    if not rep :
        page = " "
    return  (page , rep)

def text_page(url, driver) :
    """
    Get only text of url.

    Parameters
    ----------
    url : str
        
    driver :  webdriver.Chrome
        

    Returns
    -------
    ( text, rep )
    text : string.
        
    rep : Bool
        1 if succes
        
    """
    (page, info) = page_web(url, driver)
    text = page.encode('utf-8')
    text = cleaner( text )
    
    return (text, int(info))


def check_url(url="http://google"):
    """
    Verify url

    Parameters
    ----------
    url : srt

    Returns
    -------
    bool
        True if url exist, False else.

    """
    time.sleep( 1)
    try:
        urlopen(url)
        return True
    except URLError:
        return False
    except ValueError :
        return False

def list_links( url, driver ):
    """
    list link from url

    Parameters
    ----------
    url : str
        
    driver : webdriver.Chrome
        

    Returns
    -------
    List of str.
        List of urls

    """
    #time.sleep(3)
    (page, info) = page_web( url, driver )
    soup = bs4.BeautifulSoup( page )
    Liste = []
    for link in soup.find_all('a', href=True):
        Liste.append( link['href'] )
    return( np.unique( Liste ).tolist() )


def crawl_website ( object_requests_scraping ) :
    """
    Scrapping one website

    Parameters
    ----------
    url : str
        DESCRIPTION.

    Returns
    -------
    str

    """
    try :
        return object_requests_scraping[ "description" ]
    except :
        return "NaN"
    
    """
    if "Status" in object_requests_scraping.keys() :
        if object_requests_scraping[ "Status" ] == '<Response [200]>' :
            return object_requests_scraping[ "description" ]
        else :
            url = object_requests_scraping['url_website']
    else :
        if isinstance( object_requests_scraping['url_website'] , str) :
            url  = object_requests_scraping['url_website']
        else :
            return " "
    print( url )
    website = url
    print("Starting selenium with " + str(website))
    #test url
    if check_url( url) == False :
        print("Not able to connect with selenium at " + url)
        return " "
    #check url
    temp_url=url
    if temp_url[0:5] =='wwww.' :
        temp_url = re.sub('https://', '', temp_url)
    # open firefox
    driver = open_driver()
    Liste_des_liens = list_links( temp_url, driver )
    close_driver(driver)

    temp_description = ""
    # conserver les infos de la première page
    driver = open_driver()
    (text, info ) = text_page(temp_url, driver)
    close_driver(driver)
    temp_description = text
    nb_page = 1
    nb_page_lus = int( info )
    # recherche de liens problables où il y a la description
    for lien in Liste_des_liens:
        for terme_description in liste_terme :
            if ( (terme_description in lien) and not("linkedin.com" in lien) and not("twitter" in lien) ) and (nb_page < 25) :
                nb_page = nb_page +1
                lien_complet = lien
                
                if ( not "www." in lien_complet ) and (not check_url( lien_complet) ) :
                    lien_complet = url + lien_complet
                
                if check_url( lien_complet) :
                    #close_driver(driver)
                    driver = open_driver()
                    (text, info ) = text_page(lien_complet, driver)
                    close_driver(driver)

                    temp_description = temp_description + " " + text
                    nb_page_lus = nb_page_lus + int( info )

                else :
                    
                    nb_page = nb_page - 1
    
    print("Ending selenium with " + str(website))
    return temp_description
    """



def crawl_website_bis ( object_requests_scraping ) :
    """
    Scrapping one website

    Parameters
    ----------
    url : str
        DESCRIPTION.

    Returns
    -------
    str

    """
    if "Status" in object_requests_scraping.keys() :
        if object_requests_scraping[ "Status" ] == '<Response [200]>' :
            return object_requests_scraping[ "description" ]
        elif len( str( object_requests_scraping[ "description" ] ) ) > 80 :
            return object_requests_scraping[ "description" ]
        else :
            url = object_requests_scraping['url_website']
    else :
        if isinstance( object_requests_scraping['url_website'] , str) :
            url  = object_requests_scraping['url_website']
        else :
            return " "
    print( url )
    website = url
    print("Starting selenium with " + str(website))
    #test url
    if check_url( url) == False :
        print("Not able to connect with selenium at " + url)
        return " "
    #check url
    temp_url=url
    if temp_url[0:5] =='wwww.' :
        temp_url = re.sub('https://', '', temp_url)
    # open firefox
    driver = open_driver()
    Liste_des_liens = list_links( temp_url, driver )
    close_driver(driver)

    temp_description = ""
    # conserver les infos de la première page
    driver = open_driver()
    (text, info ) = text_page(temp_url, driver)
    close_driver(driver)
    temp_description = text
    nb_page = 1
    nb_page_lus = int( info )
    # recherche de liens problables où il y a la description
    for lien in Liste_des_liens:
        for terme_description in liste_terme :
            if ( (terme_description in lien) and not("linkedin.com" in lien) and not("twitter" in lien) ) and (nb_page < 25) :
                nb_page = nb_page +1
                lien_complet = lien
                
                if ( not "www." in lien_complet ) and (not check_url( lien_complet) ) :
                    lien_complet = url + lien_complet
                
                if check_url( lien_complet) :
                    #close_driver(driver)
                    driver = open_driver()
                    (text, info ) = text_page(lien_complet, driver)
                    close_driver(driver)

                    temp_description = temp_description + " " + text
                    nb_page_lus = nb_page_lus + int( info )

                else :
                    
                    nb_page = nb_page - 1
    
    print("Ending selenium with " + str(website))
    return temp_description
 
def crawl_website_ter ( object_requests_scraping ) :
    try :
        return crawl_website ( object_requests_scraping )
    except :
        return "NaN"











