import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

cols = ["Year", "Location", "Average Yearly Temperature (Celsius)", "TeamA", "TeamB", "Round", "Full-time score TeamA", "Full-time score TeamB"]
world_cup_data = pd.read_csv("worldcupdata.csv", encoding="cp1252", usecols=cols) #Loading the data from the csv file. 

labelencoder = LabelEncoder()
world_cup_data["Location"] = labelencoder.fit_transform(world_cup_data["Location"])
world_cup_data["TeamA"] = labelencoder.fit_transform(world_cup_data["TeamA"])
world_cup_data["TeamB"] = labelencoder.fit_transform(world_cup_data["TeamB"])
#world_cup_data["Form of TeamA"] = labelencoder.fit_transform(world_cup_data["Form of TeamA"])
#world_cup_data["Form of TeamB"] = labelencoder.fit_transform(world_cup_data["Form of TeamB"])

hotencoder = OneHotEncoder(handle_unknown="ignore")
encoded_df = pd.DataFrame(hotencoder.fit_transform(world_cup_data[["Location"]]).toarray())

world_cup_data = world_cup_data.join(encoded_df)
world_cup_data