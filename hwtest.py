from os import scandir,listdir,remove
from bs4 import BeautifulSoup
import pickle 
from nltk.tokenize import word_tokenize
#from nltk.stem import PorterStemmer 
import json
import re
import operator
import time
import sys
import math

search_list = {'p','h1','h2','h3','h4','h5','h6','b',
               'strong','i','em','mark','small','del','ins'}
exceptions = {'<DirEntry \'grape_ics_uci_edu\'>', '<DirEntry \'cbcl_ics_uci_edu\'>',
                '<DirEntry \'mdogucu_ics_uci_edu\'>'}

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
        self.data.clear()

class InvertedIndex:
    def __init__(self,db):
        self.words = dict();
        self.index = db;
        self.num_of_docs = 0
        self.idnum = 1

    def __repr__(self):
        return str(self.index)

    def word_Scores(self, word):
        dict_size = len(self.words)
        tf = (self.words[word] / dict_size)
        idf = 0
        try:
            idf = math.log((self.num_of_docs/len(self.index.returnDict()[word])))
        except:
            idf = math.log(self.num_of_docs/1)
        finally:
            tf_idf = tf * idf

        return tf_idf
                
    def indexDoc(self,Document):
        global search_list
        file = open(Document, 'r')
        data = json.load(file)
        soup = BeautifulSoup(data['content'], "lxml")
        raw = soup.get_text()
        all_tokens = word_tokenize(raw)
        self.num_of_docs +=1
        for t in all_tokens:
            t = t.lower()
            if re.search("(?:[a-zA-Z]+['-][a-zA-Z]+)|([a-zA-Z]+)", t):
                if t in self.words:
                    self.words[t] += 1
                else:
                    self.words[t] = 1
                
        if len(self.words) != 0:
            for word in self.words.keys():
                freqs = self.word_Scores(word)
                new_data = Postings(self.idnum,freqs,data['url'])
                self.index.addToDict(word,new_data)
            self.idnum += 1
            self.words.clear()
            if sys.getsizeof(self.index.returnDict()) >= 5000000:
                print('reached!')
                self.index.offloadData()
                self.index.wipeDict()         
        file.close()



    def returnIndex(self):
        return self.index.returnDict()

class Postings:

    def __init__(self,docid, tfidf, url):
        self.docid = docid
        self.tfidf = tfidf
        self.url = url

    def __repr__(self):
        return 'Posting({docid}, {tfidf}, {url})'.format(docid = self.docid, tfidf = self.tfidf, url=self.url)

    def __str__(self):
        return 'DocID# {docid}\t|tf-idf: {tfidf}\t|url: {url}'.format(docid = self.docid, tfidf = self.tfidf, url=self.url)

    def returnInfo(self):
        return self.docid,self.tfidf

    def getTFIDF(self):
        return self.tfidf

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
        
