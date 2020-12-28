import prijsophalen as PO
import TeslaOpladen as TO
import BelangrijkeWaarden as BW
import Teslaberekening as TB

def prijsdelen(prijs):
    f = open("website/prijs.txt", "w")
    f.write(str(prijs))
    f.close()

def main():
    Gegevens = PO.prijsophalen()
    Huidige, Min, Max = BW.belangrijkewaarden(Gegevens)
    prijsdelen(Huidige)
    Lading = TB.TeslaBerekening(float(Huidige), float(Min), float(Max))
    TO.Teslaladen(int(Lading))

main()
