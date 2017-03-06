class Celebrity:
    _tweets = []
    def __init__(self, name, imgSource, profession, bestwork):
        self.name = name
        self.imgSource = imgSource
        self.profession = profession
        self.bestwork = bestwork
    
    def display_celebrity(self):
        print self.name+"," +  self.profession + "," + self.bestwork+ ","  + self.imgSource
        
    def return_celebrity_info(self):
        return self.name +"," +  self.profession + "," + self.bestwork + ","  + self.imgSource
    
    def get_name(self):
        return self.name
    
    def get_profession(self):
        return self.profession
    
    def get_image_link(self):
        return self.imgSource
    
    def get_best_work(self):
        return self.bestwork
    
    def get_tweets(self):
        return self._tweets
    
    def set_tweets(self, tweets):
        self._tweets = tweets
        