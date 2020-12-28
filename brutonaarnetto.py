#######################################################
###Input: price including only 21% BTW
###Function: Add additional costs from easyenergy
###Output: price that needs to be paid
#######################################################


def brutoprijs_naar_nettoprijs(brutoprijs):
    nettomettoeslagen = float(brutoprijs) + 0.008 + 0.00053 + 0.15125 #kaleprijs + Easyenergyopslag + groene certificaten + Overheidsheffingen
    return nettomettoeslagen