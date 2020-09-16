import codecs
import re

import unicodedata

from bs4 import BeautifulSoup

def text_whitout_accents_and_lower(text):
    """
    This function normalizes the text
    Parameters
    ----------
    text : str.
    Returns
    -------
    text_out : str
        DESCRIPTION.
    """
    text_out = re.sub("'"," ", text )
    text_out = unicodedata.normalize("NFKD", text_out).encode("ascii", "ignore").decode()
    text_out = text_out.lower()
    return text_out

def cleaner(text) :
    """
    Remove html tags.

    Parameters
    ----------
    text : string

    Returns
    -------
    string.

    """
    html = text
    try:
        soup = BeautifulSoup(html,'html.parser')
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        text = re.sub('\s+', ' ', text)

        text = re.sub('\xa0', ' ', text)
        text = re.sub('\x83', ' ', text)
        text = re.sub('\x80', 'EUR ', text)
        text = re.sub('\x99', ' ', text)
        text = re.sub('\n', ' ', text)
        text = text_whitout_accents_and_lower(text)

    except:
        text = " "

    return(text)
