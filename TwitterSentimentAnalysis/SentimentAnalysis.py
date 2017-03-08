from FinalOutputResult import FinalOutputResult
import re
from nltk.sentiment import vader
from twython import Twython
import os
# this class is to perform the sentiment analysis 
class Senti():
    @staticmethod
    def sentiment_analysis_by_VADER(celebrity_list):
        cwd = os.getcwd()
        output_file_name = cwd+ "/analysis-result/VADER-based-sentiment-analysis-result.txt"
        sia = vader.SentimentIntensityAnalyzer()
        for indiv in celebrity_list:
            final_conclusion = Senti.__vader_analysis(sia, indiv.get_tweets())
            FinalOutputResult.set_final_output(indiv, final_conclusion, output_file_name)
    @staticmethod
    def __vader_analysis(sia, tweets):
        for tweet in tweets:
            scores = sia.polarity_scores(tweet)
            tot_pos = scores['pos']
            tot_neg = scores['neg']
            tot_neu = scores['neu']
        return Senti.__make_judement(tot_pos, tot_neu, tot_neg)
    # this method is to perform the sentiment analysis on tweets for celebrities
    @staticmethod
    def sentiment_analysis_by_rules(celebrity_list):
        positive_words = set()
        negative_words = set()
        cwd = os.getcwd()
        positive_bag_of_words = cwd+"/text-lexicon/positive-words.txt"
        negative_bag_of_words = cwd+"/text-lexicon/negative-words.txt" 
        output_file_name = cwd+"/analysis-result/Naive-Rule-based-sentiment-analysis-result.txt"
        #clear the output file
        try:
            open(output_file_name, 'w').close();
            with open(positive_bag_of_words) as fpostive:            
                for line in fpostive:
                    if str(line).startswith(';') == False:
                        word = str(line).strip().strip('\n');
                        positive_words.add(word)  
                                 
            with open(negative_bag_of_words) as fnegative:
                for line in fnegative:
                    if str(line).startswith(';') == False:
                        word = str(line).strip().strip('\n');
                        negative_words.add(word) 
        except Exception, e:
            print 'reading/writing file failed' + e                
        
        for indiv in celebrity_list:
            final_conclusion = Senti.__simple_rule_based_sentiment_analysis(positive_words, negative_words, indiv.get_tweets())
            FinalOutputResult.set_final_output(indiv, final_conclusion, output_file_name)
    
    @staticmethod
    def __simple_rule_based_sentiment_analysis(positive_words, negative_words, tweets):       
        positive_counts = []
        negative_counts = []
        tot_pos = 0 #positive
        tot_neu = 0 #neutral
        tot_neg = 0 #negative      
        #print tweets_list
        preprocessedTweets = Senti.__preprocessTweets(tweets)
        for tweet in preprocessedTweets:
            positive_counter = 0
            negative_counter = 0
            words = tweet.split(' ')
            emoticons = Senti.__get_emoticons()
            for word in words:
                if word in emoticons: # skip emoticons
                    continue
                if word.startswith('NEG_') == False: #contains negation
                    if word in positive_words:
                        positive_counter = positive_counter + 1
                    elif word in negative_words:
                        negative_counter = negative_counter + 1
                else:
                    keyword = word[4:] # get the real word
                    if keyword in negative_words:
                        positive_counter = positive_counter + 1
                    elif keyword in positive_words:
                        negative_counter = negative_counter + 1                    
            positive_counts.append(positive_counter)
            negative_counts.append(negative_counter)
            if positive_counter > negative_counter:
                tot_pos += 1
            elif positive_counter == negative_counter:
                tot_neu += 0.5
            else:
                tot_neg +=1

        return Senti.__make_judement(tot_pos, tot_neu, tot_neg)
    @staticmethod
    def __make_judement(tot_pos, tot_neu, tot_neg):
        if tot_pos > tot_neg and tot_pos > tot_neu:
            #print "Overall Sentiment - Positive"
            final_conclusion = "Positive"
        elif tot_neg > tot_pos and tot_neg > tot_neu:
            #print "Overall Sentiment - Negative"
            final_conclusion = "Negative"
        elif tot_neg == tot_neu and tot_neg > tot_pos:
            #print "Overall Sentiment - Negative"
            final_conclusion = "Negative"
        elif tot_pos + tot_neg < tot_neu:
            #print "Overall Sentiment - Semi Positive "
            final_conclusion = "Semi Positive"          
        else:
            #print "Overall Sentiment - Neutral"
            final_conclusion = "Neutral" 
        return final_conclusion
    @staticmethod
    def __preprocessTweets(tweets):
        preprocessed_tweets = []
        for tweet in tweets:
            tweet = tweet.decode("utf-8")
            tweet = tweet.strip().strip('\n')
            if not tweet:
                continue
            # 1. Convert to lower case
            tweet=tweet.lower()
            # 2. Replace links with the word URL, we won't need URL for analysis
            tweet=re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)     
            # 3. Replace @username with "AT_USER", we won't need @user  for analysis
            tweet=re.sub('@[^\s]+','AT_USER',tweet)
            # 4. Replace #word with word, we won't need hashtag for analysis
            tweet=re.sub(r'#([^\s]+)',r'\1',tweet)
            # 5. Replace groooovy to groovy
            tweet = Senti.__reduce_length(tweet)
            tweet = Senti.__negation(tweet)
            preprocessed_tweets.append(tweet)
        return preprocessed_tweets  
     
    @staticmethod
    def __negation(tweet):
        tweet_words = tweet.split(' ')
        negation_key_word_set = {"don't", "never", "nothing", "nowhere", "none", "not", "hasn't", "hadn't", "can't", "should't", "won't", "wouldn't", "don't", "doesn't", "didn't", "isn't", "aren't", "ain't"}
        neg_count =[]
        for i in range(len(tweet_words)):
            neg_count.append(0)
        for neg in negation_key_word_set:
            if neg in tweet_words:
                neg_count[i] = neg_count[i] + 1
        for i in range(len(tweet_words)):
            if neg_count[i] % 2 == 1:
                tweet_words[i] = "NEG_" + tweet_words[i]
        return ' '.join(tweet_words)
    
    
    @staticmethod
    def __reduce_length(text):          
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", text)
        
    @staticmethod
    def __get_emoticons():
        emoticons = [':)','(:',': )','( :','=)','(=','= )','( =',':D',': D',':p',': p',':(','):',': (',') :','=(',')=','= (',') =',':D',': D',':p',': p',':-)','(-:',':- )','( -:',':-(',')-:',':- (',') -:']
        emoticons = set(emoticons)
        return emoticons     