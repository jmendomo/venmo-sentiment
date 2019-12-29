import pandas as pd
import numpy as np
import csv
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib.pyplot as plt
import statistics as stt
import emoji
from scipy import stats
import math

#==========================================================================================================================================================
#==========================================================================================================================================================
#constant variables for transaction and graph lists

weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

YEAR = 0
MONTH = 1
DAY_M = 2
DAY_W = 3
TIME = 4
SCORE = 5
EMOJIS = 6
JULY = 0
AUGUST = 1
OCTOBER = 2
Y_19 = 3
Y_18 = 4
for i in range(31):
    exec("D_{} = {}".format(i+1,i+5))
for i in range(len(weekDays)):
    exec("{} = {}".format(weekDays[i].upper(),i+36))
for i in range(24):
    exec("H_{} = {}".format(i,i+44))
    

    
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

   
    
score_dict ={}
for i in range(len(ima)):
    score_dict[ima[i]] = float(e_score[i])
    score_dict[char[i]] = float(e_score[i])
    score_dict[e_name[i]] = float(e_score[i])
    
july = []
august = []
october = []
y_19 = []
y_18 = []


stats_list = [july, august, october, y_19, y_18]

for i in range(31):
    exec("d_{} = []".format(i+1))
    exec("stats_list.append(d_{})".format(i+1))

for i in range(len(weekDays)):
    exec("{} = []".format(weekDays[i].lower()))
    exec("stats_list.append({})".format(weekDays[i].lower()))

for i in range(24):
    exec("h_{} = []".format(i))
    exec("stats_list.append(h_{})".format(i))
    
    
    
venmo_data = []
score_data = []


#==========================================================================================================================================================
#==========================================================================================================================================================
#functions

def sortSecond(val):
    return val[1]

def find_s(lists):
    sum_list = []
    x_mean = stt.mean(lists)
    for l in range(len(lists)):
        var_1 = lists[l] - x_mean
        var_1 = var_1**2
        sum_list.append(var_1)
    return sum(sum_list)/len(lists)

def run_t_tests(lists):
    t_stats = {}
    for i in range(len(lists)):
        if len(lists[i])> 0: 
            x = lists[i]
            for j in range(i+1, len(lists)):
                if len(lists[j])> 0: 
                    y = lists[j]
                    df = len(x) + len(y) -2
                    t = (stt.mean(x)-stt.mean(y))/math.sqrt(find_s(x)/len(x)+find_s(y)/len(y))
                    p = 1 - stats.t.cdf(t, df =df)
                    t_stats['{}-{}'.format(i,j)] = [t,p]
            
    return t_stats


def compare_plot(lists, name, x_labels, y_label):
    if len(lists)>10: plt.rcParams.update({'figure.figsize':(10,10), 'figure.dpi':100})
    else: plt.rcParams.update({'figure.figsize':(10,4), 'figure.dpi':100})
    plt.boxplot(lists, vert=False, labels = x_labels)
    plt.xlabel('Emoji Sentiment Score', fontsize=20)
    plt.ylabel('{}'.format(y_label), fontsize=20)
    plt.grid(axis= 'x', linestyle='--', color='grey')
    plt.axvline(x =0, color='yellow', linestyle='-')
    plt.axvline(x =.2, color='green', linestyle='-')
    plt.axvline(x =-.1, color='red', linestyle='-')
    plt.tight_layout()
    plt.savefig('{}.png'.format(name))
    plt.show()
    

def plot_bar(list_object, title, name):
    pos = []
    neg = []
    neu = []
    
    for i in range(len(list_object)):
        if list_object[i] > -1 and list_object[i] <= -.1:
            neg.append(list_object[i])
        elif list_object[i] > -.1 and list_object[i] <= .2:
            neu.append(list_object[i])
        else:
            pos.append(list_object[i])
    
    plt.rcParams.update({'figure.figsize':(10,4), 'figure.dpi':100})
    plt.hist(pos, bins=17, color = 'green', label = 'positive')
    plt.hist(neu, bins=7, color = 'yellow', label = 'neutral')
    plt.hist(neg, bins=15, color = 'red', label = 'negative')
    plt.axvline(stt.mean(list_object), color='black', linestyle='-', label='mean')
    plt.title('{}'.format(title), fontsize=25)
    plt.xlabel('Emoji Sentiment Score', fontsize=20)
    plt.ylabel('Occurrences', fontsize=20)
    plt.legend()
    plt.tight_layout()
    plt.savefig('{}.png'.format(name))
    plt.show()
    
    
def list_has(obj, lists):
    for i in range(len(lists)):
        if obj in lists[i]:
            return score_dict[lists[i]]
        
def assign_score(emojis):
    x = emoji.demojize(emojis).replace('_',' ').replace(':','').replace(' Medium Skin Tone', '').replace(' Dark Skin Tone', '').replace(' Light Skin Tone', '').replace(' Medium-Dark Skin Tone', '').replace(' Medium-Light Skin Tone', '').title()
    
    if x in e_name: score = [score_dict[x]]
    elif x in countries or 'Flag' in x or 'O’Clock' in x or 'Thirty' in x: score = [0]
    elif 'Dancing' in x: score = [0.734]
    elif 'Heart' in x: score = [0.670]
    elif x == 'Ballot Box With Ballot': score =[-0.667]
    elif x=='Old Woman': score = [0.423]
    elif 'Woman' in x: score=[0.067]
    elif x=='Boy': score = [0.133]
    elif 'Male Sign'==x or 'Female Sign'==x: score = [0.133]
    elif list_has(x, e_name) != []: score = list_has(x, e_name)
    else: score=[]
        
    return score


def freq_set(min_conf, data, freq_item):
    item_set = {}
    y = list(freq_item.keys())
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] in y:
                for k in range(j+1, len(data[i])):
                    if data[i][k] in y:
                        exec("item_set['{}-{}']=0".format(data[i][j], data[i][k]))
                    
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] in y:
                for k in range(j+1, len(data[i])):
                    if data[i][k] in y:
                        exec("item_set['{}-{}']+=1".format(data[i][j], data[i][k]))
                    
    x = list(item_set.keys())
    
    occur = {}
    
    for i in range(len(x)):
        z = x[i].split('-')
        exec("occur['{}']= item_set['{}']/freq_item['{}']".format(str(z[1])+' given '+str(z[0]), x[i], z[0]))
        exec("occur['{}']= item_set['{}']/freq_item['{}']".format(str(z[0])+' given '+str(z[1]), x[i], z[1]))
    
    freq_occur = []
             
    for item in occur.keys():
        if occur[item] >= min_conf:
            freq_occur.append([item, occur[item]])
    
    return freq_occur


def freq_item(min_sup, data):
    item_set = {}
    for i in range(len(data)):
        exec("item_set['{}']=0".format(data[i]))
    
    for i in range(len(data)):
        exec("item_set['{}']+=1".format(data[i]))
    
    x = list(item_set.keys())
    freq_items = []
    
    for i in range(len(x)):
        if item_set[x[i]] >= min_sup*len(data):
            freq_items.append([x[i],item_set[x[i]]])
   
    return freq_items
        
#==========================================================================================================================================================
#==========================================================================================================================================================
#Data Transformation

data = pd.read_csv("complete_database.csv", delimiter=';', names = ['column'])

for i in range(1, len(data['column'])):
    x = data['column'][i].split(',')
    year = int(x[0])
    month = int(x[1])
    day_m = int(x[2])
    day_w = weekDays[datetime.date(year, month, day_m).weekday()]
    time = int(x[3][0:2])
    score = []
    e_list = x[4:]
    emojis = []
    for j in range(len(e_list)):
        if '\u200d' in e_list[j]: emojis+=e_list[j].split('\u200d')
        else: emojis.append(e_list[j])
    
    for j in range(len(emojis)):
        if emojis[j] in ima or emojis[j] in char:
            if score == []:
                score = [score_dict[emojis[j]]]
            else:
                if abs(score[0]) < abs(score_dict[emojis[j]]):
                    score = [score_dict[emojis[j]]]
        else:
            assign_score(emojis[j])
    venmo_data.append([year, month, day_m, day_w, time, score, emojis])
        
    if score != []:
        score_data.append([year, month, day_m, day_w, time, score, emojis])
        if year == 2019:
            y_19+= score
        else:
            y_18+=score
        
        if month == 7:
            july+=score
        elif month == 8:
            august+=score
        else:
            october+=score
        
        if day_w.lower()=='monday':
            monday+=score
        elif day_w.lower()=='tuesday':
            tuesday+=score
        elif day_w.lower()=='wednesday':
            wednesday+=score
        elif day_w.lower()=='thursday':
            thursday+=score
        elif day_w.lower()=='friday':
            friday+=score
        elif day_w.lower()=='saturday':
            saturday+=score
        else:
            sunday+=score
        
        for j in range(1,32):
            statement = 'day_m=={}'.format(j)
            if eval(statement):
                exec('d_{}+=score'.format(j))

        for j in range(24):
            statement = 'time=={}'.format(j)
            if eval(statement):
                exec('h_{}+=score'.format(j))
                
                
#==========================================================================================================================================================
#==========================================================================================================================================================
#Plotting


#To compare different conditions

compare_plot([monday, tuesday, wednesday, thursday, friday, saturday, sunday], 'days_of_week', list(weekDays), 'Day of the Week')

lists = []
x_labels = []
for i in range(1,32):
    exec('lists.append(d_{})'.format(i))
    exec('x_labels.append(str({}))'.format(i))
compare_plot(lists, 'days_of_month', x_labels, 'Day of the Month')

lists = []
x_labels = []
for i in range(24):
    exec('lists.append(h_{})'.format(i))
    exec('x_labels.append(str({}))'.format(i))
compare_plot(lists, 'hours_of_day', x_labels, 'Hour (UTC Time)')

compare_plot([august, july, october], 'month_of_year', ['August', 'July', 'October'], 'Month')


for i in range(7):
    exec("plot_bar({}, '{}', '{}_score')".format(weekDays[i].lower(), weekDays[i].upper(), weekDays[i].lower()))
    
plot_bar(august, 'AUGUST', 'august_score')
plot_bar(july, 'JULY', 'july_score')
plot_bar(october, 'OCTOBER', 'october_score')

for i in range(24):
    exec("plot_bar(h_{}, '{}:00 UTC', '{}_score')".format(i, i, i))
    
for i in range(1,32):
    statement = 'd_{} != []'.format(i)
    if eval(statement):
        exec("plot_bar(d_{}, '{}', 'd{}_score')".format(i, i, i))
        

all_emo = []
all_score = 
for i in range(len(score_data)):
    for j in range(len(score_data[i][EMOJIS])):
        all_emo.append(score_data[i][EMOJIS][j])
freq_emo = freq_item(.005, all_emo)
freq_dayw = freq_item(.05, np.transpose(score_data)[DAY_W])
freq_daym = freq_item(.05, np.transpose(score_data)[DAY_M])
freq_month = freq_item(.1, np.transpose(score_data)[MONTH])
freq_time = freq_item(.01, np.transpose(score_data)[TIME])
            
freq_data = []
for i in range(len(score_data)):
    freq_data.append(score_data[i][0:-2])
    if score_data[i][SCORE][0]>=.2:
        freq_data[i].append('positive')
    elif score_data[i][SCORE][0]>= -.1:
        freq_data[i].append('neutral')
    else:
        freq_data[i].append('negative')
        
freq_score=freq_item(.01,np.transpose(freq_data)[SCORE])

freq_everything = {}
for i in range(len(freq_emo)):
    freq_everything[freq_emo[i][0]] = freq_emo[i][1]
for i in range(len(freq_dayw)):
    freq_everything[freq_dayw[i][0]] = freq_dayw[i][1]
for i in range(len(freq_daym)):
    freq_everything[freq_daym[i][0]] = freq_daym[i][1]
for i in range(len(freq_month)):
    freq_everything[freq_month[i][0]] = freq_month[i][1]
for i in range(len(freq_time)):
    freq_everything[freq_time[i][0]] = freq_time[i][1]
for i in range(len(freq_score)):
    freq_everything[freq_score[i][0]] = freq_score[i][1]
    
freq_conf = freq_set(0.05, freq_data, freq_everything)

t_list = [july, august, october]
t_results = run_t_tests(t_list)
print(t_results)

t_list = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
t_results = run_t_tests(t_list)
print(t_results)

t_list = []
for i in range(24):
    exec('t_list.append(h_{})'.format(i))
t_results = run_t_tests(t_list)
for item in t_results.keys():
    if t_results[item][1]<0.05:
        print(item, t_results[item])
        
t_list = []
for i in range(1, 32):
    exec('t_list.append(d_{})'.format(i))
t_results = run_t_tests(t_list)
for item in t_results.keys():
    if t_results[item][1]<0.05:
        print(item, t_results[item])
