# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 13:26:39 2022

@author: robba
"""

import pandas as pd

reg = pd.read_excel("region_RM.xlsx")

s_t = pd.read_csv("suiciderate_full_reg_2020.csv")[["RegionA", "suicide_rate_reg_tot"]]
s_m = pd.read_csv("suiciderate_male_reg_2020.csv")[["RegionA", "suicide_rate_reg_male"]]
s_f = pd.read_csv("suiciderate_female_reg_2020.csv")[["RegionA", "suicide_rate_reg_female"]]

reg = pd.merge(reg, s_t, on = "RegionA")
reg = pd.merge(reg, s_m, on = "RegionA")
reg = pd.merge(reg, s_f, on = "RegionA")
reg.to_csv("region_RM_RNFeb14.csv")