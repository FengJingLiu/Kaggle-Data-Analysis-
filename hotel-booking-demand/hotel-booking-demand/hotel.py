# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:42:38 2020

@author: scofield
"""
import pandas as pd
import matplotlib.mlab as mlab  
import matplotlib.pyplot as plt 
import plotly_express as px
from plotly.offline import plot
import seaborn as sns




full_data_cln = pd.read_csv('../hotel_bookings.csv')
full_data_cln.shape
full_data_cln.columns

# After cleaning, separate Resort and City hotel
# To know the acutal visitor numbers, only bookings that were not canceled are included. 
rh = full_data_cln.loc[(full_data_cln["hotel"] == "Resort Hotel") & (full_data_cln["is_canceled"] == 0)]
ch = full_data_cln.loc[(full_data_cln["hotel"] == "City Hotel") & (full_data_cln["is_canceled"] == 0)]


# get number of acutal guests by country
country_data = pd.DataFrame(full_data_cln.loc[full_data_cln["is_canceled"] == 0]["country"].value_counts())
#country_data.index.name = "country"
country_data.rename(columns={"country": "Number of Guests"}, inplace=True)
total_guests = country_data["Number of Guests"].sum()
country_data["Guests in %"] = round(country_data["Number of Guests"] / total_guests * 100, 2)
country_data["country"] = country_data.index
#country_data.loc[country_data["Guests in %"] < 2, "country"] = "Other"

# pie plot
fig = px.pie(country_data,
             values="Number of Guests",
             names="country",
             title="Home country of guests",
             template="seaborn")
fig.update_traces(textposition="inside", textinfo="value+percent+label")
plot(fig)

# map 
guest_map = px.choropleth(country_data,
                    locations=country_data.index,
                    color=country_data["Guests in %"], 
                    hover_name=country_data.index, 
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Home country of guests")
plot(guest_map)

#adr box
full_data_cln["adr_pp"] = full_data_cln["adr"] / (full_data_cln["adults"] + full_data_cln["children"])
full_data_guests = full_data_cln.loc[full_data_cln["is_canceled"] == 0] # only actual gusts
room_prices = full_data_guests[["hotel", "reserved_room_type", "adr_pp"]].sort_values("reserved_room_type")

fig = px.box(room_prices, x="reserved_room_type", y="adr_pp", color="hotel")
fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
plot(fig)

#price per night vary over the year
room_prices_mothly = full_data_guests[["hotel", "arrival_date_month", "adr_pp"]].sort_values("arrival_date_month")
room_prices_mothly.replace('December',12,inplace=True)
ordered_months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
room_prices_mothly["arrival_date_month"] = pd.Categorical(room_prices_mothly["arrival_date_month"], categories=ordered_months, ordered=True)
room_prices_mothly.sort_values('arrival_date_month')
plt.figure()
sns.countplot(x="arrival_date_month", 
                  hue="hotel", data=room_prices_mothly)
plt.show()
#How long do people stay at the hotels
plt.figure(figsize=(16, 8))
sns.countplot(x = "stays_in_week_nights", hue="hotel", data=full_data_guests)
sns.countplot(x = "stays_in_weekend_nights", hue="hotel", data=full_data_guests)
plt.title("Length of stay", fontsize=16)
plt.xlabel("Number of nights", fontsize=16)
plt.ylabel("Guests [%]", fontsize=16)
plt.legend(loc="upper right")
plt.xlim(0,22)
plt.show()

#Bookings by market segment
fig = px.pie(full_data_guests['market_segment'].value_counts(),
             values=full_data_guests['market_segment'].value_counts(),
             names=full_data_guests['market_segment'].value_counts().index,
             title="market segment",
             template="seaborn")
fig.update_traces(textposition="inside", textinfo="value+percent+label")
plot(fig)



















