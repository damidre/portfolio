from datetime import date
import pandas as pd

'''
Data Loading - the source data is located and loaded into a pandas dataframe'
'''

listings = r"C:\Users\damid\Downloads\dataset\dataset\listings.csv"
calendar = r"C:\Users\damid\Downloads\dataset\dataset\calendar.csv"

df1 = pd.read_csv(listings)
df2 = pd.read_csv(calendar)

'''
Data Transformation - the dataframes are transformed to eliminate unneccessary columns
and rows. In addition, datetime data is joined to the dataframe
'''

date_filter = df2[df2['date'] < '2017-01-01']
listing_filter = df1[['id','host_id','host_name','host_total_listings_count']]
listing_filter.rename(columns= {'id':'listing_id'}, inplace= True)
list_date = pd.merge(listing_filter, date_filter)
list_date = list_date[list_date['available'] == 't']
list_date = list_date.groupby(['host_id','host_name','host_total_listings_count'])['date'].count().reset_index()
list_date = list_date.sort_values(by=['date'], ascending=False)

'''
Data Load - the transformed data is now loaded into a new file ready to be further analyzed
'''

list_date.to_csv(r"C:\Users\damid\Downloads\dataset\airbnb.csv", encoding='utf-8', index=False)

