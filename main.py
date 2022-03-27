import pandas as pd
import numpy as np
import sklearn
from matplotlib import pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

class Network():
    def __init__(self, dataset, X):
        self.dataset = dataset
        self.X = X

    #Transform categorical data into numerical data using ohe for nominal variables
    def nominalEncoding(self):
        ohe = OneHotEncoder()
        self.X = ohe.fit_transform(self.dataset[["Location", "TeamA", "TeamB"]]).toarray()
        
        print(self.dataset)
        #print(self.X)
        self.ordinalEncoding()
    
    #Transform categorical data into numerical data using oe for ordinal variables
    def ordinalEncoding(self):
        oe = OrdinalEncoder(categories=[["Good", "Neutral", "Bad"], ["Good", "Neutral", "Bad"], ["W", "D", "L"], ["W", "D", "L"]])
        np.append(self.X, (oe.fit_transform(self.dataset[["Form of TeamA", "Form of TeamB", "ResultsA", "ResultsB"]])))
        
        print(self.X)
        self.scaler()
    
    #Scale numerical data to a standard range
    def scaler(self):
        X = self.dataset[["Year", "Average Yearly Temperature (Celsius)", "Round", "Full-time score TeamA", "Full-time score TeamB", "TeamA Elo Rating", "TeamB Elo Rating"]] #Don't scale the target variables
        #y1 = self.dataset[["ResultsA"]].to_numpy()
        scale = StandardScaler()
        scaledX = scale.fit_transform(X)
       
        #self.mlp(y1)

    def mlp(self, y):
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, y.ravel(), test_size=0.2, random_state=0) #Split the data into training and testing sets
        model = MLPClassifier(hidden_layer_sizes=(10), max_iter=1000, solver="adam", activation="tanh")
        model.fit(X_train, y_train)
        model.predict(X_test)
        print("Score of model: ", model.score(X_test, y_test))

        """
        plt.plot(model.loss_curve_)
        plt.xlabel("iteration")
        plt.ylabel("training loss")
        plt.show()
        """

    def plotData(self):
        x = self.dataset["Full-time score TeamB"]
        y = self.dataset["ResultsB"]

        plt.bar(y, x)

        plt.xlabel("Full-time score TeamB")
        plt.ylabel("ResultsB")
        plt.show()
        #print(self.dataset.corr(method= "pearson")) #correlation between the features
    
    # ~~~ End of class 'Network' ~~~

#Main program code
#cols = ["Year", "Location", "Average Yearly Temperature (Celsius)", "TeamA", "TeamB", "Round", "Full-time score TeamA", "Full-time score TeamB"]
world_cup_data = pd.read_csv("worldcupdata.csv", encoding="latin-1") #Loading the data from the csv file.

start = Network(world_cup_data, X=[])
start.nominalEncoding()
#start.plotData()