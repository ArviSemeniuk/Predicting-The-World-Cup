from flask import * #Imports website framework
from main import * #Imports actual model

#The list of teams that can be selected from the dropdown lists, contains all (and only) the countries listed in the CSV
teams = ["Argentina", "Belgium", "Bolivia", "Brazil", "Chile", "France", "Mexico", "Paraguay", "Peru", "Romania", "United States", "Uruguay", "Yugoslavia", "Austria",
"Czechoslovakia", "Egypt", "Germany", "Hungary", "Italy", "Netherlands", "Spain", "Sweden", "Switzerland", "Cuba", "Dutch East Indies", "Norway",
"Poland", "England", "South Korea", "Scotland", "Turkey", "West Germany", "Northern Ireland", "Soviet Union", "Wales", "Bulgaria", "Colombia",
"North Korea", "Portugal", "El Salvador", "Israel", "Morocco", "Australia", "East Germany", "Haiti", "Zaire", "Iran", "Tunisia", "Algeria", "Cameroon",
"Honduras", "Kuwait", "New Zealand", "Canada", "Denmark", "Iraq", "Costa Rica", "Ireland", "United Arab Emirates", "Greece", "Nigeria",
"Saudi Arabia", "Germany", "Russia", "Croatia", "Jamaica", "Japan", "South Africa", "Yugoslavia", "China", "Ecuador", "Senegal", "Slovenia",
"Angola", "Cote d'Ivoire", "Ghana", "Togo", "Trinidad and Tobago", "Ukraine", "Czech Republic", "Slovakia", "Serbia", "Bosnia-Herzegovina", "Iceland", "Panama"]

app = Flask(__name__) #Generates framework, Neccessary to run

#Creates home/initial webpage
@app.route('/', methods=['GET', 'POST'])
def Frontend(ListOfTeams=teams):

    #Renders Website
    return render_template('main.html', ListOfTeams=ListOfTeams)

#Creates webpage for after results submitted
@app.route('/Results', methods=['GET', 'POST'])
def Results(WinningTeam=None):
    TeamA = request.form.get('Team 1')
    TeamB = request.form.get('Team 2')

    #Catches Error if same team entered twice
    if TeamA != TeamB:
        #Get Results as tuple from main
        RawResults = main(TeamA,TeamB) #Home Team = Team A, Away Team = Team B
        #Turn first result (Winner) into more legible form
        if "0" in str(RawResults[0]):
            Results = "TeamA Win"
        elif "1" in str(RawResults[0]):
            Results = "Draw"
        elif "2" in str(RawResults[0]):
            Results = "TeamB Win"
        #Turn second result (Accuracy) into more presentable form
        Accuracy = RawResults[1]
        Accuracy = str(round(Accuracy, 3))
        Accuracy += "%"
    #Registers Error if same team entered twice
    else:
        Results = "Error"
        Accuracy = "Error"

    #Renders Website
    return render_template('Results.html', WinningTeam=WinningTeam, TeamA=TeamA, TeamB=TeamB, Results=Results, Accuracy=Accuracy)

#Runs the App, Neccesary to run (Debug changed to False just before submission for self explainatory reasons)
if __name__ == "__main__":
    app.run(debug=False, port=8080)