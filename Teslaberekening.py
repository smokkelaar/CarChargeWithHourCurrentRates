#######################################################
###Input: current price, minimumprice, maximumprice and maximumcharge (optional)
###Function: Calculate best charging target
###Output: charging target
#######################################################


def TeslaBerekening(huidigeprijs = 0, minimaleprijs = 0, maximaleprijs = 0, maximalelading = 90):
    print ("huidige prijs op dit moment: ", huidigeprijs)
    print ("Minimaleprijs de komende uren: ", minimaleprijs)
    print ("Maximaleprijs de komende uren: ", maximaleprijs)
    lading = ((maximaleprijs-huidigeprijs)/(maximaleprijs-minimaleprijs))*maximalelading
    print (lading)
    return lading