import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

#cols = ["Year", "Location", "Average Yearly Temperature (Celsius)", "TeamA", "TeamB", "Round", "Full-time score TeamA", "Full-time score TeamB"]
world_cup_data = pd.read_csv("worldcupdata.csv", encoding="latin-1") #Loading the data from the csv file. 

#Transform categorical data into numerical data using ohe for nominal variables and oe for ordinal variables
ohe = OneHotEncoder()
encodedNominal = ohe.fit_transform(world_cup_data[["Location", "TeamA", "TeamB"]]).toarray()
print(encodedNominal)

oe = OrdinalEncoder(categories=[["Good", "Neutral", "Bad"], ["Good", "Neutral", "Bad"]])
encodedOrdinal = oe.fit_transform(world_cup_data[["Form of TeamA", "Form of TeamB"]])
print(oe.categories_)
print(encodedOrdinal)

#Scale numerical data to a standard range
X = world_cup_data[["Year", "Average Yearly Temperature (Celsius)", "Round"]]
y = world_cup_data[["Full-time score TeamA", "Full-time score TeamB"]]
scale = StandardScaler()

scaledX = scale.fit_transform(X)
scaledY = scale.fit_transform(y)

print(scaledX)

#Multioutput Regression ~~~ Everything below this line needs fixing to get the model to work ~~~
model = LinearRegression()

print(type(scaledX))
print(type(encodedNominal))
print(type(encodedOrdinal))

a = np.append(scaledX, encodedNominal)
b = np.append(a, encodedOrdinal)
print(b)

#model.fit(scaledX, scaledY)

#print("Start here")
#print(model.coef_)

#predictScore = model.predict(X)
#print(predictScore)