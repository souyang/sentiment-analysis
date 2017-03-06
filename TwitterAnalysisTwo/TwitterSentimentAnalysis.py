import sys
import urllib2
import datetime as dt
from bs4 import BeautifulSoup  
import tweepy
from tweepy.auth import OAuthHandler
from SentimentAnalysis import Senti
from Celebrity import Celebrity


def main():
    # use beautifulsoup to parse the information from the IMDB website
    user = validate_credentials()
    if(user == False):
        return;
    celebrity_list = get_celebrity_list()
    #print search_words
    search_and_analysis_tweets(celebrity_list)
      
def validate_credentials():
    global api
    consumer_key = 'TnQSyBoTI79UOBGdQXf5QuXSI'
    consumer_secret = '6cc52SUqayfUsiDlzJM9jmCJYeNFERgPVHJgoVosMFVSSabV5h'
    access_token = '3041260224-LBgb9DAMYv91bfdiaudVQsKQb4evLgG5GVQy7fm'
    access_secret = 's0Xhe7JImRx7fNrlYuHXHHlxyF14hKzdvv220VLlyjcKe'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth);
    if(api == False):
        print("twitter credential verification failed.")
    else:
        print("twitter credential verification successful.")
    return api.verify_credentials();
# this method is to write the final sentiment analysis result to final_output.txt"


# this method is to get the top 10 Celebrity' birthday by performing web scrapping on imdb page    
def get_celebrity_list():
    #global search_words_list
    # get today's date
    todaydate = dt.date.today().strftime("%m-%d")
    #this is t
    url = 'http://www.imdb.com/search/name?birth_monthday=' + todaydate
    test_url = urllib2.urlopen(url)
    readHtml = test_url.read()
    test_url.close()
    soup = BeautifulSoup(readHtml, "html.parser")
    #print(soup.prettify())
    count = 0
    # Fetching the value present within tag results
    movies = soup.findChildren('table', 'results')
    # Changing the movie into an iterator
    iterperson = iter(movies[0].findChildren('tr'))
    # Skipping the first value of the iterator as it does have the required info
    next(iterperson)
    search_words_list = []
    celebrityList = []
    print 'Celebrity Birthday is: ' + todaydate
    for tr in iterperson:
        if count < 10:
            # Fetching image Url for the movie
            imgSource = tr.findChildren('td', 'image')[0].find('img')['src'].split('._V1.')[0] + '._V1_SX214_AL_.jpg'
            # Fetching the name of person
            name = tr.findChildren('td', 'name')[0].find('a').contents[0]
            search_words_list.append(name)
            # Fetching the profession
            profession = tr.findChildren('td', 'name')[0].find('span','description').contents[0].split(',')[0]
            # Fetching the best work
            bestwork= tr.findChildren('td', 'name')[0].find('span','description').find('a').contents[0]
            # create single Celebrity object
            singleCelebrity = Celebrity(name.encode("utf-8"), imgSource.encode("utf-8"), profession.encode("utf-8"), bestwork.encode("utf-8"))

            celebrityList.append(singleCelebrity);
            count += 1
        else: 
            break         
    return celebrityList
# this method is to search the historic tweets via Twitter Search API and perform the sentiment analysis based on the tweets content
def search_and_analysis_tweets(celebrity_list):
    global api
    
                 
    print('******************************* Overall sentiment analysis start ******************************* ')
    #set tweets for individuals
    for indiv in celebrity_list:
        tweets_list = search_tweets(indiv.get_name())
        indiv.set_tweets(tweets_list)       
    Senti.sentiment_analysis_by_rules(celebrity_list)
    print('******************************* Overall sentiment analysis done******************************* ')
    sys.exit()
    
def search_tweets(search_string):
    total_tweets_threshold = 50
    tweets_list = []
    global api
    try:
        tweets = api.search(q=search_string, result_type='recent', lang='en', count=total_tweets_threshold)       
        for tweet in tweets:
            tweets_list.append(tweet.text)
        return tweets_list 
    except Exception, e:
        print 'search tweets failed' + e  
        return None
        
main() 
