import pickle
from hwtest import Postings
import operator
def dumpinto():
    file = open('finalOutput.pkl','rb')
    dicts = pickle.load(file)
    largest_index = -100000
    min_index = 100000000000
    number_indexed = 0
    unique_indexes = []
    lword = None
    mword = None
    for key in dicts.keys():
        if len(dicts[key]) > largest_index:
            largest_index = len(dicts[key])
            lword = key
        if len(dicts[key]) <  min_index:
            min_index = len(dicts[key])
            mword = key
        if len(dicts[key]) ==  1:
            unique_indexes.append(key)
        number_indexed += len(dicts[key])
    freq = 0
    for x in dicts[lword]:
        freq += x.tfidf
    print('Index size: ' + str(len(dicts)))
    print('Sites Indexed: ' + str(number_indexed))
    print('largest word: ' + str(lword) + '; count: '  + str(freq))
    print('smallest word: ' + str(mword) + ' count: '  + str(min_index))
    print('unique indexes: '+ str(len(unique_indexes)))
    
    file.close()

dumpinto()
