import pickle
from hwtest import Postings
import operator

def ToFile():        
    index = open('finalOutput.pkl', 'rb')
    target = open('Index.txt', 'w')
    dicts = pickle.load(index)

    for key in dicts.keys():
        target.write((key + ':' + str(dicts[key]) + '\n'))

    index.close()
    target.close()

def PrettyToFile():
    def ListNewline(l: list(), tab = True) -> str:
        answer = ''
        for item in l:
            if tab: answer += '\t'
            answer += str(item) + '\n'
        answer += '-' * 160 + '\n'
        return answer
            
    index = open('finalOutput.pkl', 'rb')
    target = open('PrettyIndex.txt', 'w')
    dicts = pickle.load(index)

    for key in dicts.keys():
        target.write((key + ':\n' + ListNewline(dicts[key]) + '\n'))

    index.close()
    target.close()

if __name__ == '__main__':
    ToFile()
    PrettyToFile()
