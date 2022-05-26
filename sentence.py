class Sentence:
    def init(self):
        self.origin_score = -1
        self.simplified_score= -1
        self.origin_sentence=""
        self.simplified_sentence=""
    
    def set_origin_sentence(self,str):
        self.origin_sentence=str
    
    def set_origin_score(self,score):
        self.origin_score=score
    
    def set_simplified_sentence(self,str):
        self.simplified_sentence=str
    
    def set_simplified_score(self,score):
        self.simplified_score=score