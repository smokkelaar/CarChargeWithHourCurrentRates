import Tesla.teslapy as teslapy

CLIENT_ID='81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
CLIENT_SECRET='c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
GEBRUIKERSNAAM = "mailadres@mail.com"
WACHTWOORD = "wachtwoord"

#######################################################
###Input: procent of charge
###Function: Set charging of the Tesla, provide extra information of the car
###Output: None.
#######################################################


def Teslaladen(procent):
    with teslapy.Tesla(GEBRUIKERSNAAM, WACHTWOORD, CLIENT_ID, CLIENT_SECRET) as tesla:
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