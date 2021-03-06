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
    testNewData = pd.DataFrame()

    def __init__(self, dataset):
        self.dataset = dataset.drop("ResultsA", axis=1)
        self.y = dataset[["ResultsA"]] #y is the output aka target feature. This is what we are trying to predict.
    
    #Method to visualise the data we have collected. At the moment it just plots goals scored against wins for teamA but it can be used to plot different features.
    def plotData(self):
        x = self.y["ResultsA"]
        y = self.dataset["Full-time score TeamA"]
        plt.bar(x, y)
        plt.xlabel("Full-time score TeamA")
        plt.ylabel("ResultsA")
        plt.show()
        #print(self.dataset.corr(method= "pearson")) #correlation between the features
    
    #Method to encode the data into a machine-friendly way. This makes the algorithms we use perform better. 
    def preprocessing(self, newDF):
        numericFeatures = ["Year", "Average Yearly Temperature (Celsius)", "Round", "TeamA Elo Rating", "TeamB Elo Rating"]
        nominalCatFeatures = ["Location", "TeamA", "TeamB"]
        ordinalCatFeatures = ["Form of TeamA", "Form of TeamB"]

        numTransformer = StandardScaler() #Scale numerical data to a standard range
        ohe = OneHotEncoder() #Transform categorical data into numerical data using ohe for nominal variables
        oe = OrdinalEncoder(categories=[["Good", "Neutral", "Bad"], ["Good", "Neutral", "Bad"]]) #Transform categorical data into numerical data using oe for ordinal variables
        yEncoder = OrdinalEncoder(categories=[["W", "D", "L"]])

        ct = ColumnTransformer( #Here I specify what transformers will be used on what columns 
            transformers=[
                ("scaler", numTransformer, numericFeatures),
                ("ohe", ohe, nominalCatFeatures),
                ("oe", oe, ordinalCatFeatures)
            ], remainder="passthrough"
        )

        self.dataset = ct.fit_transform(self.dataset).toarray() # Here I'm actually transforming the data and concatenating the results
        self.y = yEncoder.fit_transform(self.y)
        self.y = self.y.ravel()
        #print(self.y)
        self.testNewData = ct.transform(newDF)
        #print(self.testNewData)

    #Method is using the multi-layer perceptron classifier which is imported from sklearn to train the data.
    def mlp(self):
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, self.y, test_size=0.2) #Split the data into training and testing sets
        print(self.dataset.shape)
        print(self.y.shape) #Here I'm justing checking to see how many rows and columns our dataset has after preprocessing has been applied.

        model = MLPClassifier(hidden_layer_sizes=(10,10,10), max_iter=400, solver="sgd", activation="tanh", learning_rate="adaptive") #Here the model is defined. The arguments given are random(I don't know how to tune them)
        model.fit(X_train, y_train) #Pass the training data to the model
        predictions = model.predict(X_test)#Predict the results on testing data
        #print(predictions)
        
        newPred = model.predict(self.testNewData)
        #print(newPred)
        
        score = accuracy_score(y_test, predictions) #Calculated the accuracy of the predictions
        return (newPred, score)

        #print(cross_val_score(model, self.dataset, self.y)) #Not sure how to cross-vallidate
        
        #learning (loss curve) is plotted
        #plt.plot(model.loss_curve_)
        #plt.xlabel("iteration")
        #plt.ylabel("training loss")
        #plt.show()
    
    #LogisticRegression is used (I know it has regression in the name but its a classifier)
    #I do the same thing as in the mlp method but I'm just playing around to see what results this model gives us
    def logReg(self):
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, self.y, test_size=0.2, random_state=4) #Split the data into training and testing sets
        model = LogisticRegression(solver="newton-cg", C=26)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        #print(pred)

        newPred = model.predict(self.testNewData)
        print(newPred)

        scores = cross_val_score(model, self.dataset, self.y, cv=10, scoring="accuracy")
        print(scores.mean())
        #self.modelEvaluation()
    
    def modelEvaluation(self):
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, self.y, test_size=0.2, random_state=4)
        cRange = range(1, 50)
        cScores = []
        
        for i in cRange:
            model = LogisticRegression(solver="newton-cg", C=i)
            scores = cross_val_score(model, X_train, y_train, cv=10, scoring="accuracy")
            cScores.append(scores.mean())
        
        plt.plot(cRange, cScores)
        plt.title("Hyperparameter tuning 'C' value")
        plt.xlabel("C value")
        plt.ylabel("Cross-Validated Accuracy")
        plt.show()
    
    def hyperparameterTuning(self):
        X_train, X_test, y_train, y_test = train_test_split(self.dataset, self.y, test_size=0.2, random_state=4)
        model = MLPClassifier(max_iter=400)

        parameterSpace = {
            "hidden_layer_sizes": [(10, 10, 10)],
            "activation": ['tanh', 'relu'],
            "solver": ['sgd', 'adam'],
            "learning_rate": ['constant', 'adaptive'],
        }

        from sklearn.model_selection import GridSearchCV

        clf = GridSearchCV(model, parameterSpace, n_jobs=-1, cv=5)
        clf.fit(X_train, y_train)

        print("Best parameter found:\n", clf.best_params_)

    # ~~~ End of class 'Network' ~~~

#Main program code
def main (TeamA, TeamB):
    world_cup_data = pd.read_csv("worldcupdata.csv", encoding="latin-1") #Loading the data from the csv file.
    world_cup_data = world_cup_data.drop(["Full-time score TeamA", "Full-time score TeamB", "ResultsB"], axis=1) #Exculde these columns from dataframe
    newData = [[2022, "Brazil", 26, TeamA, TeamB, 1, "Error", "Error", "Error", "Error"]] #Set to ELo/Forms to Error, as it is incorrect input and will throw error if not set correctly later

    #Set Elo and Form as correct for each team
    LastRowA = world_cup_data.loc[(world_cup_data["TeamA"] == TeamA) | (world_cup_data["TeamB"] == TeamA)] #Gets each row where Team A has played
    LastRowB = world_cup_data.loc[(world_cup_data["TeamA"] == TeamB) | (world_cup_data["TeamB"] == TeamB)]
    LastRowA = LastRowA.iloc[-1:, :] #Cuts down to last row
    LastRowB = LastRowB.iloc[-1:, :]
    #Allocates correct Elo and form to each Team
    if TeamA in set(LastRowA["TeamA"]):
        newData[0][6] = LastRowA.iat[0,6]
        newData[0][8] = LastRowA.iat[0,8]
    elif TeamA in set(LastRowA["TeamB"]):
        newData[0][6] = LastRowA.iat[0,7]
        newData[0][8] = LastRowA.iat[0,9]
    if TeamB in set(LastRowB["TeamA"]):
        newData[0][7] = LastRowB.iat[0,6]
        newData[0][9] = LastRowA.iat[0,8]
    elif TeamB in set(LastRowB["TeamB"]):
        newData[0][7] = LastRowB.iat[0,7]
        newData[0][9] = LastRowA.iat[0,9]

    newDF = pd.DataFrame(newData, columns=["Year", "Location", "Average Yearly Temperature (Celsius)", "TeamA", "TeamB", "Round","TeamA Elo Rating","TeamB Elo Rating","Form of TeamA","Form of TeamB"])

    start = Network(world_cup_data) #Create instance of the Network class. Pass in the world cup data
    #start.plotData() #Initial data analysis
    start.preprocessing(newDF) #First preprocessing is done. newDF corresponds to the user input from the front-end
    #start.logReg() #Logistic Regression was used to compare two different ML models for accuracy. MLP seems to perform better
    #start.modelEvaluation() #This method used to tune a specific hyperparameter used in logistic regression to increase performnace
    #start.hyperparameterTuning() #What hyperparameters produce a better model for MLP
    return start.mlp() #Now I start training the the model on the data that was transformed and the parameters that produce the best accuracy