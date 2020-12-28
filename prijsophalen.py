import PrijsEasyenergy as easy
import PrijsEntsoe as entsoe
import math

#######################################################
###Input: none
###Function: Get the day ahead prices from 1 of those. (easy or entsoe) including 21% tax.
###Output: List of upcoming prices so far as possible. in the format: list[time, price buy, price sell]
#######################################################

def prijsophalen():
    returnvaluesEasy = easy.Ophalen()
    returnvaluesEntsoe = entsoe.Ophalen()
    if (len(returnvaluesEasy) < len(returnvaluesEntsoe)):
        returnvalues = returnvaluesEntsoe
    else:
        returnvalues = returnvaluesEasy

    if (len(returnvaluesEasy)!= len(returnvaluesEntsoe)):
        print("aantal gegevens easy ", len(returnvaluesEasy))
        print("aantal gegevens entsoe ", len(returnvaluesEntsoe))
    if (float(returnvaluesEasy[0][1]) != float(returnvaluesEntsoe[0][1])):
        print("prijs dit uur easy " , returnvaluesEasy[0][1])
        print("prijs dit uur entsoe " , returnvaluesEntsoe[0][1])
    if (float(returnvaluesEasy[-1][1])!= float(returnvaluesEntsoe[-1][1])):
        print("prijs laatste uur easy " , returnvaluesEasy[-1][1])
        print("prijs laatste uur entsoe " , returnvaluesEntsoe[-1][1])
    return returnvalues
