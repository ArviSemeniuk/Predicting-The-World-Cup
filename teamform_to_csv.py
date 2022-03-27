import csv
import pandas as pd

colsToRead = ["Year", "Location", "Average Yearly Temperature (Celsius)", "TeamA", "TeamB", "Round", "Full-time score TeamA", "Full-time score TeamB", "TeamA Elo Rating", "TeamB Elo Rating", "Form of TeamA", "Form of TeamB"]
cupData = pd.read_csv("worldcupdata.csv", encoding="latin-1", usecols=colsToRead) #Loading the data from the CSV file
teamDict = {} #Dictionary to store objects of type Team


#Class to store each teams recent performance
class Team:
	def __init__(self, name, recentResults):
		self.name = name
		self.recentResults = recentResults

	#Outcome of the match is added to the teams recent matches 
	def updateRecentResults(self, outcome):
		if len(self.recentResults) < 5:
			self.recentResults.append(outcome)
		else:
			self.recentResults.pop(0) #If the team already played 5 matches then delete the recent from 5 matches ago and add the newest match to the array 
			self.recentResults.append(outcome)

	def writeResultsToCSV(self, matchNum, home, outcome):
		if home == True:
			cupData.at[matchNum, "ResultsA"] = outcome
		else:
			cupData.at[matchNum, "ResultsB"] = outcome

	#Writes to the CSV file the new data that was calculated
	def writeFormToCSV(self, matchNum, home):
		#If the team has not played 5 matches yet than their form is set to neutral
		if len(self.recentResults) < 5:
			if home == True:
				cupData.at[matchNum, "Form of TeamA"] = "Neutral"
			else:
				cupData.at[matchNum, "Form of TeamB"] = "Neutral"
		else:
			Wins = self.recentResults.count("W")
			if Wins >= 3: #If the team has played 5 matches and has 3 or more wins then form is set to good
				if home == True:
					cupData.at[matchNum, "Form of TeamA"] = "Good" 
				else:
					cupData.at[matchNum, "Form of TeamB"] = "Good"
			elif Wins < 3:
				if home == True:
					cupData.at[matchNum, "Form of TeamA"] = "Bad"
				else:
					cupData.at[matchNum, "Form of TeamB"] = "Bad"


#List of teams that have participated in the World Cup since 1930. NOTE: Some teams don't exist anymore.
teams = ["Argentina", "Belgium", "Bolivia", "Brazil", "Chile", "France", "Mexico", "Paraguay", "Peru", "Romania", "United States", "Uruguay", "Yugoslavia", "Austria",
"Czechoslovakia", "Egypt", "Germany", "Hungary", "Italy", "Netherlands", "Spain", "Sweden", "Switzerland", "Cuba", "Dutch East Indies", "Norway",
"Poland", "England", "South Korea", "Scotland", "Turkey", "West Germany", "Northern Ireland", "Soviet Union", "Wales", "Bulgaria", "Colombia",
"North Korea", "Portugal", "El Salvador", "Israel", "Morocco", "Australia", "East Germany", "Haiti", "Zaire", "Iran", "Tunisia", "Algeria", "Cameroon",
"Honduras", "Kuwait", "New Zealand", "Canada", "Denmark", "Iraq", "Costa Rica", "Ireland", "United Arab Emirates", "Greece", "Nigeria",
"Saudi Arabia", "Germany", "Russia", "Croatia", "Jamaica", "Japan", "South Africa", "Yugoslavia", "China", "Ecuador", "Senegal", "Slovenia",
"Angola", "Cote d'Ivoire", "Ghana", "Togo", "Trinidad and Tobago", "Ukraine", "Czech Republic", "Slovakia", "Serbia", "Bosnia-Herzegovina", "Iceland", "Panama"]


#An instance of the Team class is created for every new team so that thir recent results can be stored. 
def updateResults(teamName, outcome, matchNum, home):
	if teamName in teams:
		teamDict[teamName] = Team(teamName, recentResults=[])
		teamDict[teamName].updateRecentResults(outcome)
		teams.remove(teamName)
	else:
		teamDict[teamName].updateRecentResults(outcome)
	
	teamDict[teamName].writeFormToCSV(matchNum, home)
	teamDict[teamName].writeResultsToCSV(matchNum, home, outcome)

	print(teamDict[teamName].name, " ", teamDict[teamName].recentResults) #This line is not needed but it just proves that the program works

	return teamDict


#Gets the results of each match and stores the outcome for each team. W = WIN, L = LOSS, D = DRAW
def getTeamResults():
	matchNum = 0 #Keeps track of the match number so that the appropriate row gets updated in the csv file
	home = True #Boolean value to store if the team was the home or away team

	#For loop to go through all the teams
	for teamA in cupData["TeamA"]:

		if cupData["Full-time score TeamA"].values[matchNum] > cupData["Full-time score TeamB"].values[matchNum]: #Gets result of the match
			updateResults(teamA, "W", matchNum, home)
			updateResults(cupData["TeamB"].values[matchNum], "L", matchNum, home=False)
		elif cupData["Full-time score TeamA"].values[matchNum] < cupData["Full-time score TeamB"].values[matchNum]:
			updateResults(teamA, "L", matchNum, home)
			updateResults(cupData["TeamB"].values[matchNum], "W", matchNum, home=False)
		else:
			updateResults(teamA, "D", matchNum, home)
			updateResults(cupData["TeamB"].values[matchNum], "D", matchNum, home=False)

		matchNum = matchNum + 1


getTeamResults() #Starting point for the program
cupData.to_csv("worldcupdata.csv") #Updates the CSV file