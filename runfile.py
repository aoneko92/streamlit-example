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

##add percentage variables
dummies = pd.read_csv("pref_dummies_feb17.csv")
shp = pd.merge(shp, dummies, on = ["pref"])

shp = gpd.GeoDataFrame(shp)
shp.index = shp["ADM1_EN"]


###Create mapfile for region level results
shp_1 = gpd.read_file("jpn_admbnda_adm1_2019.shp")
shp_1["pref"] = shp_1["ADM1_PCODE"].replace("JP", "", regex=True)
shp_1['pref']=shp_1['pref'].astype(int)

reg_data = pd.read_csv("region_RM_RNFeb14.csv")
##read dummy data and merge
dummies = pd.read_csv("reg_dummies_feb17.csv")
reg_data = pd.merge(reg_data, dummies, on = "RegionA")
rd_orig = reg_data

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
    
    
    var_type = st.selectbox("Choose variable type - Figure 1", ("Mean", "Percentage"), key = 9)

    if mh_0 == "Prefecture":
        if var_type == "Mean":
            mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                                                   "Suicide rate 2020", "Suicide rate 2020 - Males", 
                                                                   "Suicide rate 2020 - Females"), key = 0)
        else:
            mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                                                   ), key = 0)

    elif mh_0 == "Region": 
        if var_type == "Mean":
            mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Depression - Male", "Depression - Female", 
                                                                   "Loneliness", "Loneliness - Male", "Loneliness - Female",
                                                                   "Well-being", "Well-being - Male", "Well-being - Female",
                                                                   "RM_Choosing", "RM_Choosing - Male", "RM_Choosing - Female",
                                                                   "RM_Meeting", "RM_Meeting - Male", "RM_Meeting - Female",
                                                                   "Suicide rate 2020", "Suicide rate 2020 - Male", 
                                                                   "Suicide rate 2020 - Female"), key = 0)
        else:
            mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Depression - Male", "Depression - Female", 
                                                                   "Loneliness", "Loneliness - Male", "Loneliness - Female",
                                                                   "Well-being", "Well-being - Male", "Well-being - Female",
                                                                   "RM_Choosing", "RM_Choosing - Male", "RM_Choosing - Female",
                                                                   "RM_Meeting", "RM_Meeting - Male", "RM_Meeting - Female",
                                                                   ), key = 0)
    



elif sb_type == "Compare 2 plots":
    if mh_0 == "Prefecture":
        ##add variable typer
        col7, col8 = st.columns(2)
        with col7:
            var_type = st.selectbox("Choose variable type - Figure 1", ("Mean", "Percentage"), key = 9)
        with col8:
            var_type_1 = st.selectbox("Choose variable type - Figure 2", ("Mean", "Percentage"), key = 10)

            
        col1, col2 = st.columns(2)
        with col1:
            if var_type == "Mean":
                mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                                                       "Suicide rate 2020", "Suicide rate 2020 - Males", 
                                                                       "Suicide rate 2020 - Females"), key = 0)
            else:
                mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                                                       ), key = 1)
        with col2:
            if var_type_1 == "Mean":
                mh_1 = st.selectbox("Type of mental health - Figure 1", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                                                       "Suicide rate 2020", "Suicide rate 2020 - Males", 
                                                                       "Suicide rate 2020 - Females"), key = 5)
            else:
                mh_1 = st.selectbox("Type of mental health - Figure 1", ("Depression", "Loneliness", "Well-being", "RM_Choosing", "RM_Meeting",
                                                                       ), key = 2)
    elif mh_0 == "Region":
        ##add variable typer
        col7, col8 = st.columns(2)
        with col7:
            var_type = st.selectbox("Choose variable type - Figure 1", ("Mean", "Percentage"), key = 9)
        with col8:
            var_type_1 = st.selectbox("Choose variable type - Figure 2", ("Mean", "Percentage"), key = 10)

        col1, col2 = st.columns(2)
        with col1:
            if var_type == "Mean":
                mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Depression - Male", "Depression - Female", 
                                                                       "Loneliness", "Loneliness - Male", "Loneliness - Female",
                                                                       "Well-being", "Well-being - Male", "Well-being - Female",
                                                                       "RM_Choosing", "RM_Choosing - Male", "RM_Choosing - Female",
                                                                       "RM_Meeting", "RM_Meeting - Male", "RM_Meeting - Female",
                                                                       "Suicide rate 2020", "Suicide rate 2020 - Male", 
                                                                       "Suicide rate 2020 - Female"), key = 0)
            else: 
                mh = st.selectbox("Type of mental health - Figure 1", ("Depression", "Depression - Male", "Depression - Female", 
                                                                       "Loneliness", "Loneliness - Male", "Loneliness - Female",
                                                                       "Well-being", "Well-being - Male", "Well-being - Female",
                                                                       "RM_Choosing", "RM_Choosing - Male", "RM_Choosing - Female",
                                                                       "RM_Meeting", "RM_Meeting - Male", "RM_Meeting - Female",
                                                                       ), key = 3)
        with col2:
            if var_type_1 == "Mean":
                mh_1 = st.selectbox("Type of mental health - Figure 1", ("Depression", "Depression - Male", "Depression - Female", 
                                                                       "Loneliness", "Loneliness - Male", "Loneliness - Female",
                                                                       "Well-being", "Well-being - Male", "Well-being - Female",
                                                                       "RM_Choosing", "RM_Choosing - Male", "RM_Choosing - Female",
                                                                       "RM_Meeting", "RM_Meeting - Male", "RM_Meeting - Female",
                                                                       "Suicide rate 2020", "Suicide rate 2020 - Male", 
                                                                       "Suicide rate 2020 - Female"), key = 1)
            else: 
                mh_1 = st.selectbox("Type of mental health - Figure 1", ("Depression", "Depression - Male", "Depression - Female", 
                                                                       "Loneliness", "Loneliness - Male", "Loneliness - Female",
                                                                       "Well-being", "Well-being - Male", "Well-being - Female",
                                                                       "RM_Choosing", "RM_Choosing - Male", "RM_Choosing - Female",
                                                                       "RM_Meeting", "RM_Meeting - Male", "RM_Meeting - Female",
                                                                       ), key = 4)


###Dropdown menus
if mh_0 == "Prefecture":

    ##functions for plot 1
    if mh == "Depression": 
        t = "depression" if var_type == "Mean" else "dep_d_p"
    elif mh == "Loneliness":
        t = "loneliness" if var_type == "Mean" else "lon_d_p"
    elif mh == "Well-being": 
        t = "wellbeing" if var_type == "Mean" else "well_d_p"
    elif mh == "RM_Choosing":
        t = "choosingRM" if var_type == "Mean" else "RMch_d_p"
    elif mh == "RM_Meeting":
        t = "meetingRM" if var_type == "Mean" else "RMme_d_p"
    elif mh == "Suicide rate 2020":
        t = "suicide_rate_2020"    
    elif mh == "Suicide rate 2020 - Males":
        t = "suicide_rate_male_2020"
    elif mh == "Suicide rate 2020 - Females":
        t = "suicide_rate_female_2020" 
        
    ## set scales and labels
    if var_type == "Percentage":
        rc_f1 = False
        if "Depression" in mh: 
            label = "Percentage of people who say they are depressed/very depressed"
        elif "Loneliness" in mh: 
            label = "Percentage of people who say they are lonely/very lonely"
        elif "Well-being" in mh: 
            label = "Percentage of people who say they are dissatisfied/very dissatisfied with life"
        elif "RM_Choosing" in mh: 
            label = "Percentage of people who are above national avg for RM_choosing"
        elif "RM_Meeting" in mh: 
            label = "Percentage of people who are above national avg for RM_meetings"

    else:    
        if "Depression" in mh: 
            rc_f1 = (3,7)
            label = "Avg. response on depression (0 - Not at all depressed, 30 - Extremely depreseed)"
        elif "Loneliness" in mh: 
            rc_f1 = (11,15)
            label = "Avg. response on Loneliness (0 - Not at all lonely, 30 - Extremely lonely)"
        elif "Well-being" in mh: 
            rc_f1 = (17,20.5)
            label = "Avg. response on life satisfaction (0 - Extremely unsatisfied, 30 - Extremely satisfied)"
        elif "RM_Choosing" in mh: 
            rc_f1 = (24,27)
            label = "Avg. response on RM_choosing"
        elif "RM_Meeting" in mh: 
            rc_f1 = (16,18)
            label = "Avg. response on RM_meeting"
        elif "Suicide" in mh: 
            rc_f1 = (5,28)
            label = "Suicide rate (per 100,000 population)"

        if "Male" in mh:
            g_label = " [MALE]"
        elif "Female" in mh:
            g_label = " [FEMALE]"
        else:
            g_label = ""
        
        
  
    
    fig_1 = px.choropleth_mapbox(
        shp,
        geojson=shp.geometry,
        locations="ADM1_EN",
        color=t,
        hover_name = "RegionA",
        center=dict(lat=35.24, lon=139.32),
        mapbox_style="open-street-map",
        zoom=3,
        title = "Figure 1 - " + label,
        height = 500,
        width = 450
        )
    
    if sb_type == "Compare 2 plots":
        ##functions for plot 2
        if mh_1 == "Depression": 
            t_1 = "depression" if var_type_1 == "Mean" else "dep_d_p"
        elif mh_1 == "Loneliness":
            t_1 = "loneliness" if var_type_1 == "Mean" else "lon_d_p"
        elif mh_1 == "Well-being": 
            t_1 = "wellbeing" if var_type_1 == "Mean" else "well_d_p"
        elif mh_1 == "RM_Choosing":
            t_1 = "choosingRM" if var_type_1 == "Mean" else "RMch_d_p"
        elif mh_1 == "RM_Meeting":
            t_1 = "meetingRM" if var_type_1 == "Mean" else "RMme_d_p"
        elif mh_1 == "Suicide rate 2020":
            t_1 = "suicide_rate_2020"    
        elif mh_1 == "Suicide rate 2020 - Males":
            t_1 = "suicide_rate_male_2020"
        elif mh_1 == "Suicide rate 2020 - Females":
            t_1 = "suicide_rate_female_2020" 
        
        ## set scales and labels
        if var_type_1 == "Percentage":
            
            rc_f2 = False
            if "Depression" in mh_1: 
                
                label_1 = "Percentage of people who say they are depressed/very depressed"
            elif "Loneliness" in mh_1: 
                label_1 = "Percentage of people who say they are lonely/very lonely"
            elif "Well-being" in mh_1: 
                label_1 = "Percentage of people who say they are dissatisfied/very dissatisfied with life"
            elif "RM_Choosing" in mh_1: 
                label_1 = "Percentage of people who are above national avg for RM_choosing"
            elif "RM_Meeting" in mh_1: 
                label_1 = "Percentage of people who are above national avg for RM_meetings"

        else:
            
            if "Depression" in mh_1: 
                rc_f2 = (3,7)
                label_1 = "Avg. response on depression (0 - Not at all depressed, 30 - Extremely depreseed)"
            elif "Loneliness" in mh_1: 
                rc_f2 = (11,15)
                label_1 = "Avg. response on Loneliness (0 - Not at all lonely, 30 - Extremely lonely)"

            elif "Well-being" in mh_1: 
                rc_f2 = (17,20.5)
                label_1 = "Avg. response on life satisfaction (0 - Extremely unsatisfied, 30 - Extremely satisfied)"

            elif "RM_Choosing" in mh_1: 
                rc_f2 = (24,27)
                label_1 = "Avg. response on RM_choosing"

            elif "RM_Meeting" in mh_1: 
                rc_f2 = (16,18)
                label_1 = "Avg. response on RM_meeting"

            elif "Suicide" in mh_1: 
                rc_f2 = (5,28)
                label_1 = "Suicide rate (per 100,000 population)"

        if "Male" in mh_1:             
            g_label_1 = " [MALE]"
        elif "Female" in mh_1:
            g_label_1 = " [FEMALE]"
        else:
            g_label_1 = ""
    

        fig_2 = px.choropleth_mapbox(
            shp,
            geojson=shp.geometry,
            locations="ADM1_EN",
            color=t_1,
            hover_name = "RegionA",
            center=dict(lat=35.24, lon=139.32),
            mapbox_style="open-street-map",
            zoom=3,
            title = "Figure 2 - " + label_1,
            height = 500,
            width = 450
            )
        #calculate pearsons correlation
        mes = 'Pearsons correlation: ' + str(shp[t].corr(shp[t_1]))[:6]

##for regions
if mh_0 == "Region":
    ##functions for plot 1
    if mh == "Depression": 
        t = "dep0" if var_type == "Mean" else "dep_d_r"
    elif mh == "Depression - Male":
        t = "dep0M" if var_type == "Mean" else "dep_d_m_r"
    elif mh == "Depression - Female":
        t = "dep0F" if var_type == "Mean" else "dep_d_f_r"
    elif mh == "Loneliness":
        t = "loneliness" if var_type == "Mean" else "lon_d_r"
    elif mh == "Loneliness - Male":
        t = "lonelinessM" if var_type == "Mean" else "lon_d_m_r"
    elif mh == "Loneliness - Female":
        t = "lonelinessF" if var_type == "Mean" else "lon_d_f_r"
    elif mh == "Well-being": 
        t = "well" if var_type == "Mean" else "well_d_r"
    elif mh == "Well-being - Male":
        t = "wellM" if var_type == "Mean" else "well_d_r"
    elif mh == "Well-being - Female":
        t = "wellF" if var_type == "Mean" else "well_d_r"
    elif mh == "RM_Choosing":
        t = "chRM" if var_type == "Mean" else "RMch_d_r"
    elif mh == "RM_Choosing - Male":
        t = "chRMM" if var_type == "Mean" else "RMch_d_m_r"
    elif mh == "RM_Choosing - Female":
        t = "chRMF" if var_type == "Mean" else "RMch_d_f_r"
    elif mh == "RM_Meeting":
        t = "mtRM" if var_type == "Mean" else "RMme_d_r"
    elif mh == "RM_Meeting - Male":
        t = "mtRMM" if var_type == "Mean" else "RMme_d_m_r"
    elif mh == "RM_Meeting - Female":
        t = "mtRMF" if var_type == "Mean" else "RMme_d_f_r"
    elif mh == "Suicide rate 2020":
        t = "suicide_rate_reg_tot" 
    elif mh == "Suicide rate 2020 - Male":
        t = "suicide_rate_reg_male" 
    elif mh == "Suicide rate 2020 - Female":
        t = "suicide_rate_reg_female" 
    
    ## set scales and labels
    if var_type == "Percentage":
        rc_f1 = False
        if "Depression" in mh: 
            label = "Percentage of people who say they are depressed/very depressed"
        elif "Loneliness" in mh: 
            label = "Percentage of people who say they are lonely/very lonely"
        elif "Well-being" in mh: 
            label = "Percentage of people who say they are dissatisfied/very dissatisfied with life"
        elif "RM_Choosing" in mh: 
            label = "Percentage of people who are above national avg for RM_choosing"
        elif "RM_Meeting" in mh: 
            label = "Percentage of people who are above national avg for RM_meetings"

    else:    
        if "Depression" in mh: 
            rc_f1 = (3,7)
            label = "Avg. response on depression (0 - Not at all depressed, 30 - Extremely depreseed)"
        elif "Loneliness" in mh: 
            rc_f1 = (11,15)
            label = "Avg. response on Loneliness (0 - Not at all lonely, 30 - Extremely lonely)"

        elif "Well-being" in mh: 
            rc_f1 = (17,20.5)
            label = "Avg. response on life satisfaction (0 - Extremely unsatisfied, 30 - Extremely satisfied)"

        elif "RM_Choosing" in mh: 
            rc_f1 = (24,27)
            label = "Avg. response on RM_choosing"

        elif "RM_Meeting" in mh: 
            rc_f1 = (16,18)
            label = "Avg. response on RM_meeting"

        elif "Suicide" in mh: 
            rc_f1 = (5,28)
            label = "Suicide rate (per 100,000 population)"

    if "Male" in mh:
        g_label = " [MALE]"
    elif "Female" in mh:
        g_label = " [FEMALE]"
    else:
        g_label = ""
    
    fig_1 = px.choropleth_mapbox(
        shp_1,
        geojson=shp.geometry,
        locations="ADM1_EN",
        color=t,
        hover_name = "RegionA",
        center=dict(lat=35.24, lon=139.32),
        mapbox_style="open-street-map",
        zoom=3,
        title = "Figure 1 - " + label + g_label,
        height = 500,
        width = 450,
        range_color = rc_f1,
        
        )
    if sb_type == "Compare 2 plots":

        ##functions for plot 2
        if mh_1 == "Depression": 
            t_1 = "dep0" if var_type_1 == "Mean" else "dep_d_r"
        elif mh_1 == "Depression - Male":
            t_1 = "dep0M" if var_type_1 == "Mean" else "dep_d_m_r"
        elif mh_1 == "Depression - Female":
            t_1 = "dep0F" if var_type_1 == "Mean" else "dep_d_f_r"
        elif mh_1 == "Loneliness":
            t_1 = "loneliness" if var_type_1 == "Mean" else "lon_d_r"
        elif mh_1 == "Loneliness - Male":
            t_1 = "lonelinessM" if var_type_1 == "Mean" else "lon_d_m_r"
        elif mh_1 == "Loneliness - Female":
            t_1 = "lonelinessF" if var_type_1 == "Mean" else "lon_d_f_r"
        elif mh_1 == "Well-being": 
            t_1 = "well" if var_type_1 == "Mean" else "well_d_r"
        elif mh_1 == "Well-being - Male":
            t_1 = "wellM" if var_type_1 == "Mean" else "well_d_r"
        elif mh_1 == "Well-being - Female":
            t_1 = "wellF" if var_type_1 == "Mean" else "well_d_r"
        elif mh_1 == "RM_Choosing":
            t_1 = "chRM" if var_type_1 == "Mean" else "RMch_d_r"
        elif mh_1 == "RM_Choosing - Male":
            t_1 = "chRMM" if var_type_1 == "Mean" else "RMch_d_m_r"
        elif mh_1 == "RM_Choosing - Female":
            t_1 = "chRMF" if var_type_1 == "Mean" else "RMch_d_f_r"
        elif mh_1 == "RM_Meeting":
            t_1 = "mtRM" if var_type_1 == "Mean" else "RMme_d_r"
        elif mh_1 == "RM_Meeting - Male":
            t_1 = "mtRMM" if var_type_1 == "Mean" else "RMme_d_m_r"
        elif mh_1 == "RM_Meeting - Female":
            t_1 = "mtRMF" if var_type_1 == "Mean" else "RMme_d_f_r"
        elif mh_1 == "Suicide rate 2020":
            t_1 = "suicide_rate_reg_tot"    
        elif mh_1 == "Suicide rate 2020 - Male":
            t_1 = "suicide_rate_reg_male"
        elif mh_1 == "Suicide rate 2020 - Female":
            t_1 = "suicide_rate_reg_female" 
            
    
        ## set scales and labels
        if var_type_1 == "Percentage":
            
            rc_f2 = False
            if "Depression" in mh_1: 
                
                label_1 = "Percentage of people who say they are depressed/very depressed"
            elif "Loneliness" in mh_1: 
                label_1 = "Percentage of people who say they are lonely/very lonely"
            elif "Well-being" in mh_1: 
                label_1 = "Percentage of people who say they are dissatisfied/very dissatisfied with life"
            elif "RM_Choosing" in mh_1: 
                label_1 = "Percentage of people who are above national avg for RM_choosing"
            elif "RM_Meeting" in mh_1: 
                label_1 = "Percentage of people who are above national avg for RM_meetings"

        else:
            
            if "Depression" in mh_1: 
                rc_f2 = (3,7)
                label_1 = "Avg. response on depression (0 - Not at all depressed, 30 - Extremely depreseed)"
            elif "Loneliness" in mh_1: 
                rc_f2 = (11,15)
                label_1 = "Avg. response on Loneliness (0 - Not at all lonely, 30 - Extremely lonely)"

            elif "Well-being" in mh_1: 
                rc_f2 = (17,20.5)
                label_1 = "Avg. response on life satisfaction (0 - Extremely unsatisfied, 30 - Extremely satisfied)"

            elif "RM_Choosing" in mh_1: 
                rc_f2 = (24,27)
                label_1 = "Avg. response on RM_choosing"

            elif "RM_Meeting" in mh_1: 
                rc_f2 = (16,18)
                label_1 = "Avg. response on RM_meeting"

            elif "Suicide" in mh_1: 
                rc_f2 = (5,28)
                label_1 = "Suicide rate (per 100,000 population)"

        if "Male" in mh_1:             
            g_label_1 = " [MALE]"
        elif "Female" in mh_1:
            g_label_1 = " [FEMALE]"
        else:
            g_label_1 = ""

        fig_2 = px.choropleth_mapbox(
            shp_1,
            geojson=shp.geometry,
            locations="ADM1_EN",
            color=t_1,
            hover_name = "RegionA",
            center=dict(lat=35.24, lon=139.32),
            mapbox_style="open-street-map",
            zoom=3,
            title = "Figure 2 - " + label_1 + g_label_1,
            height = 500,
            width = 450,
            range_color = rc_f2
            )
        #calculate pearsons correlation
        mes = 'Pearsons correlation: ' + str(rd_orig[t].corr(rd_orig[t_1]))[:6]


if sb_type == "Single plot":
    st.plotly_chart(fig_1, use_container_width=True)

if sb_type == "Compare 2 plots":
    st.write(mes)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_1, use_container_width=True)
    with col2:
        st.plotly_chart(fig_2, use_container_width=True)

