from django import db
from flask import *
teams = ["Argentina", "Belgium", "Bolivia", "Brazil", "Chile", "France", "Mexico", "Paraguay", "Peru", "Romania", "United States", "Uruguay", "Yugoslavia", "Austria",
"Czechoslovakia", "Egypt", "Germany", "Hungary", "Italy", "Netherlands", "Spain", "Sweden", "Switzerland", "Cuba", "Dutch East Indies", "Norway",
"Poland", "England", "South Korea", "Scotland", "Turkey", "West Germany", "Northern Ireland", "Soviet Union", "Wales", "Bulgaria", "Colombia",
"North Korea", "Portugal", "El Salvador", "Israel", "Morocco", "Australia", "East Germany", "Haiti", "Zaire", "Iran", "Tunisia", "Algeria", "Cameroon",
"Honduras", "Kuwait", "New Zealand", "Canada", "Denmark", "Iraq", "Costa Rica", "Ireland", "United Arab Emirates", "Greece", "Nigeria",
"Saudi Arabia", "Germany", "Russia", "Croatia", "Jamaica", "Japan", "South Africa", "Yugoslavia", "China", "Ecuador", "Senegal", "Slovenia",
"Angola", "Cote d'Ivoire", "Ghana", "Togo", "Trinidad and Tobago", "Ukraine", "Czech Republic", "Slovakia", "Serbia", "Bosnia-Herzegovina", "Iceland", "Panama"]

app = Flask(__name__)


@app.route('/')
def Frontend(WinningTeam=None,ListOfTeams=teams):
    return render_template('main.html', WinningTeam=WinningTeam, ListOfTeams=ListOfTeams)

if __name__ == "__main__":
    app.run(debug=True, port=8080)