import sys
import re, collections
import pandas as pd
from konlpy.tag import Twitter,Kkma

word_lists = []


search = open('bad_Emotional_Word_Dictionary_RES_v1.2.txt', encoding='utf-8')
search_list = search.read()
search_list = search_list.split('\n')
search_list = search_list[30:-1]
for sl in search_list:
    word = sl.split('\t')[2]
    word= re.sub('/[a-zA-Z]*', '', word)
    if word == '':
        continue
    word_lists += [[word]]


search = open('good_Emotional_Word_Dictionary_RES_v1.2.txt', encoding='utf-8')
search_list = search.read()
search_list = search_list.split('\n')
search_list = search_list[30:-1]
for sl in search_list:
    word = sl.split('\t')[2]
    word= re.sub('/[a-zA-Z]*', '', word)
    if word == '':
        continue
    word_lists += [[word]]

lexi3 = pd.read_csv('lexicon3.csv', encoding='cp949' )
lexi3 = lexi3.iloc[:,1:]
lexi3.columns = ['0','1','3','4','6','7']

for i in lexi3:
    for le in lexi3[i]:
        if type(le) == float:
            continue
        word_lists +=[[(i+le)]]

word_dic = {}
for i in ['0','1','3','4','6','7']:
    word_dic[i] = []


numbers = [str(i) for i in range(10)]

for w in word_lists:
    if w[0][0] in numbers:
        word_dic[w[0][0]]+=[w[0][1:]]

input_s = sys.argv ## input

twi=Twitter()
kkm = Kkma()
count=0
comment_list = []
for s in input_s:
    comtemp = [s]
    s_nltk = twi.morphs(comtemp[0])+kkm.morphs(comtemp[0])
    for k in word_dic.keys():
        for i in range(len(word_dic[k])):
            if word_dic[k][i] in s_nltk:
                comtemp+=[k]
    comment_list+=[comtemp]
    count+=1


new_comlist=[]
emo_naming = ['0', '1', '3', '4', '6', '7']
for c in comment_list:
    if len(c)>1:
        count = collections.Counter(c[1:])
        emo_count = len(c)-1
        
        new_c = [c[0]]
        
        highest = [-1, None]
        for nnnn in emo_naming:
            if nnnn in count.keys():
                new_c += [count[nnnn]/emo_count]
                if new_c[-1] > highest[0]:
                    highest[0] = new_c[-1]
                    highest[1] = nnnn
            else:
                new_c +=[0]

            continue
        new_c +=[highest[1]]

        new_comlist+=[new_c]
    else:
        new_comlist +=[c[0]]

if new_comlist[0][-1] == '0':
    print(['laugh'])
elif new_comlist[0][-1] == '1':
    print(['love'])
elif new_comlist[0][-1] == '3':
    print(['shock'])
elif new_comlist[0][-1] == '4':
    print(['shock'])
elif new_comlist[0][-1] == '6':
    print(['sad'])
elif new_comlist[0][-1] == '7':
    print(['angry'])
else :
    print(['angry'])


total = 0
for i in range(len(new_comlist)):
    if str(new_comlist[i][0][0]) == new_comlist[i][-1]:
        total +=1


