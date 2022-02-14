# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:11:51 2022

@author: robba
"""

import pandas as pd

pop = pd.read_excel("pop_jan1_2021_soumu.xlsx", skiprows=(2))
pop.columns
pop["pref"] = pop["団体コード"].str[:2]
pop.columns

pop["tot_pop"] = pop["人"]
pop["sex"] = pop["性別"]

pop = pop[["pref", "sex", "tot_pop"]]

pop_t = pop[pop["sex"] == "計"]
pop_m = pop[pop["sex"] == "男"]
pop_f = pop[pop["sex"] == "女"]

pop_t.to_csv("pop_tot_2021.csv")
pop_m.to_csv("pop_male_2021.csv")
pop_f.to_csv("pop_female_2021.csv")