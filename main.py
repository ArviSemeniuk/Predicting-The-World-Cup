import pandas as pd
import numpy as np
import sklearn
from matplotlib import pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

#Class to encapsulate the process of the machine learning life-cycle
#Prehaps I should give it a different name because network doesn't really make sense but oh well..
class Network():
    def __init__(self, dataset):
        self.dataset = dataset
        self.y = dataset["ResultsA"] #y is the output aka target feature. This is what we are trying to predict.
    
    #Method to visualise the data we have collected. At the moment it just plots goals scored against wins for teamA but it can be used to plot different features.
    def plotData(self):
        x = self.dataset["ResultsA"]
        y = self.dataset["Full-time score TeamA"]
        plt.bar(x, y)
        plt.xlabel("Full-time score TeamA")
        plt.ylabel("ResultsA")
        plt.show()
        #print(self.dataset.corr(method= "pearson")) #correlation between the features
    
    #Method to encode the data into a machine-friendly way. This makes the algorithms we use perform better. 
    def preprocessing(self):
        numericFeatures = ["Average Yearly Temperature (Celsius)", "Round", "Full-time score TeamA", "Full-time score TeamB", "TeamA Elo Rating", "TeamB Elo Rating"]
        nominalCatFeatures = ["Location", "TeamA", "TeamB"]
        ordinalCatFeatures = ["Form of TeamA", "Form of TeamB", "ResultsA"]

        numTransformer = StandardScaler() #Scale numerical data to a standard range
        ohe = OneHotEncoder() #Transform categorical data into numerical data using ohe for nominal variables
        oe = OrdinalEncoder(categories=[["Good", "Neutral", "Bad"], ["Good", "Neutral", "Bad"], ["W", "D", "L"]]) #Transform categorical data into numerical data using oe for ordinal variables

        ct = ColumnTransformer( #Here I specify what transformers will be used on what columns 
            transformers=[
                ("scaler", numTransformer, numericFeatures),
                ("ohe", ohe, nominalCatFeatures),
                ("oe", oe, ordinalCatFeatures)
            ], remainder="passthrough"
        )

        self.dataset = ct.fit_transform(self.dataset).toarray() # Here I'm actually transforming the data and concatenating the results
        #print(self.dataset)

    #Method is using the multi-layer perceptron classifier which is imported from sklearn to train the data.
    def mlp(self):
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, self.y, test_size=0.2) #Split the data into training and testing sets
        print(self.dataset.shape)
        print(self.y.shape) #Here I'm justing checking to see how many rows and columns our dataset has after preprocessing has been applied.

        model = MLPClassifier(hidden_layer_sizes=(100), max_iter=1000, solver="adam", activation="tanh") #Here the model is defined. The arguments given are random(I don't know how to tune them)
        model.fit(X_train, y_train) #Pass the training data to the model
        predictions = model.predict(X_test)#Predict the results on testing data
        print(predictions)
        
        score = accuracy_score(y_test, predictions) #Calculated the accuracy of the predictions
        print("score: ", score)

        #print(cross_val_score(model, self.dataset, self.y)) #Not sure how to cross-vallidate
        
        #learning (loss curve) is plotted
        plt.plot(model.loss_curve_)
        plt.xlabel("iteration")
        plt.ylabel("training loss")
        plt.show()
    
    #LogisticRegression is used (I know it has regression in the name but its a classifier)
    #I do the same thing as in the mlp method but I'm just playing around to see what results this model gives us
    def logReg(self):
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, self.y, test_size=0.2) #Split the data into training and testing sets
        model = LogisticRegression(solver="lbfgs", max_iter=900).fit(X_train, y_train)
        pred = model.predict(X_test)
        print(pred)

        score = model.score(X_test, y_test)
        print(score)

        
    # ~~~ End of class 'Network' ~~~

#Main program code
world_cup_data = pd.read_csv("worldcupdata.csv", encoding="latin-1") #Loading the data from the csv file.

start = Network(world_cup_data) #Create instance of the Network class. Pass in the world cup data
#start.plotData()
start.preprocessing() #First preprocessing is done...
start.mlp() #...then I start training the data
#start.logReg()