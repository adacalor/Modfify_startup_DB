import logging
import re

import requests
from random import randint
from bs4 import BeautifulSoup

from cleaner import cleaner

from urllib.parse import urljoin

#requests.get('https://www.addevmaterials.fr/',verify = True)
#requests.get('https://www.addevmaterials.fr/',verify = False)


liste_user_agent = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
]

liste_terme = ["about",
               "company",
               "corporate",
               "industries",
               "solution",
               "a-propos",
               "en-quelques-mots",
               "entreprise",
               "equipe",
               "innovation",
               "nos-services",
               "professionnel",
               "qui-nous-sommes",
               "service",
               "societe"]


def requests_scraping(website):
    url_web = "{}".format(website)
    #logging.info(url_web)
    data_website = {
            "url_website": website,
            "description": "NaN"
            }

    try:
        user_agent = liste_user_agent[randint(0, len(liste_user_agent))]
    except:
        user_agent = liste_user_agent[0]

    ####
    try:
        #html_orig = requests.get(website, timeout=2, headers={'User-Agent': user_agent})
        html_orig = requests.get(website, timeout=2, headers={'User-Agent': user_agent})
        bsObj = BeautifulSoup(html_orig.content, 'html.parser')
        tab_descr = []
        content_page_1 = cleaner(html_orig.content)
        if len(content_page_1) > 5:
            tab_descr.append("{}".format(content_page_1))
            tab_link = []
            Liste_des_liens = bsObj.find_all("a", href=True)
            for url in Liste_des_liens:
                lien = url.attrs["href"]
                for terme in liste_terme:
                    if ((terme in lien) and not ("linkedin.com" in lien) and not ("twitter" in lien)):
                        tab_link.append(url.attrs["href"])

            for link in list( set(tab_link) )[0:100]:
                verif_link = re.findall("http", link)
                if verif_link:
                    html = requests.get(link, timeout=1, headers={'User-Agent': user_agent})
                    content = cleaner(html.content)
                    if content:
                        tab_descr.append("{}".format(content))
                else:
                    #correct_link = "{}{}".format(website, link)
                    correct_link = urljoin( html_orig.url, link )
                    try:
                        html = requests.get(correct_link, timeout=1, headers={'User-Agent': user_agent})
                        content = cleaner(html.content)
                        if content:
                            tab_descr.append("{}".format(content))
                    except:
                        correct_link = re.sub("http", "https", correct_link)
                        try:
                            html = requests.get(correct_link, timeout=1, headers={'User-Agent': user_agent})
                            content = cleaner(html.content)
                            if content:
                                tab_descr.append("{}".format(content))
                        except:
                            #logging.info("Error link" + str(correct_link))
                            pass
                    

            data_website = {
                "Status": str(html_orig),
                "url_website": website,
                "description": " ".join(tab_descr)
            }
            print("Successfully scraped " + website + " with requests")

    except requests.exceptions.RequestException as error_connection:
        error = str(error_connection).split(":")
        verif_error = re.findall("No address associated | Name or service not known", str(error_connection), re.IGNORECASE)
        if verif_error:
            data_website = {
                "Status": error[-1],
                "url_website": website,
                "description": "NaN"
            }

    return data_website
