# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 13:00:17 2022

@author: robba
"""

import os
os.environ['PROJ_LIB'] = 'C:\\Users\\robba\\anaconda3\\envs\\sai\\Library\\share\\proj'
os.environ['GDAL_DATA'] = 'C:\\Users\\robba\\anaconda3\\envs\sai\\Library\\share'

import pandas as pd
import streamlit as st
import geopandas as gpd
import plotly.express as px

import matplotlib.pyplot as plt


shp = gpd.read_file("jpn_admbnda_adm1_2019.shp")
shp["pref"] = shp["ADM1_PCODE"].replace("JP", "", regex=True)
shp['pref']=shp['pref'].astype(int)

f_list = ["PrefDep.csv", "PrefLon.csv", "PrefRMch.csv", "PrefRMme.csv", "PrefWell.csv"]

for i in range(0, len(f_list)): 
    data = pd.read_csv(f_list[i])
    data['pref']=data['pref'].astype(int)

    shp = pd.merge(shp, data, on = ["pref"])

shp = gpd.GeoDataFrame(shp)

shp.index = shp["ADM1_EN"]

st.write("Mental health in Japan by relational mobility status")

mh = st.selectbox("Type of mental health", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting"))

if mh == "Depression": 
    t = "depression"
elif mh == "Loneliness":
    t = "loneliness"
elif mh == "Well-being": 
    t = "wellbeing"
elif mh == "RM_Choosing":
    t = "choosingRM"
elif mh == "RM_Meeting":
    t = "meetingRM"

fig = px.choropleth_mapbox(
    shp,
    geojson=shp.geometry,
    locations="ADM1_EN",
    color=t,
    center=dict(lat=35.24, lon=139.32),
    mapbox_style="open-street-map",
    zoom=3,
)


st.plotly_chart(fig)
