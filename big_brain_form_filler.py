import csv
import pandas as pd #if 'unresolved import' message appears, go to cmd and type 'pip install pandas' to install

teams = ["Argentina", "Belgium", "Bolivia", "Brazil", "Chile", "France", "Mexico", "Paraguay", "Peru", "Romania", "United States", "Uruguay", "Yugoslavia", "Austria",
"Czechoslovakia", "Egypt", "Germany", "Hungary", "Italy", "Netherlands", "Spain", "Sweden", "Switzerland", "Cuba", "Dutch East Indies", "Norway",
"Poland", "England", "South Korea", "Scotland", "Turkey", "West Germany", "Northern Ireland", "Soviet Union", "Wales", "Bulgaria", "Colombia",
"North Korea", "Portugal", "El Salvador", "Israel", "Morocco", "Australia", "East Germany", "Haiti", "Zaire", "Iran", "Tunisia", "Algeria", "Cameroon",
"Honduras", "Kuwait", "New Zealand", "Canada", "Denmark", "Iraq", "Costa Rica", "Republic of Ireland", "United Arab Emirates", "Greece", "Nigeria",
"Saudi Arabia", "Germany", "Russia", "Croatia", "Jamaica", "Japan", "South Africa", "FR Yugoslavia", "China PR", "Ecuador", "Senegal", "Slovenia",
"Angola", "Ivory Coast", "Ghana", "Togo", "Trinidad and Tobago", "Ukraine", "Czech Republic", "Slovakia", "Serbia", "Bosnia and Herzegovina", "Iceland", "Panama"]

scoreA = int()
scoreB = int()

winrec = int(0) #number of 'wins' across the past 5 matches

table = pd.read_csv("worldcupdata.csv") 

for x in teams:
    tempwin1 = 1 #these store the results of the previous 4 matches
    tempwin2 = 0
    tempwin3 = 1
    tempwin4 = 0
    currentwin = 0 #result of current match
    
    for row in table:
        if(x == TeamA or x == TeamB):
            #TODO: get and assign scores
            #scoreA = table.loc[row, 'Full-time score TeamA']?
            #scoreB = table.loc[row, 'Full-time score TeamB']?
            if(x == TeamA):   
                if (scoreA >= scoreB): #Full-time score TeamA >= Full-time score TeamB
                    currentwin = 1
                else:
                    currentwin = 0
                winrec = tempwin1 + tempwin2 + tempwin3 + tempwin4 + currentwin

                if(winrec >= 4):
                    table.loc[row, 'Form of TeamA'] = 'Good' 
                elif(winrec <= 1):
                    table.loc[row, 'Form of TeamA'] = 'Bad'
                else:
                    table.loc[row, 'Form of TeamA'] = 'Neutral'
            else:               
                 if (scoreB >= scoreA): #Full-time score TeamB >= Full-time score TeamA
                    currentwin = 1
                 else:
                    currentwin = 0
                 
                    winrec = tempwin1 + tempwin2 + tempwin3 + tempwin4 + currentwin

                 if(winrec >= 4):
                     table.loc[row, 'Form of TeamB'] = 'Good' 
                 elif(winrec <= 1):
                     table.loc[row, 'Form of TeamB'] = 'Bad'
                 else:
                     table.loc[row, 'Form of TeamB'] = 'Neutral'

            tempwin1 = tempwin2 #updates most recent matches
            tempwin2 = tempwin3
            tempwin3 = tempwin4
            tempwin4 = currentwin
           
