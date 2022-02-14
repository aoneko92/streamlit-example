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
from scipy.stats import pearsonr

###Create mapfile for prefecture level results
shp = gpd.read_file("jpn_admbnda_adm1_2019.shp")
shp["pref"] = shp["ADM1_PCODE"].replace("JP", "", regex=True)
shp['pref']=shp['pref'].astype(int)

f_list = ["PrefDep.csv", "PrefLon.csv", "PrefRMch.csv", "PrefRMme.csv", "PrefWell.csv",
          "suiciderate_full_2020.csv", "suiciderate_male_2020.csv", "suiciderate_female_2020.csv"]

regions = pd.read_excel("regionsRN.xlsx")[["ken", "RegionA"]]
regions = regions.rename(columns={"ken":"pref"})
shp = pd.merge(shp, regions, on = ["pref"])
for i in range(0, len(f_list)): 
    data = pd.read_csv(f_list[i])
    data['pref']=data['pref'].astype(int)

    shp = pd.merge(shp, data, on = ["pref"])

shp = gpd.GeoDataFrame(shp)
shp.index = shp["ADM1_EN"]


###Create mapfile for region level results
shp_1 = gpd.read_file("jpn_admbnda_adm1_2019.shp")
shp_1["pref"] = shp_1["ADM1_PCODE"].replace("JP", "", regex=True)
shp_1['pref']=shp_1['pref'].astype(int)

reg_data = pd.read_csv("region_RM_RNFeb14.csv")
rd_orig = pd.read_csv("region_RM_RNFeb14.csv")

regions = pd.read_excel("regionsRN.xlsx")[["ken", "RegionA"]]

reg_data = pd.merge(regions, reg_data, on = "RegionA")
reg_data = reg_data.rename(columns={"ken":"pref"})
shp_1 = pd.merge(shp_1, reg_data, on = ["pref"])

shp_1 = gpd.GeoDataFrame(shp_1)
shp_1.index = shp_1["ADM1_EN"]

      
st.write("Mental health in Japan by relational mobility status")

col3, col4 = st.columns(2)

with col3:     
    sb_type = st.selectbox("Analysis type",("Single plot", "Compare 2 plots"))
with col4:
    mh_0 = st.selectbox("Choose area type", ("Prefecture", "Region"))

if sb_type == "Single plot":
    mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                        "Suicide rate 2020", "Suicide rate 2020 - Males", 
                                        "Suicide rate 2020 - Females"), key = 0)
elif sb_type == "Compare 2 plots":
    col1, col2 = st.columns(2)
    with col1:
        mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                            "Suicide rate 2020", "Suicide rate 2020 - Males", 
                                            "Suicide rate 2020 - Females"), key = 0)
    with col2:
        mh_1 = st.selectbox("Type of mental health - Figure 2", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                            "Suicide rate 2020", "Suicide rate 2020 - Males", 
                                            "Suicide rate 2020 - Females"), key = 1)



###Dropdown menus
if mh_0 == "Prefecture":

    ##functions for plot 1
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
    elif mh == "Suicide rate 2020":
        t = "suicide_rate_2020"    
    elif mh == "Suicide rate 2020 - Males":
        t = "suicide_rate_male_2020"
    elif mh == "Suicide rate 2020 - Females":
        t = "suicide_rate_female_2020" 
    fig_1 = px.choropleth_mapbox(
        shp,
        geojson=shp.geometry,
        locations="ADM1_EN",
        color=t,
        hover_name = "RegionA",
        center=dict(lat=35.24, lon=139.32),
        mapbox_style="open-street-map",
        zoom=3,
        title = "Figure 1 - " + mh,
        height = 500,
        width = 450
        )
    
    if sb_type == "Compare 2 plots":
        ##functions for plot 2
        if mh_1 == "Depression": 
            t_1 = "depression"
        elif mh_1 == "Loneliness":
            t_1 = "loneliness"
        elif mh_1 == "Well-being": 
            t_1 = "wellbeing"
        elif mh_1 == "RM_Choosing":
            t_1 = "choosingRM"
        elif mh_1 == "RM_Meeting":
            t_1 = "meetingRM"
        elif mh_1 == "Suicide rate 2020":
            t_1 = "suicide_rate_2020"    
        elif mh_1 == "Suicide rate 2020 - Males":
            t_1 = "suicide_rate_male_2020"
        elif mh_1 == "Suicide rate 2020 - Females":
            t_1 = "suicide_rate_female_2020" 
    

        fig_2 = px.choropleth_mapbox(
            shp,
            geojson=shp.geometry,
            locations="ADM1_EN",
            color=t_1,
            hover_name = "RegionA",
            center=dict(lat=35.24, lon=139.32),
            mapbox_style="open-street-map",
            zoom=3,
            title = "Figure 2 - " + mh_1,
            height = 500,
            width = 450
            )
        #calculate pearsons correlation
        mes = 'Pearsons correlation: ' + str(shp[t].corr(shp[t_1]))

##for regions
if mh_0 == "Region":
    ##functions for plot 1
    if mh == "Depression": 
        t = "dep0"
    elif mh == "Loneliness":
        t = "loneliness"
    elif mh == "Well-being": 
        t = "well"
    elif mh == "RM_Choosing":
        t = "chRM"
    elif mh == "RM_Meeting":
        t = "mtRM"
    elif mh == "Suicide rate 2020":
        t = "suicide_rate_reg_tot"    
    elif mh == "Suicide rate 2020 - Males":
        t = "suicide_rate_reg_male"
    elif mh == "Suicide rate 2020 - Females":
        t = "suicide_rate_reg_female" 
    
    fig_1 = px.choropleth_mapbox(
        shp_1,
        geojson=shp.geometry,
        locations="ADM1_EN",
        color=t,
        hover_name = "RegionA",
        center=dict(lat=35.24, lon=139.32),
        mapbox_style="open-street-map",
        zoom=3,
        title = "Figure 1 - " + mh,
        height = 500,
        width = 450
        )
    if sb_type == "Compare 2 plots":

        ##functions for plot 2
        if mh_1 == "Depression": 
            t_1 = "dep0"
        elif mh_1 == "Loneliness":
            t_1 = "loneliness"
        elif mh_1 == "Well-being": 
            t_1 = "well"
        elif mh_1 == "RM_Choosing":
            t_1 = "chRM"
        elif mh_1 == "RM_Meeting":
            t_1 = "mtRM"
        elif mh_1 == "Suicide rate 2020":
            t_1 = "suicide_rate_reg_tot"    
        elif mh_1 == "Suicide rate 2020 - Males":
            t_1 = "suicide_rate_reg_male"
        elif mh_1 == "Suicide rate 2020 - Females":
            t_1 = "suicide_rate_reg_female" 
            
    

        fig_2 = px.choropleth_mapbox(
            shp_1,
            geojson=shp.geometry,
            locations="ADM1_EN",
            color=t_1,
            hover_name = "RegionA",
            center=dict(lat=35.24, lon=139.32),
            mapbox_style="open-street-map",
            zoom=3,
            title = "Figure 2 - " + mh_1,
            height = 500,
            width = 450
            )
        #calculate pearsons correlation
        mes = 'Pearsons correlation: ' + str(rd_orig[t].corr(rd_orig[t_1]))


if sb_type == "Single plot":
    st.plotly_chart(fig_1, use_container_width=True)

if sb_type == "Compare 2 plots":
    st.write(mes)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_1, use_container_width=True)
    with col2:
        st.plotly_chart(fig_2, use_container_width=True)

