import pandas as pd

TrendsFilepath = "/Users/petrandreev/Desktop/leSnack/Trends.csv"
RawDataFilepath = "/Users/petrandreev/Desktop/leSnack/RawData.csv"
MixingInfoFilepath = "/Users/petrandreev/Desktop/leSnack/MixingInfo.csv"

trends_data = pd.read_csv(TrendsFilepath)
mix_data = pd.read_csv(MixingInfoFilepath)
raw_data = pd.read_csv(RawDataFilepath)


#columns WRLM_TT8501_Value  WRLM_TT8502_Value
#filling the columns with the corresponding values from other dataset
temperature_dict = {}
time_dict = {'12 PM':'00', '1 AM':'01','2 AM':'02','3 AM':'03','4 AM':'04','5 AM':'05','6 AM':'06','7 AM':'07','8 AM':'08','9 AM':'09','10 AM':'10',
            '11 AM':'11','12 AM':'12','1 PM':'13','2 PM':'14','3 PM':'15','4 PM':'16','5 PM':'17','6 PM':'18','7 PM':'19','8 PM':'20','9 PM':'21','10 PM':'22','11 PM':'23'}
month_dict = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
print(trends_data.columns)
for index, row in trends_data.iterrows():
    x = row['DateTime']
    x = x.split()
    date = x[0]
    month = date[7:-3]
    month = month_dict[month]
    date = date[4:-6] + month + '/19'
    #print(date)
    time = x[1]
    time = time.split(':')
    time = time[0]
    time_val = time_dict[time+' '+x[2]]
    date_time = date + ' ' + time_val
    print(date_time)
    temperatures = [row['WRLM_TT8501_Value'], row['WRLM_TT8502_Value']]
    temperature_dict[date_time] = temperatures


bad_responses = ['000395477A','000397596A','000397893A','000408081A','000428757A','000430339A','000429682A','000440594A','000435566A','000441059A','000443286A','000443354A','000442240A','000448316A','000444918A','000444963A','000447676A',
                '000448330A','000443590A','000448323A','000445553A','000448423A','000444910A','000444692A','000443355A','000442299A','000442708A','000446732A','000448047A','000452612A','000451812A','000452190A','000450968A','000450941A',
                '000452366A','000451985A','000452005A','000452034A','000452075A', '000450093A','000450423A','000450082A','000450108A','000450430A','000450431A','000451356A','000450400A','000449528A','000451698A','000450716A','000452191A',
                '000451167A','000450705A','000449894A','000449555A','000449410A','000451146A','000450080A','000450987A','000450969A','000449425A','000453259A','000452328A','000453201A','000451816A','000451813A','000453292A','000450942A',
                '000453102A','000453112A','000451019A','000453182A','000453330A','000453332A','000453659A',
                '000449481A','000449463A','000449216A','000452640A','000452632A','000449863A']

time_date ={'31/07/19':['16'],'01/08/19':['07'],'02/08/19':['07'],'11/08/19':['23'],'13/08/19':['14'],
            '22/08/19':['15'],'23/08/19':['21'],'25/08/19':['07'],'26/08/19':['07'],'27/08/19':['07'],'29/08/19':['21'],'30/08/19':['07']}

for index, row in raw_data.iterrows():
    if row['Ref Number'] in bad_responses:
        if row['Man. Date'] in time_date:
            time_val = row['Man. Time']
            time_val = str(time_val) #rounding to nearest hour
            time_val = time_val[0:2]
            if time_val != 'na':
                time_val = int(time_val)
                if time_val < 10:
                    if time_val < 9:
                        time_valpls = '0' + str(time_val+1)
                    elif time_val == 0:
                        time_valmin = '23'
                    else:
                        time_valmin = '0' + str(time_val-1)
                time_date[row['Man. Date']].append(time_valpls)
                time_date[row['Man. Date']].append(str(time_val-1))
            time_date[row['Man. Date']].append(str(time_val))
        else:
            time_val = row['Man. Time']
            time_val = str(time_val)
            time_val = time_val[0:2]
            time_date[row['Man. Date']] = [time_val]
        
        #time_date.append(row['Man. Date'])#row['Man. Time']])

dummyList = ['N/A']*mix_data.shape[0]
mix_data['Result'] = dummyList
mix_data['filler_temp'] = dummyList
mix_data['kettle_temp'] = dummyList


print(len(time_date),'Currentlen')
counter =0
for index, row in mix_data.iterrows():
    if index %2 == 0:
        dateTimeVar = row['DATETIME']
        days = dateTimeVar.split('/')
        day = int(days[0])
        if day< 10:
            day = '0' + str(day)
        time = row['DISCHARGE TIME']
        time = str(time)
        time = time[0:2]
        if time != 'na':
            #print(time,'before')
            time = int(time)%12
            #print(time,'after')
            if time< 10:
                time = '0' + str(time)
        date_time = str(day) + '/' + str(days[1]) + '/' + str(days[2]) + ' ' + str(time)
        #print(date_time)
        if date_time in temperature_dict:
            values = temperature_dict[date_time]
            if values[0] != 'Null' and values[1] != 'Null':
                print("happened")
                mix_data.at[index,'kettle_temp'] = float(values[1])
                mix_data.at[index,'filler_temp'] = float(values[0])
        else:
            mix_data.drop(index, inplace =True)
        if row['DATETIME'] in time_date:
            time_val = row['DISCHARGE TIME']
            time_val = str(time_val)
            time_val = time_val[0:2]
            if time_val == "na" or time_val == 'nan':
                counter +=1
                mix_data.at[index,'Result'] = 1

            if time_val in time_date[row['DATETIME']]:
                counter +=1
                mix_data.at[index,'Result'] = 1
            else:
                mix_data.at[index,'Result'] = 0
        else:
                mix_data.at[index,'Result'] = 0
    else:
        mix_data.drop(index, inplace=True)



print(temperature_dict)
print(len(bad_responses), "bad responses")
print(mix_data['Result'])
print(counter, 'Counter of ones')
print(mix_data['filler_temp'])
print(mix_data['kettle_temp'])


counter = 0
for index, row in mix_data.iterrows():    
    if row['filler_temp'] != 'N/A' and row['Result'] ==1:
        counter += 1
print(counter)
        

print(len(temperature_dict.keys()))
print(mix_data.columns)
# Delete multiple columns from the dataframe
mix_data = mix_data.drop(columns = [ 'BIN', 'Unnamed: 4', 'RECIPE',
       'PREWEIGH TIME', 'Unnamed: 7', 'Unnamed: 8', 'TASTY CHEESE W',
       'TASTY CHEESE B', 'TASTY CHEESE DB', 'Unnamed: 12',
       'MILD CHEESE B', 'MILD CHEESE DB', 'BUTTER B', 'BUTTER DB', 'WHEY B', 'WHEY DB', 'JOHA S9 W', 'JOHA S9 B', 'JOHA S9 DB',
       'NISAPLIN W', 'NISAPLIN B', 'Unnamed: 27', 'NISAPLIN DB', 'TRUCAL D7 W',
       'TRUCAL D7 B', 'TRUCAL D7 DB', 'OMYABAKE W', 'OMYABAKE B',
       'OMYABAKE DB', 'TASTYMITE W', 'TASTYMITE B', 'TASTYMITE DB',
       'WHITE ONION W', 'WHITE ONION B', 'WHITE ONION DB', 'ROAST ONION W',
       'ROAST ONION B', 'ROAST ONION DB', 'TANGY BBQ W', 'TANGY BBQ B',
       'TANGY BBQ DB', 'NAT SMOKE W', 'NAT SMOKE B', 'NAT SMOKE DB',
       'LESNAK CHEESE W', 'LESNAK CHEESE B', 'LESNAK CHEESE DB', 'JOHAT W',
       'JOHAT B', 'JOHAT DB', 'LACTIC B', 'LACTIC DB',
       'WATER ADDED', 'MAJOR OPERATOR', 'MINOR OPERATOR', 'KETTLE START',
       'COOK RISE',  
       'CCP HOLD TIME', 'CCP NISAPLIN', 'CCP NISAPLIN OPERATOR', 
        'QUALITY OPERATOR', 'VISUAL'])

mix_data.to_csv("/Users/petrandreev/Desktop/leSnack/CombinedData.csv", index=False)
