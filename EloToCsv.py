import math
import csv
import pandas as pd

colsToRead = ["Year", "Location", "Average Yearly Temperature (Celsius)", "TeamA", "TeamB", "Round", "Full-time score TeamA", "Full-time score TeamB", "TeamA Elo Rating", "TeamB Elo Rating", "Form of TeamA", "Form of TeamB"]
cupData = pd.read_csv("worldcupdata.csv", encoding="latin-1", usecols=colsToRead)
teams = {"Argentina" : 400, "Belgium" : 400, "Bolivia" : 400, "Brazil" : 400, "Chile" : 400, "France" : 400, "Mexico" : 400, "Paraguay" : 400, "Peru" : 400, "Romania" : 400, "United States" : 400, "Uruguay" : 400, "Yugoslavia" : 400, "Austria" : 400,
"Czechoslovakia" : 400, "Egypt" : 400, "Germany" : 400, "Hungary" : 400, "Italy" : 400, "Netherlands" : 400, "Spain" : 400, "Sweden" : 400, "Switzerland" : 400, "Cuba" : 400, "Dutch East Indies" : 400, "Norway" : 400,
"Poland" : 400, "England" : 400, "South Korea" : 400, "Scotland" : 400, "Turkey" : 400, "West Germany" : 400, "Northern Ireland" : 400, "Soviet Union" : 400, "Wales" : 400, "Bulgaria" : 400, "Colombia" : 400,
"North Korea" : 400, "Portugal" : 400, "El Salvador" : 400, "Israel" : 400, "Morocco" : 400, "Australia" : 400, "East Germany" : 400, "Haiti" : 400, "Zaire" : 400, "Iran" : 400, "Tunisia" : 400, "Algeria" : 400, "Cameroon" : 400,
"Honduras" : 400, "Kuwait" : 400, "New Zealand" : 400, "Canada" : 400, "Denmark" : 400, "Iraq" : 400, "Costa Rica" : 400, "Ireland" : 400, "United Arab Emirates" : 400, "Greece" : 400, "Nigeria" : 400,
"Saudi Arabia" : 400, "Germany" : 400, "Russia" : 400, "Croatia" : 400, "Jamaica" : 400, "Japan" : 400, "South Africa" : 400, "Yugoslavia" : 400, "China" : 400, "Ecuador" : 400, "Senegal" : 400, "Slovenia" : 400,
"Angola" : 400, "Cote d'Ivoire" : 400, "Ghana" : 400, "Togo" : 400, "Trinidad and Tobago" : 400, "Ukraine" : 400, "Czech Republic" : 400, "Slovakia" : 400, "Serbia" : 400, "Bosnia-Herzegovina" : 400, "Iceland" : 400, "Panama" : 400}
constant = 32
counter = 0

print(teams["Mexico"])

with open('worldcupdata.csv', 'r') as csvfile:
    datareader = csv.reader(csvfile)
    next(datareader)
    for row in datareader:
        if row[7] > row[8]:
            outcomeA = 1
            outcomeB = 0
        elif row[7] < row[8]:
            outcomeA = 0
            outcomeB = 1
        else:
            outcomeA, outcomeB = 0.5, 0.5

        ratingA = teams[row[4]]
        ratingB = teams[row[5]]

        expectedOutcomeA = 1 / (1 + pow(10, ((ratingB - ratingA) / 400)))
        expectedOutcomeB = 1 / (1 + pow(10, ((ratingA - ratingB) / 400)))

        newRatingA = teams[row[4]] + (constant * (outcomeA - expectedOutcomeA))
        newRatingB = teams[row[5]] + (constant * (outcomeB - expectedOutcomeB))

        print(row, end=" |||| ")
        print(ratingA, ratingB, end=" |||| ")

        teams[row[4]] = newRatingA
        teams[row[5]] = newRatingB

        print(newRatingA, newRatingB)