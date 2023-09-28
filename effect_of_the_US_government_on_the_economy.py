import pandas as pd
import numpy as np
import scipy.stats as sts
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
"""We are going to analyze the markets of the united states based on each govenment from the last two elections
we'll begin with the crude oil and gas markets than we'll move to other markets to see if there is a noticable pattern
Ill Note that Trump's tenure as president started on  januray 20'th 2017 and he his tenure ended on january 20'th 2021. 
Biden's  tenure stated on january 20'th 2021 until now (26'th of september 2023)"""

oil_market=pd.read_csv('US_markets_affect_by_the_government/WTI Price.csv',parse_dates=['DATE'])
oil_market=oil_market[oil_market['DATE']>=datetime.datetime(2017,0o1,20)]#we are only interested in trump and biden
gas_market=pd.read_csv('US_markets_affect_by_the_government/DGASUSGULF.csv',parse_dates=['DATE'])


gas_market.drop(gas_market[gas_market['DGASUSGULF']=='.'].index,inplace=True)
gas_market['DGASUSGULF']=gas_market['DGASUSGULF'].astype(float)#turning the values to a float
#we notice that this data set only starts at 2018 so there is no need to filter dates

#now we categorize by president
oil_market['president']=oil_market['DATE'].apply(lambda date: 'Trump' if date<datetime.datetime(2021,0o1,20) else 'Biden')
gas_market['president']=gas_market['DATE'].apply(lambda date: 'Trump' if date<datetime.datetime(2021,0o1,20) else 'Biden')

#now lets just keep the s&p500 from the oil database so we can easily see the pattern
oil_market_all=oil_market.copy()
oil_market=oil_market[['DATE','SP500','president']]
#creating the figures
f,[ax1,ax2]=plt.subplots(nrows=1,ncols=2)
f.set_figheight(8)
f.set_figwidth(12)
ax1.plot(oil_market['DATE'][oil_market['president']=='Trump'],oil_market['SP500'][oil_market['president']=='Trump'],color='red',label='Trump')
ax1.plot(oil_market['DATE'][oil_market['president']=='Biden'],oil_market['SP500'][oil_market['president']=='Biden'],color='blue',label='Biden')
ax1.set_title('Crude Oil Market')
ax1.legend()

ax2.plot(gas_market['DATE'][gas_market['president']=='Trump'],gas_market['DGASUSGULF'][gas_market['president']=='Trump'],color='red',label='Trump')
ax2.plot(gas_market['DATE'][gas_market['president']=='Biden'],gas_market['DGASUSGULF'][gas_market['president']=='Biden'],color='blue',label='Biden')
ax2.set_title('Gas Market')
ax2.legend()
plt.show()
#lets use the describe method in scipy stats to see some more insight about the two data_sets

print(sts.describe(oil_market['SP500'],nan_policy='omit'))#skewness=0.45, kurtosis=-1.15
print(sts.describe(gas_market['DGASUSGULF']))#skewness=0.41,kurtosis=0.22

"""It seems that both oil and gas prices were alot higher while biden was the president. 
But of course we need to consider that while Trump was president the corona virus started spreading 
That menas that we can't blame the govenment just yet. we need to check a lot more markets to see if this trend continus
When we analyze the scipy stats results we can see that both graphs are skewed to the right, which matches our graphs.
For the gas markets the kurtosis is .22 which means that the graphs is pretty close to a normal distribution.
This kinda makes sense becuase the end point and the start point of the graphs are close in highet and the lows and highes seem very symetrical
"""

#lets merge the dataframes to see if there is a correlation between the two datasets
oil_gas=pd.merge(left=gas_market,right=oil_market,how='inner')
oil_gas.rename(columns={'SP500':'oil','DGASUSGULF':'gas'},inplace=True)
print(oil_gas['oil'].corr(oil_gas['gas']))#0.614 Thats a very high coorelation. lets plot it

plt.scatter(oil_gas['oil'],oil_gas['gas'])
plt.xticks([],[])
plt.yticks([],[])
plt.xlabel('Oil Price')
plt.ylabel('Gas Price')
plt.title('Correlation between gas and oil prices')
plt.show()
"""The scatter plot shows it perfectly, there is a strong correlation between the gas prices and the crude oil prices.
That makes a lot of sense because clearly the two markets are intengled"""

"""Just to be sure that our oil in the s&p500 is correct lets graph the mean of all the markets in the oil dataframe
And see if the trend stays the same"""

def mean(row):
    return row.iloc[1:16].sum()/15
oil_market_all['mean']=oil_market_all.apply(mean,axis=1)
print(oil_market_all['mean'].mean())#5346
"""The average of the mean columns is 5346. We can see there are a few outliers. 
we'll drop the data that is smaller than 3500 becuse they ruin the graph and they are probably caused by errors in the data"""

oil_market_all.drop(oil_market_all[oil_market_all['mean']<3500].index,inplace=True)
plt.plot(oil_market_all['DATE'][oil_market_all['president']=='Trump'],oil_market_all['mean'][oil_market_all['president']=='Trump'],color='red',label='Trump')
plt.plot(oil_market_all['DATE'][oil_market_all['president']=='Biden'],oil_market_all['mean'][oil_market_all['president']=='Biden'],color='blue',label='Biden')
plt.xlim(min(oil_market_all['DATE']),max(oil_market_all['DATE']))
plt.ylim(min(oil_market_all['mean']-1000))
plt.legend()
plt.title('Oil markets In Trump\'s vs Biden\'s tenures')
plt.show()

"""So the trend stayed the same, even when we took the average of all the oil markets in all the Major stock exchanges
Now that we know that we can continue to other markets to see if the trend stays the same"""

#now lets move to the housing market 
houses=pd.read_csv('US_markets_affect_by_the_government/ASPUS.csv',parse_dates=['DATE'])
houses['president']=houses['DATE'].apply(lambda date: 'Trump' if date<datetime.datetime(2021,0o1,20) else 'Biden')
houses=houses[houses['DATE']>=datetime.datetime(2017,0o1,20)]
#now we have the market prices based on the president. lets plot the results

new_row={'DATE':datetime.datetime(2021,0o1,0o1),"ASPUS":418600,"president":'Biden'}#we create another row with the same values to
#make the graph continues
houses.loc[len(houses)]=new_row
houses.sort_values('DATE',inplace=True)#we make sure the new row is in the right place

print(houses)
plt.figure(figsize=(10,8))
plt.plot(houses['DATE'][houses['president']=='Trump'],houses['ASPUS'][houses['president']=='Trump'],color='red',label='Trump')
plt.plot(houses['DATE'][houses['president']=='Biden'],houses['ASPUS'][houses['president']=='Biden'],color='blue',label='Biden')
plt.xlabel('Year')
plt.ylabel('Houses average price')
plt.title('Average houses price in Trump\'s vs Biden\'s tenures')
plt.legend()
plt.show()
#lets calaculate the mean for each period
trump_mean=houses['ASPUS'][houses['president']=='Trump'].mean()
biden_mean=houses['ASPUS'][houses['president']=='Biden'].mean()
print(trump_mean,biden_mean)#Trump:386673 Biden:497190
#lets also look at the scipy stats describe for the apartment prices
print(sts.describe(houses['ASPUS']))#skewness=0.768, kurtosis=-0.97
#lets use a ttest to look at the values. lets expect the houses price to be the median of the series and see how much we deviatge from this
print(sts.ttest_1samp(houses['ASPUS'],houses['ASPUS'].median()))#p_value of 0.019

"""That's intersting! the prices of houses accually skyrocketed by a ton. On average houses at Trump's tenure coseted 110000 less 
than on Biden's tenure
Also if we look at scipy stats results we can see that the graph is massively skewed to the left, which fits the graphs and the kurtosis is -.97 
which means that the graph is squished a lot. which also makes sense if we look that when the graph is red the values stay about the same
the p_value of the prices of the houses is 0.019 which is less than 0.05. that means we can reject the null hypothesis and conclude that there
is some correlation between the prices of the houses and the median. the median is the point where the presidents switched meaning
that the prices have a lot to do with that switch


and when the graph is blue the values shoot up
So while Stock prices have gone up on Biden's tenure which is a good thing. The housing market has also gone up
making it much harder for the average citizen to buy a house.
We need to keep exploring to see the behaivoir of the rest of the market to see if the govenment had a positive or negative result"""

"""Now lets take a look on some big tech companies like Apple, Microsoft  Facebook and Amazon
For ease of use we'll use the opening cost for each company"""


facebook=pd.read_csv('US_markets_affect_by_the_government/FB_stock_history.csv',parse_dates=['Date'])
facebook=facebook.rename(columns={'Date':'date','Open':'facebook_open'})
facebook=facebook[['date','facebook_open']]#keeping only the relevant info
#to complete the data until 2023 we read another facebook data set

facebook1=pd.read_csv('US_markets_affect_by_the_government/facebook1.csv',parse_dates=['Date'])
facebook1=facebook1.rename(columns={'Date':'date','Open':'facebook_open'})
facebook1=facebook1[['date','facebook_open']]#keeping only the relevant info
facebook=pd.concat([facebook1,facebook],axis=0)
facebook=facebook.sort_values('date')
#if the dates overlapped we need to remove the duplicated
facebook=facebook.drop_duplicates()

apple=pd.read_csv('US_markets_affect_by_the_government/Apple Stock Prices (1981 to 2023).csv')
#we need to clean apple Date's columns so we can turn it into date time
apple['Date']=apple['Date'].str.replace('/','-')
#we need to change the format of the parse so it reads it correctly
apple['Date']=pd.to_datetime(apple['Date'],format='%d-%m-%Y')
apple=apple.rename(columns={'Date':'date','Open':'apple_open'})
apple=apple[['date','apple_open']]#keeping only the relevant info


microsoft=pd.read_csv('US_markets_affect_by_the_government/Microsoft Stocks.csv',parse_dates=['Date'])
microsoft=microsoft.rename(columns={'Date':'date','Open':'microsoft_open'})
microsoft=microsoft[['date','microsoft_open']]#keeping only the relevant info

amazon=pd.read_csv('US_markets_affect_by_the_government/amzn_split_adjusted.csv',parse_dates=['date'])
amazon=amazon[['date','open']]#keeping only the relevant info
amazon=amazon.rename(columns={'open':'amazon_open'})
combine=pd.merge(left=amazon,right=facebook,how='inner')
combine=pd.merge(left=combine,right=microsoft,how='inner')
combine=pd.merge(left=combine,right=apple)
#we combined all of the data sets. lets graph them one time sepratly and one time on the same graph, filter by the relevent dates and assign a presidnt to each peroid
combine=combine[combine['date']>=datetime.datetime(2017,0o1,20)]
combine['president']=combine['date'].apply(lambda date: 'Trump' if date<datetime.datetime(2021,0o1,20) else 'Biden')


#now lets plot all of the stockes side by side
f,[[ax1,ax2],[ax3,ax4]]=plt.subplots(nrows=2,ncols=2)
f.set_figwidth(10)
f.set_figheight(8)
ax1.plot(combine['date'][combine['president']=='Trump'],combine['amazon_open'][combine['president']=='Trump'],color='red',label='Trump')
ax1.plot(combine['date'][combine['president']=='Biden'],combine['amazon_open'][combine['president']=='Biden'],color='blue',label='Biden')
ax1.legend()
ax1.set_title('Amazon stock')
ax1.spines[['right', 'top']].set_visible(False)

ax2.plot(combine['date'][combine['president']=='Trump'],combine['apple_open'][combine['president']=='Trump'],color='red',label='Trump')
ax2.plot(combine['date'][combine['president']=='Biden'],combine['apple_open'][combine['president']=='Biden'],color='blue',label='Biden')
ax2.legend()
ax2.set_title('Apple stock')
ax2.spines[['right', 'top']].set_visible(False)

ax3.plot(combine['date'][combine['president']=='Trump'],combine['microsoft_open'][combine['president']=='Trump'],color='red',label='Trump')
ax3.plot(combine['date'][combine['president']=='Biden'],combine['microsoft_open'][combine['president']=='Biden'],color='blue',label='Biden')
ax3.legend()
ax3.set_title('Microsoft stock')
ax3.spines[['right', 'top']].set_visible(False)

ax4.plot(combine['date'][combine['president']=='Trump'],combine['facebook_open'][combine['president']=='Trump'],color='red',label='Trump')
ax4.plot(combine['date'][combine['president']=='Biden'],combine['facebook_open'][combine['president']=='Biden'],color='blue',label='Biden')
ax4.legend()
ax4.set_title('Facebook stock')
ax4.spines[['right', 'top']].set_visible(False)
plt.show()
"""Wow it seems like all of those stocks follow a similar pattern.
They All begin to fall at the end of 2021. 
A few months after Biden tenure stated.
maybe Biden wasn't so good for the economy after all.
It looks like after his tenure started A lot of the huge teck companies began to lose thier value"""

#now lets look at some stats for the graphs we'll use scipy.stats to help us with those stats
for name in combine.columns[1:5]:
    print(name,sts.describe(combine[name]),"variation:",sts.variation(combine[name]))
"""from the stats we can see that the graph that is skewed the most is the apple one, which we can definitly notice.
All the other stocks fall down significatly except apple which barely drops
Another intersting fact is that facebook's kurtosis is closest to 0 which means that facebook's graph has the least outliers of the bunch
Which we can definatly see it's true becuae the graph looks similar to a normal distribution
We confirm this fact again when we also calculate the coefficient of the variation of facebook's stock.
It is closets to 0 and stantard deviation coefficient

In conclustion we have a contridiction, tech companies prices have gone down while gas and crude oil have gone up
We need to keep exploring the extract some more valueble data"""


"""Now lest move to another important indicator- inflation rate"""
inflation=pd.read_csv('US_markets_affect_by_the_government/US_inflation_rates.csv',parse_dates=['date'])

inflation=inflation[inflation['date']>=datetime.datetime(2017,0o1,0o1)]#filter by the wanted dates
inflation['president']=inflation['date'].apply(lambda date: 'Trump' if date<datetime.datetime(2021,0o1,20) else 'Biden')#we assign the presidents
row={'date':datetime.datetime(2021,0o1,0o1),'value':inflation['value'][inflation['date']==datetime.datetime(2021,0o1,0o1)],'president':'Biden'}#adding a new row to the plot has not gaps
inflation.loc[len(inflation)]=row
inflation.sort_values('date',inplace=True)

#plotting the graph
plt.plot(inflation['date'][inflation['president']=='Trump'],inflation['value'][inflation['president']=='Trump'],color='red',label='Trump')
plt.plot(inflation['date'][inflation['president']=='Biden'],inflation['value'][inflation['president']=='Biden'],color='blue',label='Biden')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Percentage rate')
plt.title('inflation rate percentage in the US')
sns.despine()
plt.show()

#lets look at some statistics 
inflation['value']=inflation['value'].astype(float)#lest first convert to float
print(sts.describe(inflation['value']))#skewnes= 0.83
print('Trump\'s mean:', str(inflation['value'][inflation['president']=='Trump'].mean()))#252,884
print('Biden\'s mean:', str(inflation['value'][inflation['president']=='Biden'].mean()))#285.901


"""wow, it looks like the the inflation rate is much higher even since biden stepped into the role of the president
The inflation rate does not seem to slow down
the mean value of the values is 265. However Trump's mean is 252.88 and Biden's mean is 285.901 which is much higher than Trump's.
Meaning the the inflation skyrocketed after biden started his tenure
the skew ness is 0.83 which indicated a strong skewness to the right Which again helps us understand how much the precentage went up in Biden's tenure

Lets plot some correlation graph between the interest rate and other indicators that we explored before
Lets start with the inlation against the price of the big tech companies
"""
#now lets clean our combine dataframe such that we aggregate the data per year and per month so it is in the same format as the inflation rate, so we can plot the values agains each other 
combine['Year']=combine['date'].apply(lambda date: date.year)
combine['month']=combine['date'].apply(lambda date: date.month)
combine_pivot=combine[['Year','month','amazon_open','facebook_open','microsoft_open','apple_open']]
combine_pivot=pd.pivot_table(combine_pivot,index=['Year','month']).reset_index()

def create_date(row):# a function that crates a date from the month and year column, the day is set to 1
    year=row.loc['Year']
    month=row.loc['month']
    day=1
    date=datetime.datetime(year=int(year),month=int(month),day=int(day))
    return date

combine_pivot['date']=combine_pivot.apply(create_date,axis=1)#applying the funciton
combine_pivot=pd.merge(left=combine_pivot,right=inflation,on='date',how='inner')

#now lets plot
f,[[ax1,ax2],[ax3,ax4],[ax5,ax6],[ax7,ax8]]=plt.subplots(nrows=4,ncols=2)
f.set_figheight(30)
f.set_figwidth(30)
plt.subplots_adjust(bottom=0.2,top=1,left=0.1,right=1,wspace=0.2,hspace=1)
axes=[ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]#make the subplots preattier
for ax in axes:
    sns.despine()
axes_twos=[[ax1,ax2],[ax3,ax4],[ax5,ax6],[ax7,ax8]]
stockes=['amazon_open','apple_open','microsoft_open','facebook_open']
for axes,stock in zip(axes_twos,stockes):
    axes[0].scatter(combine_pivot[name][combine_pivot['president']=='Trump'],combine_pivot['value'][combine_pivot['president']=='Trump'],color='red')
    axes[0].set_title('Infaltion in Trump\'s era vs {}'.format(stock))
    axes[0].set_xlabel('stock value')
    axes[0].set_ylabel('inflation rate')

    axes[1].scatter(combine_pivot[name][combine_pivot['president']=='Biden'],combine_pivot['value'][combine_pivot['president']=='Biden'],color='blue')
    axes[1].set_title('Infaltion in Biden\'s era vs {}'.format(stock))
    axes[1].set_xlabel('stock value')
    axes[1].set_ylabel('inflation rate')

plt.show()
"""That is very interesting. We plotted the inflation rate vs tech companies in Biden's vs Trump's tenure
We see that when Trump was the president There was a correlation between the stock price and the inflation rate
When the inflaiton has gone up so has the stock 
While on Biden's tenure, there was no correlation to speak off, the stock's prices behave abnormally and siminglly at random...
We can conclude that the tech indestry was at a much better place when Trump was the president.
It was a lot more stable and predictable"""

