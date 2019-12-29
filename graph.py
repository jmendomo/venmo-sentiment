from config import *
from emoji_lex import *
from functions import *
from data_transf import *

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
                             
#===========================================================
#Plotting graphs and printing t-test results

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
print('\nt-test based on month\n')
for item in t_results.keys():
    if t_results[item][1]<0.05:
        print(item, t_results[item])

t_list = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
t_results = run_t_tests(t_list)
print('\nt-test based on day of the week\n')
for item in t_results.keys():
    if t_results[item][1]<0.05:
        print(item, t_results[item])

t_list = []
for i in range(24):
    exec('t_list.append(h_{})'.format(i))
t_results = run_t_tests(t_list)
print('\nt-test based on hour of the day (UTC)\n')
for item in t_results.keys():
    if t_results[item][1]<0.05:
        print(item, t_results[item])
        
t_list = []
for i in range(1, 32):
    exec('t_list.append(d_{})'.format(i))
t_results = run_t_tests(t_list)
print('\nt-test based on day of the month\n')
for item in t_results.keys():
    if t_results[item][1]<0.05:
        print(item, t_results[item])
