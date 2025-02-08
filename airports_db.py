# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 07:50:29 2020

@author: Araz Sharma
"""
#Global Variables Required
#strt_cods = []
#dstn_cods = []
Nodes = {}

import math

#Distance Function
#d = 60 * inv(cos)[(sin lat1 * sin lat2) + (cos lat1 * cos lat2) * cos(lon1 - lon2)]
def distance(lat1, lon1, lat2, lon2):
   lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
   d = 6371 * math.acos((math.cos(lon1-lon2)) * (math.cos(lat1) * math.cos(lat2)) + (math.sin(lat1) * math.sin(lat2)))
   return d 

#IMPORTS 

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


#Importing Values from SQL
import sqlite3

st.title("Aviation Distance Estimation & Route Planning Tool")
st.markdown("This app is a streamlit dashboard that can be used"
" to show A-Star Algorithm for Air Routes based on User Input 🦇✈️⛽🏴󠁫󠁭󠁭󠁿💥")

@st.cache(persist=True, allow_output_mutation = True)
def load_data():
    conn = sqlite3.connect('global_airports_sqlite.db')
    c = conn.cursor()
    c.execute('SELECT name, city, country, lat_decimal, lon_decimal FROM airports')
    data = c.fetchall()
    df = pd.DataFrame(data, columns = ['Name', 'City', 'Country', 'Lat', 'Lon'])

    df.drop(df[((df['Lon'] == 0.000) & (df['Lat']== 0.000))].index, inplace = True)
    return df

df = load_data()


#User Input for Starting Location/Node
st.header("Airports you want to visit")
st.subheader("Starting Airport:")
#Country Selection

cntry_list = list(set(df['Country']))#.sort(key = strn)
cntry_list.sort()
country = st.selectbox("Country you want to start at:", cntry_list)

st.write("Country you selected for Starting your journey:", country)

#City Selection
city_list = list(set(df[df.Country == country]['City']))
city_list.sort()
print(city_list)
city = st.selectbox("City you want to start at:", city_list)

st.write("City you selected for Starting your journey:", city)

#Coods of Strting Pnt

strt_df = df[df.Country == country][df.City == city]
strt_df.reset_index(inplace = True)
strt_df.drop(['index'], axis = 1, inplace = True)
strt_df.index = strt_df.index + 1
print(strt_df)
st.subheader("Airports Available with your selection")
st.write(strt_df)

#Choose Starting Airport Final
str_choice = st.selectbox("Choose your Srt Airport from Index Number:",range(1,len(strt_df)+1))
str_air = strt_df.loc[str_choice]

strt_cods = [str_air['Lat'], str_air['Lon']]

st.write("These are:",strt_cods)

Nodes[str_air['Name']] = strt_cods

#Destination Airport

st.subheader("Destination Airport:")
#Country Selection


country_dst = st.selectbox("Destination Country:", cntry_list)

st.write("Country you selected for Destination:", country_dst)

#City Selection
cityds_list = list(set(df[df.Country == country_dst]['City']))
cityds_list.sort()
#print(cityds_list)
city_dst = st.selectbox("Destination City:", cityds_list)

st.write("City you selected for Destination:", city_dst)

#Coods of Destination

new_df = df[df.Country == country_dst][df.City == city_dst]
new_df.reset_index(inplace = True)
new_df.drop(['index'], axis = 1, inplace = True)
new_df.index = new_df.index + 1
print(new_df)
st.subheader("Airports Available with your selection")
st.write(new_df)

#Choose Destination Airport Final
dst_choice = st.selectbox("Choose your Dst Airport from Index Number:",range(1,len(new_df)+1))
dst_air = new_df.loc[dst_choice]

dstn_cods = [dst_air['Lat'], dst_air['Lon']]
st.write(dstn_cods)


Nodes[dst_air['Name']] = dstn_cods

st.subheader("Start & Destination")
st.write("You have selected ", str_air['Name'], "Airport at city of ", str_air['City'], "in ", str_air['Country'], "to start your journey")
st.write("You have selected ", dst_air['Name'], "Airport at city of ", dst_air['City'], "in ", dst_air['Country'], "to end your journey")



#st.write(str_air)
#st.write(dst_air)
#str_air -> Starting Airport
#dst_air -> Destination Airport

#Nodes to Add
st.subheader('Add Node Airports to Path')
num_nodes = st.slider("No. of Airports to add:", 0,30)
st.write("You chose to add ",num_nodes,"number of airports in path")
for i in range(num_nodes):
    st.write("Airport -",i+1)
    nd_cntry = st.selectbox("Country for Airport:", cntry_list, key = "Airport_Cntry_"+ str(i))
    citynd_list = list(set(df[df.Country == nd_cntry]['City']))
    citynd_list.sort()
    nd_city = st.selectbox("City for Airport:", citynd_list, key = "Airport_City_"+ str(i))
    
    
    new_df = df[df.Country == nd_cntry][df.City == nd_city]
    new_df.reset_index(inplace = True)
    new_df.drop(['index'], axis = 1, inplace = True)
    new_df.index = new_df.index + 1
    
    st.write("Airports Available with your selection")
    st.write(new_df)
    
    nd_choice = st.selectbox("Choose your Airport from Index Number:",range(1,len(new_df)+1), key = "Airport_"+ str(i))
    nd_air = new_df.loc[nd_choice]
    
    st.write("You have added ", nd_air['Name'], "Airport at city of ", nd_air['City'], "in ", nd_air['Country'], "to your journey")
    
    Nodes[nd_air['Name']]= [nd_air['Lat'], nd_air['Lon']]

print(Nodes)


# Maximum Allowed Distance before Refuelling
max_refuel = st.number_input("Enter Max Distance allowed before Refuelling", 1000)
st.write("Distance allowed:", max_refuel)



#Distance between starting & destination


st.write("Distance between Start & Destination is", distance(strt_cods[0], strt_cods[1], dstn_cods[0], dstn_cods[1]))
#Data Manipulation Stuff

#print(df.shape)
#num_country = df['Country'].value_counts()
#num_cities = df['City'].value_counts()
#print(len(num_cities))
#print("No of countries:", len(num_country))

#print(len(df[df.Country== "INDIA"]['City']))
#print(len(set(df[df.Country== "INDIA"]['City'])))
#print((df[df.Country== "INDIA"]['City']).value_counts())
#print(df[['Lon', 'Lat']].where(df['Country']=="INDIA"))
 
#print((df[df.Country== "INDIA"][['City', 'Lon', 'Lat']]))

# A-Star Algo


def to_sort(x):
    hn_cst = distance(dstn_cods[0], dstn_cods[1], Nodes[x[0]][0], Nodes[x[0]][1])
    gn_cst = x[1]
    return (hn_cst + gn_cst)

def route_DMA(start, goal, nodes, mx):
    visited = set()
    path = []
    fn_stack = [[start, 0]]
    true_cost = 0
    while fn_stack:
        fn_stack.sort(key = to_sort)
        print("stack is:", fn_stack)
        print("visited is:", visited)
        node = fn_stack.pop(0)
        print("node selected:", node)
        
        if node[0] not in visited:
            visited.add(node[0])
            path.append(node[0])
            if(node[0]== goal):
                print("Goal found with route distance:", node[1])
                print("Path is:", path)
                return path, node[1]
            
            true_cost = node[1]
            for i in nodes.keys():
                if i not in visited:
                    d = distance(nodes[i][0], nodes[i][1], nodes[node[0]][0],nodes[node[0]][1])
                    if(d <= mx ):
                        fn_stack.append([i, (true_cost + d )])
                    #IF MAX DISTANCE CONDITION SATISFIED
                #ADD NODE IN STACK TO CHECK FOR F(n)
    print("No Path Available")
    return 0, 0
    
    
path, op_distance = route_DMA(str_air['Name'],dst_air['Name'], Nodes, max_refuel )
output_df = {"Journey Routes in order":[], "Distance of Flight Leg":[]}

st.subheader("RESULTS")

if(path):
    
    st.write("PATH FOUND:", path, "WITH TOTAL OPTIMAL DISTANCE:", op_distance)

    for i in range(len(path)-1):
        output_df["Journey Routes in order"].append(path[i] + " - " + path[i+1])
        output_df["Distance of Flight Leg"].append(round(distance(Nodes[path[i]][0],Nodes[path[i]][1],Nodes[path[i+1]][0],Nodes[path[i+1]][1]), 2))
        
    print(output_df)
    output_df = pd.DataFrame(output_df)
    st.dataframe(output_df)
    

    


    #final_df = {'lat':[Nodes[i][0] for i in path], 'lon':[Nodes[i][1] for i in path]}
    final_df = {'fpath':[[Nodes[i] for i in path]]}
    print(final_df)
    final_df = pd.DataFrame(final_df)
    print(final_df)
    #tst_df = {'strt':[Nodes[i]]}
    
    #st.map(final_df)
    
    view_state = pdk.ViewState(
    latitude=strt_cods[0],
    longitude=strt_cods[1],
    zoom=10
    )

    layer = pdk.Layer(
    type='PathLayer',
    data=final_df,
    pickable=True,
    get_color=[253, 128, 93],
    width_scale=20,
    width_min_pixels=2,
    get_path='fpath',
    #get_source_position= [-122.3535851, 37.9360513],
    #get_target_position=[23.889, 91.241],
    get_width=5
    )

    r = pdk.Deck(layers=[layer], initial_view_state=view_state)

    st.pydeck_chart(r)

else:
    st.write("NO PATH AVAILABLE FOR YOUR SELECTION") 