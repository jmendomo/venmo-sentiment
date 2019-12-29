from bs4 import BeautifulSoup
from urllib.request import urlopen

#creating a lexicon (dictionary) mapping emoji characters to their sentiment scores

#=========================================================
#scrapping data from emoji sentiment ranking webpage
url = "http://kt.ijs.si/data/Emoji_sentiment_ranking/"
content = urlopen(url).read()
soup = BeautifulSoup(content)


char = []
test_count = 0
for td in soup.find_all('td'):
    if test_count == 1:
        char.append(td.string)
        test_count = -11 
    test_count +=1

ima = []
test_count = 0
for td in soup.find_all('td'):
    if test_count == 0:
        ima.append(td.string)
        test_count = -12
    test_count +=1

e_score =[]
test_count = 0
for td in soup.find_all('td'):
    if test_count == 8:
        e_score.append(td.string)
        test_count = -4  
    test_count +=1

e_name =[]
test_count = 0
for td in soup.find_all('td'):
    if test_count == 10:
        e_name.append(td.string)
        test_count = -2
    test_count +=1

   
#initializing emoji sentiment lexicon    
score_dict ={}
for i in range(len(ima)):
    score_dict[ima[i]] = float(e_score[i])
    score_dict[char[i]] = float(e_score[i])
    score_dict[e_name[i]] = float(e_score[i])
