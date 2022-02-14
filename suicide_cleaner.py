# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 13:07:43 2022

@author: robba
"""

#### Training on using streamlit

import os
import pandas as pd
import streamlit as st


fil = os.listdir("mhlw_2020")

##get only A5 files

a7_files = [fil for fil in fil if "A5" in fil]

data_full = pd.DataFrame()
for b in range(len(a7_files)):
    print(str(b) + " / " + str(len(a7_files)))
    data = pd.read_excel("mhlw_2020/" + a7_files[b])

    ##create new column names
    n_1 = data.iloc[2]
    n_1 = n_1.fillna(method='ffill')
    n_2 = data.iloc[3]
    n_2 = n_2.fillna(method='ffill')
    n_3 = data.iloc[4]
    n_4 = data.iloc[5]

    names = []
    for i in range(0, len(n_1)): 
        #print(str(n_1[i]) + str(n_2[i]) + str(n_3[i]) + str(n_4[i]))
        names.append(str(n_1[i]) + " " + str(n_2[i]) + " " + str(n_3[i])+ " " + str(n_4[i]))
        names[i] = names[i].replace("nan", "")
    data.columns = names    
    
    ##cut the 6 first rows
    data = data.iloc[6: , :]

    ##get year and month data
    data["year"] = a7_files[b].split("-")[0]
    data["month"] = a7_files[b].split("-")[1]
    

    data_full = data_full.append(data)   
##save result to disc
data_full.to_csv("mhlw_A5_combined_2019-2020.csv")
##get only pref_id and suicide rate
data_full["pref"] = data_full["都道府県コード   "]
data_full["suicide_rate_2020"] = data_full['自殺死亡率   ']
data_2 = data_full[["pref", "suicide_rate_2020"]]
data_2.to_csv("suiciderate_full_2020.csv")

##calculate regional suicide rate
pop = pd.read_csv("pop_tot_2021.csv")
pop = pop[1:]
pop["pref"] = pop["pref"].astype(int)
data_full.columns
data_full["pref"] = data_full["都道府県コード   "]
data_full["suicide_n"] = data_full['自殺者数   ']
data_3 = data_full[["pref", "suicide_n"]]
data_3 = pd.merge(data_3, pop, on = ["pref"])
reg = pd.read_excel("regionsRN.xlsx")
reg = reg.rename(columns={"ken":"pref"})
data_3 = pd.merge(data_3, reg, on = ["pref"])
data_3["suicide_n"] = data_3["suicide_n"].astype(int)

data_3 = data_3.groupby("RegionA").sum().reset_index()
data_3["suicide_rate_reg_tot"] = data_3["suicide_n"]/(data_3["tot_pop"]/100000)
data_3.columns
data_3 = data_3[["RegionA", "suicide_rate_reg_tot"]]
data_3.to_csv("suiciderate_full_reg_2020.csv")



##get only A5 files

a7_files = [fil for fil in fil if "A5" in fil]

data_full = pd.DataFrame()
for b in range(len(a7_files)):
    print(str(b) + " / " + str(len(a7_files)))
    data = pd.read_excel("mhlw_2020/" + a7_files[b], sheet_name=1)

    ##create new column names
    n_1 = data.iloc[2]
    n_1 = n_1.fillna(method='ffill')
    n_2 = data.iloc[3]
    n_2 = n_2.fillna(method='ffill')
    n_3 = data.iloc[4]
    n_4 = data.iloc[5]

    names = []
    for i in range(0, len(n_1)): 
        #print(str(n_1[i]) + str(n_2[i]) + str(n_3[i]) + str(n_4[i]))
        names.append(str(n_1[i]) + " " + str(n_2[i]) + " " + str(n_3[i])+ " " + str(n_4[i]))
        names[i] = names[i].replace("nan", "")
    data.columns = names    
    
    ##cut the 6 first rows
    data = data.iloc[6: , :]

    ##get year and month data
    data["year"] = a7_files[b].split("-")[0]
    data["month"] = a7_files[b].split("-")[1]
    

    data_full = data_full.append(data)   
##save result to disc
data_full.to_csv("mhlw_A5_male_combined_2019-2020.csv")
##get only pref_id and suicide rate
data_full["pref"] = data_full["都道府県コード   "]
data_full["suicide_rate_male_2020"] = data_full['自殺死亡率   ']
data_2 = data_full[["pref", "suicide_rate_male_2020"]]
data_2.to_csv("suiciderate_male_2020.csv")

##calculate regional suicide rate
pop = pd.read_csv("pop_male_2021.csv")
pop = pop[1:]
pop["pref"] = pop["pref"].astype(int)
data_full.columns
data_full["pref"] = data_full["都道府県コード   "]
data_full["suicide_n"] = data_full['自殺者数   ']
data_3 = data_full[["pref", "suicide_n"]]
data_3 = pd.merge(data_3, pop, on = ["pref"])
reg = pd.read_excel("regionsRN.xlsx")
reg = reg.rename(columns={"ken":"pref"})
data_3 = pd.merge(data_3, reg, on = ["pref"])
data_3["suicide_n"] = data_3["suicide_n"].astype(int)

data_3 = data_3.groupby("RegionA").sum().reset_index()
data_3["suicide_rate_reg_male"] = data_3["suicide_n"]/(data_3["tot_pop"]/100000)
data_3 = data_3[["RegionA", "suicide_rate_reg_male"]]
data_3.to_csv("suiciderate_male_reg_2020.csv")

##get only A5 files

a7_files = [fil for fil in fil if "A5" in fil]

data_full = pd.DataFrame()
for b in range(len(a7_files)):
    print(str(b) + " / " + str(len(a7_files)))
    data = pd.read_excel("mhlw_2020/" + a7_files[b], sheet_name=2)

    ##create new column names
    n_1 = data.iloc[2]
    n_1 = n_1.fillna(method='ffill')
    n_2 = data.iloc[3]
    n_2 = n_2.fillna(method='ffill')
    n_3 = data.iloc[4]
    n_4 = data.iloc[5]

    names = []
    for i in range(0, len(n_1)): 
        #print(str(n_1[i]) + str(n_2[i]) + str(n_3[i]) + str(n_4[i]))
        names.append(str(n_1[i]) + " " + str(n_2[i]) + " " + str(n_3[i])+ " " + str(n_4[i]))
        names[i] = names[i].replace("nan", "")
    data.columns = names    
    
    ##cut the 6 first rows
    data = data.iloc[6: , :]

    ##get year and month data
    data["year"] = a7_files[b].split("-")[0]
    data["month"] = a7_files[b].split("-")[1]
    

    data_full = data_full.append(data)   
##save result to disc
data_full.to_csv("mhlw_A5_female_combined_2019-2020.csv")
##get only pref_id and suicide rate
data_full["pref"] = data_full["都道府県コード   "]
data_full["suicide_rate_female_2020"] = data_full['自殺死亡率   ']
data_2 = data_full[["pref", "suicide_rate_female_2020"]]
data_2.to_csv("suiciderate_female_2020.csv")

##calculate regional suicide rate
pop = pd.read_csv("pop_female_2021.csv")
pop = pop[1:]
pop["pref"] = pop["pref"].astype(int)
data_full.columns
data_full["pref"] = data_full["都道府県コード   "]
data_full["suicide_n"] = data_full['自殺者数   ']
data_3 = data_full[["pref", "suicide_n"]]
data_3 = pd.merge(data_3, pop, on = ["pref"])
reg = pd.read_excel("regionsRN.xlsx")
reg = reg.rename(columns={"ken":"pref"})
data_3 = pd.merge(data_3, reg, on = ["pref"])
data_3["suicide_n"] = data_3["suicide_n"].astype(int)

data_3 = data_3.groupby("RegionA").sum().reset_index()
data_3["suicide_rate_reg_female"] = data_3["suicide_n"]/(data_3["tot_pop"]/100000)
data_3 = data_3[["RegionA", "suicide_rate_reg_female"]]
data_3.to_csv("suiciderate_female_reg_2020.csv")





























