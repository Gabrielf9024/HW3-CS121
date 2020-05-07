from os import scandir,listdir,remove
from bs4 import BeautifulSoup
import pickle 
#from nltk.tokenize import word_tokenize
#from nltk.stem import PorterStemmer 
import json
import re
import operator
import time
#import math

def printGUI():
    print('First Milestone') 
    return input('Search: ')

class Database:
    def __init__(self):
        self.offload = 0
        self.data = dict()
        self.files = list() 

    def addToDict(self, word, Postings):
        if word in self.data:
            self.data[word].append(Postings)
        else:
            self.data[word] = [Postings]
                                     
    def size(self):
        return len(self.data)

    def returnDict(self):
        return self.data

    def __repr__(self):
        return str(self.data)

    def offloadData(self):
        filename = 'offloadedData' + str(self.offload) + '.pkl'
        self.files.append(filename)
        file = open(filename, 'wb')
        self.offload += 1
        sorted_dict = dict(sorted(self.data.items(), key = lambda x:x[0]))
        pickle.dump(sorted_dict,file)
        file.close()
        
    def wipeDict(self):
        self.data = dict()

class InvertedIndex:
    def __init__(self,db):
        self.words = dict();
        self.index = db;
        self.num_of_docs = 0
        self.idnum = 1

    def __repr__(self):
        return str(self.index)

    def word_Scores(self):
        return max(self.words.items(),key=operator.itemgetter(1))[0]
                
    def indexDoc(self,Document):
        file = open(Document, 'r');
        data = json.load(file)
        #ps = PorterStemmer()
        soup = BeautifulSoup(data['content'], "lxml");
        self.num_of_docs +=1
        for word in re.findall('[a-zA-Z]+', soup.get_text().lower()):
            #stem_word = ps.stem(word)
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1
                
        if len(self.words) != 0:
            index = self.word_Scores()
            
            self.index.addToDict(index,Postings(self.idnum,self.words[index]).returnInfo())
            self.idnum += 1
            self.words = dict()
            if self.index.size() == 250:
                print('reached!')
                self.index.offloadData()
                self.index.wipeDict()         
        file.close()

    def returnIndex(self):
        return self.index.returnDict()

class Postings:

    def __init__(self,docid, tfidf):
        self.docid = docid
        self.tfidf = tfidf
        #self.url = url

    def returnInfo(self):
        return self.docid,self.tfidf

    #def returnUrl(self):
        #return self.url
        

if __name__ == '__main__':
    path = printGUI()
    start_time = time.time()
    db = Database()
    index = InvertedIndex(db)
    for directory in scandir(path):
        print(directory)
        for file in scandir(directory): 
            index.indexDoc(file)
    print(' Final Index')
    file_name = 'offloadedData' + str(index.index.offload) + '.pkl'
    file = open(file_name,'wb')
    pickle.dump(index.returnIndex(),file)
    file.close()
    print('Merging Files')
    list_of_files = listdir()
    final_index = dict()
    for file in list_of_files:
        if re.search('offloadedData',file) != None:
            data_file = open(file,'rb')
            file_dict = pickle.load(data_file)
            for key in file_dict.keys():
                if key in final_index:
                    final_index[key].extend(file_dict[key])
                else:
                    final_index[key] = file_dict[key]
            data_file.close()
            remove(file)
            
    final_output = open('finalOutput.pkl','wb')
    pickle.dump(final_index,final_output)
    final_output.close()
               
    print('--- %s seconds ---' % (time.time() - start_time))
        
