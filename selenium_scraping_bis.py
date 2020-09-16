# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:34:37 2020

@author: Collabcap
"""





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
    

def crawl_website_ter ( object_requests_scraping ) :
    try :
        return crawl_website ( object_requests_scraping )
    except :
        return "NaN"











