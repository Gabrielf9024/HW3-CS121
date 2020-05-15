import pickle
from hwtest import Postings
import operator
import re

def textGUI() -> str:
    'Prints the GUI for query'
    print('Searching in Developer directory')
    return input('Search: ')

    
def search(queries: [str]) -> dict():
    answer = {}
    index = open('finalOutput.pkl', 'rb')
    dicts = pickle.load(index)

    for key in dicts.keys():
        if key in queries:
            answer[key] = dicts[key]

    return answer
    
def PrettyList(l: list()) -> str:
    answer = ''
    for item in l:
        answer += '\t' + str(item) + '\n'
    return answer

if __name__ == '__main__':
    query = textGUI()
    queryList = re.split(' ', query)

    answer = search(queryList)
    for key, value in answer.items():
        value.sort(key= lambda post: post.getTFIDF(), reverse=True)
        print(str(key) + ':\n' + PrettyList(value) )
