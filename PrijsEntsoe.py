import datetime as dt
import requests
from bs4 import BeautifulSoup


#######################################################
###Input: none
###Function: Get the day ahead prices form entsoe, and transform them to price per kWh including taxation. (*0.00121)
###Output: List of upcoming prices so far as possible. in the format: list[time, price buy, price sell]
#######################################################

def Ophalen():
    nu = dt.datetime.now(dt.timezone.utc)
    morgen = nu + dt.timedelta(days=1)
    urlvandaag = "https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime="+"{:02d}".format(nu.day)+"."+"{:02d}".format(nu.month)+"."+str(nu.year)+"+00:00|UTC|DAY&biddingZone.values=CTY|10YNL----------L!BZN|10YNL----------L&dateTime.timezone=UTC&dateTime.timezone_input=UTC"
    urlmorgen = "https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime="+"{:02d}".format(morgen.day)+"."+"{:02d}".format(morgen.month)+"."+str(morgen.year)+"+00:00|UTC|DAY&biddingZone.values=CTY|10YNL----------L!BZN|10YNL----------L&dateTime.timezone=UTC&dateTime.timezone_input=UTC"
    #print (urlvandaag)
    #print (urlmorgen)
    pagevandaag = requests.get(urlvandaag)
    pagemorgen = requests.get(urlmorgen)
    soupv = BeautifulSoup(pagevandaag.text, 'html.parser')
    soupm = BeautifulSoup(pagemorgen.text, 'html.parser')
    price_hidev = soupv.find_all(class_='dv-value-cell')
    price_hidem = soupm.find_all(class_='dv-value-cell')
    returnvalues = []
    for price in price_hidev:
        try:
            noISOdatum = str(price).split("\', \'")[2]
            datum = dt.datetime.fromisoformat(noISOdatum[:-1])
            if ((datum.timestamp() - nu.timestamp()) >= -7200):
                #print (price.text)
                returnvalues.append([datum, str(float(price.text)*0.00121), str(float(price.text)*0.00121)])
        except:
            pass
    try:
        for price in price_hidem:
            try:
                noISOdatum = str(price).split("\', \'")[2]
                datum = dt.datetime.fromisoformat(noISOdatum[:-1])
                if ((datum.timestamp() - nu.timestamp()) >= -7200):
                    #print (price.text)
                    returnvalues.append([datum, str(float(price.text)*0.00121), str(float(price.text)*0.00121)])
            except:
                pass
    except:
        pass
    return returnvalues
