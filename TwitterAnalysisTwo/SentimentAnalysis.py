from FinalOutputResult import FinalOutputResult
# this class is to perform the sentiment analysis 
class Senti():
        
    # this method is to perform the sentiment analysis on tweets for celebrities
    @staticmethod
    def sentiment_analysis_by_rules(celebrity_list):
        positive_words = set()
        negative_words = set()
        positive_bag_of_words = "positive-words.txt"
        negative_bag_of_words = "negative-words.txt" 
        output_file_name = "rule-based-sentiment-analysis-result.txt"
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
        
        for tweet in tweets:
            positive_counter = 0
            negative_counter = 0
            tweet = tweet.encode("utf-8")
            tweet_processed = tweet.lower()

            words = tweet_processed.split(' ')
            for word in words:
                if word in positive_words:
                    positive_counter = positive_counter + 1
                elif word in negative_words:
                    negative_counter = negative_counter + 1
            positive_counts.append(positive_counter)
            negative_counts.append(negative_counter)
            if positive_counter > negative_counter:
                tot_pos += 1
            elif positive_counter == negative_counter:
                tot_neu += 0.5
            else:
                tot_neg +=1

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