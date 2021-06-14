'''
This is purely an EDA project , where in I would be drawing inferences on what advices 
I can provide to a person who plans on deploying an app on playstore.

The various columns originally present alongwith their descriptions are as follows -

1.  App            - Application name
2.  Category       - Category the app belongs to
3.  Rating         - Overall user rating of the app (as when scraped)
4.  Reviews        - Number of user reviews for the app (as when scraped)
5.  Size           - Size of the app (as when scraped)
6.  Installs       - Number of user downloads/installs for the app (as when scraped)
7.  Type           - Paid or Free
8.  Price          - Price of the app (as when scraped)
9.  Content Rating - Age group the app is targeted at - Children / Mature 21+ / Adult
10. Genres         - An app can belong to multiple genres (apart from its main category). 
                     For eg, a musical family game will belong to Music, Game, Family genres.
11. Last Update
12. Current Ver
13. android Ver
'''

import pandas as pd
import numpy as np
#missing_values = ["n/a","na",np.nan]

#importing datset
dataset = "C:/Users/HIMANSHU GUPTA/Data analysis folder/google play store_data_analysis/Google PlayStore.csv"
GooglePlayStore_dataset = pd.read_csv(dataset)

#copying data into df dataframe.
df =GooglePlayStore_dataset.copy()

#checking info of datset
#df.info()

# finding unique values in each column.
# df.apply(lambda x: len(x.unique()))

# counting values of each category
def value_count_by_category(x,y):
    for i in y:
        print("value of this category:",i)
        print(x[i].value_counts())

# selected_column =['CONTENT RATING']
# value_count_by_category(df,selected_column)

######### EDA
######################## cleaning #############################################

# droping specific row.
df = df.drop(df[df['Last Updated'] =='1.0.19'].index,axis = 0)

######## dropping duplicate values.

# checking duplicates values.
# df1 = df.loc[df.duplicated(keep = False),:].sort_values(by = '')
# droping duplicate values 
df = df.loc[df.drop_duplicates(inplace = True),:]

###### converting col. to upper case

# converting lower str columns features into upper str.
df.columns = [col.upper() for col in df]

############# category column

# doing spliting in category column and converting rows into lower case.
df['CATEGORY'] = df['CATEGORY'].apply(lambda x: x.title().replace('_',' '))

# sorting and checking unique values in category column.
# df1 = df.sort_values(by = 'CATEGORY')
# df2 = df1.CATEGORY.unique()

############ installs column 

# doing spliting and type change in installs column
df['INSTALLS'] = df['INSTALLS'].apply(lambda x: x.split('+')[0])
df['INSTALLS'] = df['INSTALLS'].apply(lambda x: x.replace(',',''))
df['INSTALLS'] = df['INSTALLS'].astype('int')

########### price column

# doing spliting and type change in Price column - convert into indian currency
df['PRICE'] = df['PRICE'].apply(lambda x: x.replace('$','')) 
df['PRICE'] = df['PRICE'].astype('float')

######### dropping columns.

# droping current ver, android ver, GENRES columns.
drop_column = ['CURRENT VER','ANDROID VER','GENRES','LAST UPDATED']
df = df[df.drop(drop_column,inplace = True, axis = 1)]

########## reviews column

# doing type change in reviews column
df['REVIEWS'] = df['REVIEWS'].astype('int')

########## content rating

# doing spliting and type change in content rating column 
df['CONTENT RATING'] = df['CONTENT RATING'].apply(lambda x: x.replace('Adults only 18+','Mature 17+')).replace('Everyone 10+','Teen')
df['CONTENT RATING'] = df['CONTENT RATING'].replace(to_replace = ['Unrated'], value = [np.nan])
df['CONTENT RATING'] = df['CONTENT RATING'].astype('str')
df['CONTENT RATING'] = df['CONTENT RATING'].apply(lambda x: x.split('17+')[0])
df['CONTENT RATING'] = df['CONTENT RATING'].str.strip()

######### size column 

# doing spliting and type change in size column
df['SIZE'] = df['SIZE'].apply(lambda x: x.replace('M',''))

# df['SIZE'].apply(lambda x: x.find('k')).value_counts()
# df.loc[df['SIZE'].str.contains('k'),'SIZE'] = '0'

# checking particular value in size column
# df[df.SIZE == 'Varies with device'] # 1526 values 
# df['SIZE']= df['SIZE'].replace(to_replace = ['Varies with device'],value = [np.nan])

df['SIZE'] = df['SIZE'].map(lambda x: str(round((float(x.rstrip('k'))/1024), 1)) if x[-1]=='k' else x)
df['SIZE'] = df['SIZE'].map(lambda x: 0 if x.startswith('Varies') else x)
df['SIZE'] = df['SIZE'].astype('float')

######## type column

# creating dummies of type column 
dummies = pd.get_dummies(df.TYPE)
# concatenating dummies, df. 
df = pd.concat([df,dummies],axis = 1)

# dropping type column.
# df = df[df.drop('TYPE',inplace = True,axis = 1)] 

####### rating column

# changing data type of rating column.
df['RATING'] = df['RATING'].astype('str')

####### grouping and aggregating 

# grouping values and aggregating reviews column values.
column = ["APP","CATEGORY","SIZE","PRICE","CONTENT RATING","TYPE","INSTALLS",
          "RATING",'Free','Paid']

# checking total duplicate values in dataset. 
# df1 = df.loc[df.duplicated(subset = column,keep = False),:]
# df2 = df1.set_index(column).sort_values(by = "APP")

summary = {'REVIEWS':'mean'}

# grouping values and aggregating in reviews.
df = df.groupby(by = column).agg(summary).sort_values(by = 'APP').reset_index()
# total rows dropped => 10357 -> 9757

# checking again for any lefted duplicate value.
# df1 = df.loc[df.duplicated(subset = column,keep = False),:]

############### changing data type of specific column again.

# rating column
df['RATING'] = df['RATING'].astype('float')

########### dropping column

# dropping app column
df = df[df.drop('APP',inplace = True, axis = 1)]

########### finding outliers
# there is no need to find outliers in this dataset.
 
####### filling nan 

# rating column
df['RATING'] = df['RATING'].interpolate(method = 'ffill')
df['RATING'] = df['RATING'].interpolate(method = 'bfill')

# making new csv file.
df.to_csv(r'C:/Users/HIMANSHU GUPTA/Data analysis folder/google play store_data_analysis/Google PlayStore_cleaned_dataset.csv',index=False)

