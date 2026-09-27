"""
Script takes all match report files scraped from fb-ref.com and concatenates them into a single csv file
"""

import pandas as pd 
import glob
import os

os.chdir("lic")

folders = os.listdir()

df = pd.DataFrame()

files = glob.glob("**/**/*.csv", recursive=True)
for file in files: 
    d = pd.read_csv(file)
    df = pd.concat([df, d], axis=0)

df.drop("Unnamed: 0", axis=1, inplace=True)

df["league"] = 'ITA'
df = df[["league", "season", "team_name", "match_date", "comp", "venue", "opponent", "match_id", 
           "Player", "#", "Nation", "Pos", "Age", "Min", "Gls", "Ast", "PK", "PKatt", "Sh", "SoT", 
           "CrdY", "CrdR", "Fls", "Fld", "Off", "Crs", "TklW", "Int", "OG", "PKwon", "PKcon"]]

df.to_csv("lic_match_report_data.csv", index=False)