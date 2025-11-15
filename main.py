## Imports
import keyboard
import time
import json
import pygame
import random
import sys
import gif_pygame

from matplotlib.pyplot import eventplot

## Climate Data Variables
## Commented lines are optional and can be included if data is available and when the programm is more advanced.    

# rcp = None                  # representative concentration pathway                  Link:
ggc = 417                # Treibhausgaskonzentration (ppm CO2-Äquivalent)        Link:
globalTemp = 1.6          # globale Temperatur (°C)                               Link: https://climate.nasa.gov/vital-signs/global-temperature/  & Link: https://de.statista.com/statistik/daten/studie/1073559/umfrage/durchschnittliche-temperaturschwankungen-land-meer/#:~:text=Die%20Temperaturen%20des%20Jahres%201850%20lagen%20durchschnittlich%20rund,weltweit%20das%20w%C3%A4rmste%20Jahr%20seit%20Beginn%20der%20Aufzeichnungen.  & Link: https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature
# snowCover = None            # Eisfläche (km²)                                       Link: 
# avgPrec = None              # Niederschlag (mm/Jahr)                                Link: 
# gsStrenght = None           # Golfstromstärke (Sv)                                  Link:
# climInv = None             # Klimainvestitionen (Mrd. USD/Jahr)                    Link:
# glacMelt = None             # Gletscherschmelze (t)                                 Link: 
seaLevel = 0.1           # Meeresspiegel (m)                                     Link: https://www.umweltbundesamt.de/monitoring-zur-das/handlungsfelder/kuesten-meeresschutz/km-i-2/indikator
# oceanHeat = None          # Ozeanwärmegehalt  (Joule)                             Link:
# forestLoss = None         # Waldverlust   (km²/Jahr)                              Link:
# forestArea = None           # Waldfläche (km²)                                      Link: https://www.fao.org/3/i4793e/i4793e.pdf
# winterLength = None         # Winterlänge (Tage)                                    Link:              
# permafrostDepth = None      # Permafrost-Tiefe (m)                                  Link:     
# energyMix = None            # Energie-Mix (% Erneuerbare Energien)                  Link:
deaths = 0                # Todesfälle durch Klimakatastrophen
MAX_GGC = 40000      # ppm
MAX_TEMP = 5      # °C
MAX_SEALEVEL = 1   # m
MAX_DEATHS = 2000000000
events = []
with open('events.JSON', 'r') as file:
    data = json.load(file)
example_gif = gif_pygame.load("kaboom.gif")

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
    change1=0
    change2=0
    change3=0
    change4=0

    def effects(self, change1, change2, change3, change4, eventText, globalTemp, ggc, seaLevel, deaths):
        globalTemp += change1
        ggc += change2
        seaLevel += change3
        print("Before deaths:", deaths)
        deaths += change4 ## höherer Faktor bei stärkeren Event
        print("deaths", deaths)
        print("change 4", change4)
        print("\n\n")
        print(eventText)
        print("\n")
        if self.name == "Saeureregen":
                events.append("Säureregen tritt auf! Wasser und Sauerstoff in der Atmosphäre verbinden sich vermehrt mit Schwefeloxiden und Stickoxiden und fallen als Regen nieder. Diese Art an Regen stört die Ausgeglichenheit der Naturböden und tötet dadurch Pflanzen.")
        elif self.name == "Gletcherschmelzung":
                events.append("Gletscher schmelzen so stark ab wie noch nie! Die globale Erderwärmung bringt immer mehr GLetscher zum kompletten Abschmelzen. Nicht nur der Meeresspiegel steigt durch diese Schmelzen, die Gletscher gehen auch als natürliche Süßwasserreserven und Feuchteausgleich in ihren Regionen verloren.")
        elif self.name == "Waldbrand":
                events.append("Starke Waldbrände breiten sich aus!")
        elif self.name == "Ueberschwemmung":
                events.append("Überflutungen bedrohen vermehrt Menschenleben!")
        elif self.name == "Duerre":
                events.append("Extreme Dürren sorgen für Notzustände in der ganzen Welt!")
        elif self.name == "Permafrostbodenaufsprengungen":
                events.append("Ursprünglich im Permafrost gespeicherte Klimagase treten in großen Mengen aus!")
        # time.sleep(2)
        return deaths
        

    def normalise(self, min, max, value):
        return (value - min) / (max - min)

    def calculatePropability(self, weighting1, weighting2, weighting3):
        return (weighting1 * self.normalise(0, 5, globalTemp) + weighting2 * self.normalise(250, 40000, ggc) + weighting3 * seaLevel / (weighting1 + weighting2 + weighting3))

    def propabilityCheck(self, propability, effects=effects, change1=change1, change2=change2, change3=change3, change4=change4, eventText=eventText):
        randNum = random.random()
        if(randNum <= propability):
            self.effects(self.change1, self.change2, self.change3, self.change4, self.eventText, globalTemp, ggc, seaLevel, deaths)
            
            print("deaths in gui loop:", deaths)
            
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
    def initialise(self):
        for i in range(len(listOfEvents)):
            listOfEvents[i].name = data[i]["name"]
            listOfEvents[i].eventText = data[i]["descr"]
            listOfEvents[i].change1 = data[i]["change"]["globalTemp"]
            listOfEvents[i].change2 = data[i]["change"]["seaLevel"]
            listOfEvents[i].change3 = data[i]["change"]["ggc"]
            listOfEvents[i].change4 = data[i]["change"]["deaths"]
            listOfEvents[i].weighting1 = data[i]["parameterWeighting"]["globalTemp"]
            listOfEvents[i].weighting2 = data[i]["parameterWeighting"]["ggc"]
            listOfEvents[i].weighting3 = data[i]["parameterWeighting"]["seaLevel"]
            # add weighting parameters
            listOfEvents[i].propability = listOfEvents[i].calculatePropability(listOfEvents[i].weighting1, listOfEvents[i].weighting2, listOfEvents[i].weighting3)
        # acidRain = listOfEvents[0]
        # icebergMelt = listOfEvents[1]
        # bushFire = listOfEvents[2]
        # flooding = listOfEvents[3]
        # drought = listOfEvents[4]
        # permFrostBurst = listOfEvents[5]   
    def checkPropabilities(self):
        for i in range(len(listOfEvents)):
            listOfEvents[i].propabilityCheck(listOfEvents[i].propability)

simulation = Simulation()
simulation.initialise()    
            
# ## Main Program

# print("CLIMATE++\n \n \n Wählen Sie eine Option aus indem sie die zugehörige Nummer eingeben: \n 1. Simulation starten\n 2. Programm verlassen")
# user_input = input()
# if(user_input == "1"):
#     print("Starte Simulation...")
#     print("\n\nWählen Sie Ihre Startparameter:\n")
#     print("Geben sie die Anfangs-Treibhausgaskonzentration (in ppm CO2-Äquivalent): ")
#     ggc = float(input())
#     print("Geben sie die Anfangs-globale Temperatur (in °C): ")
#     globalTemp = float(input())
#     print("Geben sie den Anfangs-Meeresspiegel (in m ueber Normal Null): ")
#     seaLevel = float(input())
#     print("\n\nSimulation hat mit den folgenden Parameterm gestartet: \n Treibhausgaskonzentration: " + str(ggc) + " ppm CO2-Äquivalent \n globale Temperatur: " + str(globalTemp) + " °C \n Wasserpegel: " + str(seaLevel) + " m ueber Normal Null")
#     simulation = Simulation()
#     simulation.initialise()
#     print("\n\n--- SIMULATION LAEUFT ---\n\n")
#     print("Um das Programm zu verlassen, drücken sie Escape. Einige der folgenden Ereignisse werden von ihnen verlangen mit dem Programm zu interagieren.")
#     i = 0
#     while not keyboard.is_pressed('esc'):
#         # Hier ist unser kompletter Simulationscode
#         simulation.checkPropabilities()
#         # Funktion die Ereignisse und Parameter abfragt und damit möglicherweise Ereignisse auslöst
#         i+=1
#         print("\n\n")
#         print("In dieser Iteration (Nr. "+str(i)+") ist nichts weiteres passiert.") 
#         print("\n")
#         input("Drücken sie Enter um fortzufahren")
        
#         time.sleep(0.1)
#         pass
#     print("Simulation beendet.")
# elif(user_input == "2"):
#     print("Verlasse Programm...")
# --- Hilfsfunktion für Farben ---
def berechne_farbe(x, min_val, max_val):
    if x < 1/3*max_val:
        return (0, 255, 0)   # Grün
    elif 1/3*max_val <= x < 2/3*max_val:
        return (255, 220, 0) # Gelb
    elif 2/3*max_val <= x:
        return (255, 0, 0)   # Rot
    return (0, 0, 0)

# --- Simulation Schritt ---
def simulation_step(ggc, globalTemp, seaLevel,deaths):
    simulation.checkPropabilities()
    events.append("In dieser Iteration ist nichts weiteres passiert.")
    time.sleep(1)
    return ggc, globalTemp, seaLevel, events, deaths

# --- GUI starten ---
def starten_gui():
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Climate++ Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    global ggc, globalTemp, seaLevel , deaths
    running = True
    events_log = []
    weltuntergang = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulation aktualisieren
        if not weltuntergang:
            ggc, globalTemp, seaLevel, events, deaths = simulation_step(ggc, globalTemp, seaLevel, deaths)
            # Neue Ereignisse ins Log aufnehmen
            for e in events:
                events_log.append(e)
                if len(events_log) > 10:  # nur die letzten 10 anzeigen
                    events_log.pop(0)
            # Prüfen ob Maximalwerte überschritten
            if ggc > MAX_GGC or globalTemp > MAX_TEMP or seaLevel > MAX_SEALEVEL or deaths > MAX_DEATHS:
                weltuntergang = True
                events_log.append("!!! WELTUNTERGANG !!!")
                if len(events_log) > 10:
                    events_log.pop(0)
            # Bildschirm weiß füllen
        screen.fill((255, 255, 255))

            # Texte rendern

            

        text1 = font.render(f"Treibhausgase: {ggc:.2f} ppm", True, (berechne_farbe(ggc, 250, 40000)))
        text2 = font.render(f"Temperatur: {globalTemp:.2f} °C", True, (berechne_farbe(globalTemp, 0, 5)))
        text3 = font.render(f"Meeresspiegel: {seaLevel:.2f} m", True,(berechne_farbe(seaLevel, 0, 1)))
        text4 = font.render(f"Todesfälle: {deaths}", True, (0, 0, 0))
        text5 = font.render("Simulation läuft... (Fenster schließen zum Beenden)", True, (0, 0, 0))

        if weltuntergang:
            text5 = font.render("Simulation gestoppt: WELTUNTERGANG!", True, (255, 0, 0))
            example_gif.render(screen, (128 - example_gif.get_width() * 0.5, 256 - example_gif.get_height() * 0.5))
            example_gif.speed = 3  # Set the speed of the gif
        else:
            text5 = font.render("Simulation läuft... (Fenster schließen zum Beenden)", True, (0, 0, 0))


        # Texte anzeigen
        screen.blit(text1, (50, 50))
        screen.blit(text2, (50, 100))
        screen.blit(text3, (50, 150))
        screen.blit(text4, (50, 200))
        screen.blit(text5, (50, 250))

            # Ereignisse anzeigen
        y_offset = 300
        for e in events_log:
            event_text = font.render(f"- {e}", True, (200, 0, 0))
            screen.blit(event_text, (50, y_offset))
            y_offset += 35

        pygame.display.flip()
        clock.tick(1)  # 2 Updates pro Sekunde

    pygame.quit()

if __name__ == "__main__":
    starten_gui()