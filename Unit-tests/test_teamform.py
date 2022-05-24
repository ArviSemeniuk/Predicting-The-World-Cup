import unittest
import unittest.mock as mock
import pandas as pd
import os
import teamform_to_csv
from teamform_to_csv import Team

testData = teamform_to_csv.cupData
testData.to_csv("testingworldcupdata.csv", encoding='utf-8', index=False)

class TestTeam(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        testData = pd.DataFrame()
        with mock.patch("pandas.DataFrame.to_csv") as to_csv_mock:
            teamform_to_csv.updateCSV(testData, "testingworldcupdata.csv")
            to_csv_mock.assert_called_with("testingworldcupdata.csv", encoding='utf-8', index=False)

    @classmethod
    def tearDownClass(cls):
        os.remove("testingworldcupdata.csv")
    
    def setUp(self):
        self.teamA = Team("Lithuania", recentResults=["W", "L", "L", "W", "W"])
        self.teamB = Team("Estonia", recentResults=["D", "L", "L", "D", "D"])
        self.teamC = Team("Lativa", recentResults=["W", "W", "W"])
    
    def test_updateRecentResults(self):
        self.teamA.updateRecentResults("D")
        self.teamB.updateRecentResults("W")
        self.teamC.updateRecentResults("L")
        self.assertListEqual(self.teamA.recentResults, ["L", "L", "W", "W", "D"])
        self.assertListEqual(self.teamB.recentResults, ["L", "L", "D", "D", "W"])
        self.assertListEqual(self.teamC.recentResults, ["W", "W", "W", "L"])
    
    def test_writeResultsToCSV(self):
        self.teamA.writeResultsToCSV(0, True, "L")
        self.teamB.writeResultsToCSV(1, False, "L")
        self.teamC.writeResultsToCSV(1, True, "W")
        self.assertEqual(testData["ResultsA"].values[0], "L")
        self.assertEqual(testData["ResultsB"].values[1], "L")
        self.assertEqual(testData["ResultsA"].values[1], "W")
    
    def test_writeFormToCSV(self):
        self.teamA.writeFormToCSV(0, True)
        self.teamB.writeFormToCSV(1, True)
        self.teamC.writeFormToCSV(2, False)
        self.assertEqual(testData["Form of TeamA"].values[0], "Good")
        self.assertEqual(testData["Form of TeamA"].values[1], "Bad")
        self.assertEqual(testData["Form of TeamB"].values[2], "Neutral")

if __name__ == "__main__":
    unittest.main()
