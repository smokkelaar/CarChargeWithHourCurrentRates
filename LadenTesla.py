import datetime as dt
import requests
import json
import Tesla.teslapy as teslapy
from bs4 import BeautifulSoup

CLIENT_ID='81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
CLIENT_SECRET='c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
MAXIMAAL_LADEN_TOT = 90

def brutoprijs_naar_nettoprijs(brutoprijs, Easyenergybron = 0):
    if(not Easyenergybron):
        brutocentkwh = brutoprijs / 1000
        brutoprijs = brutocentkwh * 1.21
    nettomettoeslagen = brutoprijs + 0.008 + 0.00053 + 0.15125 #kaleprijs + Easyenergyopslag + groene certificaten + Overheidsheffingen
    return nettomettoeslagen

def Teslaladen(procent):
    with teslapy.Tesla("email tesla account", "wachtwoord tesla account", CLIENT_ID, CLIENT_SECRET) as tesla:
        tesla.fetch_token()
        print (procent)
        vehicles = tesla.vehicle_list()
        vehicles[0].sync_wake_up()
        try:
            print (vehicles[0].get_vehicle_data()["charge_state"])
        except:
            print ("kon voertuig gegevens niet ophalen")
        if (procent < 0):
            try:
                vehicles[0].command('STOP_CHARGE')
            except:
                print ("Laden kan niet uitgezet worden, stond waarschijnlijk al uit")
            return
        if (procent < 50):
            procent = 50
        try:
            vehicles[0].command('CHANGE_CHARGE_LIMIT', percent=procent)
        except:
            print ("Kan laad precentage niet zetten, waarschijnlijk is deze niet veranderd")
        try:
            vehicles[0].command('START_CHARGE')
        except:
            print ("Laden kan niet aangezet worden, stond waarschijnlijk al aan")
        return

def Ophalen_entsoe():
    nu = dt.datetime.now(dt.timezone.utc)
    morgen = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)
    urlvandaag = "https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime="+str(nu.day)+"."+str(nu.month)+"."+str(nu.year)+"+00:00|CET|DAY&biddingZone.values=CTY|10YNL----------L!BZN|10YNL----------L&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)"
    urlmorgen = "https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime="+str(morgen.day)+"."+str(morgen.month)+"."+str(morgen.year)+"+00:00|CET|DAY&biddingZone.values=CTY|10YNL----------L!BZN|10YNL----------L&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)"
    print (urlvandaag)
    print (urlmorgen)
    pagevandaag = requests.get(urlvandaag)
    pagemorgen = requests.get(urlmorgen)
    soupv = BeautifulSoup(pagevandaag.text, 'html.parser')
    soupm = BeautifulSoup(pagemorgen.text, 'html.parser')
    price_hidev = soupv.find_all(class_='dv-value-cell')
    price_hidem = soupm.find_all(class_='dv-value-cell')
    returnvalues = []
    for price in price_hidev:
        noISOdatum = str(price).split("\', \'")[2]
        datum = dt.datetime.fromisoformat(noISOdatum[:-1])
        if ((datum.timestamp() - nu.timestamp()) >= -3600):
            #print (price.text)
            returnvalues.append([datum, str(price.text), str(price.text)])
    for price in price_hidem:
        noISOdatum = str(price).split("\', \'")[2]
        datum = dt.datetime.fromisoformat(noISOdatum[:-1])
        if ((datum.timestamp() - nu.timestamp()) >= -3600):
            #print (price.text)
            returnvalues.append([datum, str(price.text), str(price.text)])
    return returnvalues, 0

def Ophalen():
    bron = 1
    nu = dt.datetime.now(dt.timezone.utc)- dt.timedelta(days=1)
    morgen = dt.datetime.now(dt.timezone.utc)
    urlvandaag = "https://mijn.easyenergy.com/nl/api/tariff/getapxtariffs?startTimestamp="+str(nu.year)+"-"+str(nu.month)+"-"+str(nu.day)+"&endTimestamp=2100-01-01&grouping="
    urlmorgen = "https://mijn.easyenergy.com/nl/api/tariff/getapxtariffs?startTimestamp="+str(morgen.year)+"-"+str(morgen.month)+"-"+str(morgen.day)+"&endTimestamp=2100-01-01&grouping="
    print (urlvandaag)
    print (urlmorgen)
    print (morgen)
    responsev = requests.get(urlvandaag, verify=False)
    cv = json.loads(responsev.text)
    returnvalues = []
    for x in cv:
        datum = dt.datetime.fromisoformat(x['Timestamp'])
        print (datum)
        if ((datum.timestamp() - morgen.timestamp()) >= -3600):
            print (x['TariffUsage'])
            returnvalues.append([datum, x['TariffUsage'], x['TariffReturn']])
    if (len(returnvalues) < 10):
        print("te weinig input! letop! bron geeft niet genoeg informatie, TODO mail naar easyenergie en naar mij")
    if (len(returnvalues) < 4):
        print ("er zijn geen of te weinig gegevens opgehaald bij easyenergy dus wordt er overgeschakeld naar entsoe")
        returnvalues, bron = Ophalen_entsoe()
    return returnvalues, bron

def belangrijkewaarden(gegevens, bron):
    huidigeprijs = gegevens[0][1]
    lijst = []
    for x in gegevens:
        lijst.append(x[1])
    lijst.sort()
    maximaleprijs = lijst[-3]
    minimaleprijs = lijst[0]


    huidigeprijs = brutoprijs_naar_nettoprijs(huidigeprijs, bron)
    minimaleprijs = brutoprijs_naar_nettoprijs(minimaleprijs, bron)
    maximaleprijs = brutoprijs_naar_nettoprijs(maximaleprijs, bron)


    return huidigeprijs, minimaleprijs, maximaleprijs


def TeslaBerekening(huidigeprijs = 0, minimaleprijs = 0, maximaleprijs = 0, maximalelading = 90):
    print ("huidige prijs op dit moment: ", huidigeprijs)
    print ("Minimaleprijs de komende uren: ", minimaleprijs)
    print ("Maximaleprijs de komende uren: ", maximaleprijs)
    lading = ((maximaleprijs-huidigeprijs)/(maximaleprijs-minimaleprijs))*maximalelading
    print (lading)
    return lading

def instellingen():
    Maximalelading = 90
    cutoffduurstewaarden = 3
    return Maximalelading, cutoffduurstewaarden

def Lading(lading):
    print ("de auto zal geladen worden tot %d procent",lading)
    return 0

def prijsdelen(prijs):
    f = open("website/prijs.txt", "w")
    f.write(str(prijs))
    f.close()

def main():
    try:
        Gegevens, easyenergy = Ophalen()
    except:
        print ("er is iets mis gegaan bij het ophalen van gegevens bij Easyenergy, daarom wordt er nu informatie opgehaald bij entsoe.eu")
        Gegevens, easyenergy = Ophalen_entsoe()
    Huidige, Min, Max = belangrijkewaarden(Gegevens, easyenergy)
    prijsdelen(Huidige)
    Lading = TeslaBerekening(float(Huidige), float(Min), float(Max))
    Teslaladen(int(Lading))

main()
