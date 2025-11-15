## Imports
import keyboard
import time
import json

from matplotlib.pyplot import eventplot

## Climate Data Variables
## Commented lines are optional and can be included if data is available and when the programm is more advanced.    

# rcp = None                  # representative concentration pathway                  Link:
ggc = None                  # Treibhausgaskonzentration (ppm CO2-Äquivalent)        Link:
globalTemp = None           # globale Temperatur (°C)                               Link: https://climate.nasa.gov/vital-signs/global-temperature/  & Link: https://de.statista.com/statistik/daten/studie/1073559/umfrage/durchschnittliche-temperaturschwankungen-land-meer/#:~:text=Die%20Temperaturen%20des%20Jahres%201850%20lagen%20durchschnittlich%20rund,weltweit%20das%20w%C3%A4rmste%20Jahr%20seit%20Beginn%20der%20Aufzeichnungen.  & Link: https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature
# snowCover = None            # Eisfläche (km²)                                       Link: 
# avgPrec = None              # Niederschlag (mm/Jahr)                                Link: 
# gsStrenght = None           # Golfstromstärke (Sv)                                  Link:
# climInv = None             # Klimainvestitionen (Mrd. USD/Jahr)                    Link:
# glacMelt = None             # Gletscherschmelze (t)                                 Link: 
seaLevel = None             # Meeresspiegel (m)                                     Link: https://www.umweltbundesamt.de/monitoring-zur-das/handlungsfelder/kuesten-meeresschutz/km-i-2/indikator
# oceanHeat = None          # Ozeanwärmegehalt  (Joule)                             Link:
# forestLoss = None         # Waldverlust   (km²/Jahr)                              Link:
# forestArea = None           # Waldfläche (km²)                                      Link: https://www.fao.org/3/i4793e/i4793e.pdf
# winterLength = None         # Winterlänge (Tage)                                    Link:              
# permafrostDepth = None      # Permafrost-Tiefe (m)                                  Link:     
# energyMix = None            # Energie-Mix (% Erneuerbare Energien)                  Link:
deaths = None                 # Todesfälle durch Klimakatastrophen
with open('events.JSON', 'r') as file:
    data = json.loads(file)

## Classes

class climateEvent:
    name=None
    # indexNumber=None
    eventText=None
    changingParameter1=None
    changingParameter2=None
    changingParameter3=None
    weighting1=None
    weighting2=None
    weighting3=None
    propability=None
    change1=None
    change2=None
    change3=None

    def effects(change1, change2, change3, kills, eventText):
        changingParameter1 += change1
        changingParameter2 += change2
        changingParameter3 += change3
        deaths += kills
        print(eventText)

    def normalise(min, max, value):
        return (value - min) / (max - min)

    def calculatePropability(weighting1, weighting2, weighting3):
        return (weighting1 * climateEvent.normalise(0, 5, globalTemp) + weighting2 * climateEvent.normalise(250, 40000, ggc) + weighting3 * seaLevel / (weighting1 + weighting2 + weighting3)) / (weighting1 + weighting2 + weighting3)

    def propabilityCheck(propability, effects=effects, change1=change1, change2=change2, change3=change3, eventText=eventText):
        import random
        randNum = random.random()
        if(randNum <= propability):
            effects(change1, change2, change3, eventText)
            return True
        else:
            return False
        
acidRain = climateEvent()
icebergMelt = climateEvent()
bushFire = climateEvent()
flooding = climateEvent()
drought = climateEvent()
permFrostBurst = climateEvent()
listOfEvents = [acidRain, icebergMelt, bushFire, flooding, drought, permFrostBurst]  # Durch diese Liste wird später durchiteriert um die Ereignisse zu definieren

class Simulation:
    def initialise():
        for i in range(len(listOfEvents)):
            listOfEvents[i].name = data[str(i)]["name"]
            listOfEvents[i].eventText = data[str(i)]["descr"]
            # add weighting parameters
            listOfEvents[i].calculatePropability()
        acidRain = listOfEvents[0]
        icebergMelt = listOfEvents[1]
        bushFire = listOfEvents[2]
        flooding = listOfEvents[3]
        drought = listOfEvents[4]
        permFrostBurst = listOfEvents[5]   
    def checkPropabilities():
        for i in range(len(listOfEvents)):
            listOfEvents[i].propabilityCheck(listOfEvents[i].propability)    
            
## Main Program

print("CLIMATE++\n \n \n Wählen Sie eine Option aus indem sie die zugehörige Nummer eingeben: \n 1. Simulation starten\n 2. Programm verlassen")
user_input = input()
if(user_input == "1"):
    print("Starte Simulation...")
    print("\n\nWählen Sie Ihre Startparameter:\n")
    print("Geben sie die Anfangs-Treibhausgaskonzentration (in ppm CO2-Äquivalent): ")
    ggc = float(input())
    print("Geben sie die Anfangs-globale Temperatur (in °C): ")
    globalTemp = float(input())
    print("Geben sie den Anfangs-Meeresspiegel (in m ueber Normal Null): ")
    seaLevel = float(input())
    print("\n\nSimulation hat mit den folgenden Parameterm gestartet: \n Treibhausgaskonzentration: " + str(ggc) + " ppm CO2-Äquivalent \n globale Temperatur: " + str(globalTemp) + " °C \n Wasserpegel: " + str(seaLevel) + " m ueber Normal Null")
    Simulation.initialise()
    print("\n\n--- SIMULATION LAEUFT ---\n\n")
    print("Um das Programm zu verlassen, drücken sie Escape. Einige der folgenden Ereignisse werden von ihnen verlangen mit dem Programm zu interagieren.")
    while not keyboard.is_pressed('esc'):
        # Hier ist unser kompletter Simulationscode

        # Funktion die Ereignisse und Parameter abfragt und damit möglicherweise Ereignisse auslöst
        
        print("In dieser Iteration ist noch nichts passiert.") 
        time.sleep(0.1)
        pass
    print("Simulation beendet.")
elif(user_input == "2"):
    print("Verlasse Programm...")