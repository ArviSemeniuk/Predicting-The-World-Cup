ratingA = 350
ratingB = 450
constant = 32
outcomeA = 1
outcomeB = 0

expectedOutcomeA = round(1 / (1 + pow(10, ((ratingB - ratingA) / 400))), 5)
expectedOutcomeB = round(1 / (1 + pow(10, ((ratingA - ratingB) / 400))), 5)
newRatingA = ratingA + (constant * (outcomeA - expectedOutcomeA))
newRatingB = ratingB + (constant * (outcomeB - expectedOutcomeB))

expectedOutcomeATest = 0.35994
expectedOutcomeBTest = 0.64006

newRatingATest = 370.48192
newRatingBTest = 429.51808

if expectedOutcomeA == expectedOutcomeATest:
    print("Test 1 successful.")
else:
    print("Test 1 unsuccessful")

if expectedOutcomeB == expectedOutcomeBTest:
    print("Test 2 successful.")
else:
    print("Test 2 unsuccessful")

if newRatingA == newRatingATest:
    print("Test 3 successful")
else:
    print("Test 3 unsuccessful")

if newRatingB == newRatingBTest:
    print("Test 4 successful")
else:
    print("Test 4 unsuccessful")

