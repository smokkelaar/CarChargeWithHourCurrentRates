import brutonaarnetto as brutonaarnetto

#######################################################
###Input: List of prices
###Function: Get current, min and max price for list of prices
###Output: Current price, minimum price, maximumprice
#######################################################

def belangrijkewaarden(gegevens):
    huidigeprijs = gegevens[0][1]
    lijst = []
    for x in gegevens:
        lijst.append(x[1])
    lijst.sort()
    maximaleprijs = lijst[-3]
    minimaleprijs = lijst[0]
    
    huidigeprijs = brutonaarnetto.brutoprijs_naar_nettoprijs(huidigeprijs)
    minimaleprijs = brutonaarnetto.brutoprijs_naar_nettoprijs(minimaleprijs)
    maximaleprijs = brutonaarnetto.brutoprijs_naar_nettoprijs(maximaleprijs)
    
    return huidigeprijs, minimaleprijs, maximaleprijs