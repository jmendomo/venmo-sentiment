#===============================================================================
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
