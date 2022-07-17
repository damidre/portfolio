from datetime import date
import pandas as pd

listings = r"C:\Users\damid\Downloads\dataset\dataset\listings.csv"
calendar = r"C:\Users\damid\Downloads\dataset\dataset\calendar.csv"

df1 = pd.read_csv(listings)
df2 = pd.read_csv(calendar)

date_filter = df2[df2['date'] < '2017-01-01']
listing_filter = df1[['id','host_id','host_name','host_total_listings_count']]
listing_filter.rename(columns= {'id':'listing_id'}, inplace= True)

list_date = pd.merge(listing_filter, date_filter)
list_date = list_date[list_date['available'] == 't']

list_date = list_date.groupby(['available','host_id','host_name'])['host_total_listings_count'].sum().reset_index()

list_date = list_date.sort_values(by=['host_total_listings_count'], ascending=False)

list_date.to_csv(r"C:\Users\damid\Downloads\dataset\airbnb.csv", encoding='utf-8', index=False)

print('finished')

