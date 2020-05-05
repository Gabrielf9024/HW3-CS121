from os import scandir
from bs4 import BeautifulSoup
import json
import re
import operator
import time

def printGUI():
    print('First Milestone') 
    return input('Search: ')

class InvertedIndex:
    def __init__(self):
        self.words = dict();
        self.index = dict();

    def __repr__(self):
        return str(self.index)

    def freq(self):
        return max(self.words.items(),key=operator.itemgetter(1))[0]
        

    def indexDoc(self,Document):
        file = open(Document, 'r');
        data = json.load(file)
        soup = BeautifulSoup(data['content'], 'html.parser');
        for word in re.findall(r"(?:[a-zA-Z]+[\'][a-zA-Z]+|[^\s\W_][a-zA-Z0-9]*)",soup.get_text().lower()):
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1
                
        if self.words != dict():
            index = self.freq()
            self.words = dict()
            if index in self.index:
                self.index[index].append(data['url'])
            else:
                self.index[index] = [data['url']]
        file.close()

    def returnDict(self):
        return self.index

if __name__ == '__main__':
    path = printGUI()
    start_time = time.time()
    db = InvertedIndex()
    for directory in scandir(path):
        print(directory)
        for file in scandir(directory):
            db.indexDoc(file)
            
    file = open('output.txt','w')
    index = db.returnDict()
    for key in index.keys():
        file.write( str(key) +": "+str(index[key]) + "\n")
    file.close
    
    print(db)
    print('--- %s seconds ---' % (time.time() - start_time))
        
