from newspaper import Article
import datefinder as dtf
from pandas import read_csv

# file that contains mapping from abbreviations to their expansions
abbrev_fname = 'abbrev.csv'

def isfloat(value):
    """
        Check if the value is a float.
        :param value: Value to check
        :returns: Boolean
    """
    
    try:
        float(value)
        return True
    
    except ValueError:
        return False

def isint(value):
    """
        Check if the value is a int.
        :param value: Value to check
        :returns: Boolean
    """
    
    try:
        int(value)
        return True
    
    except ValueError:
        return False

def parse_date_in_article(article_text):
    """
        Replace dates as required in the extracted text; ex: 12th Aug => <date>12th Aug</date>
        :param article_text: Text of the article (modified by adding expansions)
        :returns: Modified text
    """
    
    # parsing the dates in the text
    matches = dtf.find_dates(article_text, source=False, index=True)
    try:
        offset = 0
        # iterating over matches
        for (match, idx) in matches:
            datestr = article_text[idx[0] + offset:idx[1] + offset]
            datestr = datestr.strip()
            # replacing the dates
            if not isint(datestr) and not isfloat(datestr): #  A small hack since the lib picks up numeric values
                mdatestr = ' <date>' + datestr + '</date> '
                article_text = article_text.replace(datestr, mdatestr)
                offset += len(mdatestr) - len(datestr)
                
    except Exception as exp:
        None
    return article_text
        
def parse_abbrev_in_article(article_text, abbrev_dict):
    """
        Replace abbreviations with their expansions in the extracted text
        :param article_text, abbrev_dict: Text of the article & dictionary of abbreviations
        :returns: Modified text
    """
    
    # iterating over words to check for abbreviations
    for word in article_text.split(' '):
        # replacing the abbreviations
        if word in abbrev_dict and word != 'a': # A small hack for excluding 'a'
            abbrev_word = '<say-as text="' + abbrev_dict[word] + '"></say-as>'
            article_text = article_text.replace(word, abbrev_word)
    article_text = parse_date_in_article(article_text)
    return article_text

def extract_data_using_newspaper(link):
    """
        Given a link,download it and extract all required data wrt that link.
        Uses Newspaper3k to get the data
        :param link: The URL to download and extract
        :returns: dictionary of relevant data per article or empty dict if error occurs
    """

    try:
        # reading csv for abbreviations
        abbrev_dict = read_csv(abbrev_fname, index_col=0, header=None, squeeze=True).to_dict()
        article = {}
        # download the article
        a = Article(link)
        a.download()
        # if successful, parse the article
        if a.download_state == 2:
            a.parse()
        else:
            return {}
        article['body'] = parse_abbrev_in_article(a.text, abbrev_dict)
        return article
    
    except Exception as ex:
        return {}