import statistics as stt
import matplotlib.pyplot as plt
import emoji

#ordeing numbers in list in desceding order
def sortSecond(val):
    return val[1]

#finding variance of a list
def find_s(lists):
    sum_list = []
    x_mean = stt.mean(lists)
    for l in range(len(lists)):
        var_1 = lists[l] - x_mean
        var_1 = var_1**2
        sum_list.append(var_1)
    return sum(sum_list)/len(lists)

#finding t-value between lists (multiple t-test)
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

#plotting multiple time conditions against each other
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
    
#sentiment bars based on time condition
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
    
#assign emoji score based on emoji name        
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

#finding frequent 1-itemset
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
        
