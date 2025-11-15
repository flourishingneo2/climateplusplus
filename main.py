## Imports
import time
import json
import pygame
import random
import sys
import gif_pygame

## Climate Data Variables
ggc = 417                # Treibhausgaskonzentration (ppm CO2-Äquivalent)
globalTemp = 1.6         # globale Temperatur (°C)
seaLevel = 0.1           # Meeresspiegel (m)
deaths = 0               # Todesfälle durch Klimakatastrophen
MAX_GGC = 40000          # ppm
MAX_TEMP = 5             # °C
MAX_SEALEVEL = 1         # m
MAX_DEATHS = 2000000000
events = []

# Load event data
with open('events.JSON', 'r') as file:
    data = json.load(file)

# Load gif
example_gif = gif_pygame.load("kaboom.gif")

## Classes

class climateEvent:
    def __init__(self):
        self.name = None
        self.eventText = None
        self.changingParameter1 = None
        self.changingParameter2 = None
        self.changingParameter3 = None
        self.weighting1 = None
        self.weighting2 = None
        self.weighting3 = None
        self.propability = None
        self.change1 = 0
        self.change2 = 0
        self.change3 = 0
        self.change4 = 0

    def effects(self, change1, change2, change3, change4, eventText):
        global globalTemp, ggc, seaLevel, deaths, events
        
        globalTemp += change1
        ggc += change2
        seaLevel += change3
        deaths += change4
        
        print("\n\n")
        print(eventText)
        print("\n")
        
        if self.name == "Saeureregen":
            events.append("Säureregen tritt auf! Wasser und Sauerstoff in der Atmosphäre verbinden sich vermehrt mit Schwefeloxiden und Stickoxiden und fallen als Regen nieder.")
        elif self.name == "Gletcherschmelzung":
            events.append("Gletscher schmelzen so stark ab wie noch nie! Die globale Erderwärmung bringt immer mehr Gletscher zum kompletten Abschmelzen.")
        elif self.name == "Waldbrand":
            events.append("Starke Waldbrände breiten sich aus!")
        elif self.name == "Ueberschwemmung":
            events.append("Überflutungen bedrohen vermehrt Menschenleben!")
        elif self.name == "Duerre":
            events.append("Extreme Dürren sorgen für Notzustände in der ganzen Welt!")
        elif self.name == "Permafrostbodenaufsprengungen":
            events.append("Ursprünglich im Permafrost gespeicherte Klimagase treten in großen Mengen aus!")

    def normalise(self, min_val, max_val, value):
        if max_val == min_val:
            return 0
        return (value - min_val) / (max_val - min_val)

    def calculatePropability(self, weighting1, weighting2, weighting3):
        global globalTemp, ggc, seaLevel
        
        norm_temp = self.normalise(0, 5, globalTemp)
        norm_ggc = self.normalise(250, 40000, ggc)
        norm_sea = self.normalise(0, 1, seaLevel)
        
        total_weight = weighting1 + weighting2 + weighting3
        if total_weight == 0:
            return 0
            
        return (weighting1 * norm_temp + weighting2 * norm_ggc + weighting3 * norm_sea) / total_weight

    def propabilityCheck(self, propability):
        randNum = random.random()
        if randNum <= propability:
            self.effects(self.change1, self.change2, self.change3, self.change4, self.eventText)
            return True
        else:
            return False

# Create event instances
acidRain = climateEvent()
icebergMelt = climateEvent()
bushFire = climateEvent()
flooding = climateEvent()
drought = climateEvent()
permFrostBurst = climateEvent()
listOfEvents = [acidRain, icebergMelt, bushFire, flooding, drought, permFrostBurst]

class Simulation:
    def initialise(self):
        for i in range(len(listOfEvents)):
            listOfEvents[i].name = data[i]["name"]
            listOfEvents[i].eventText = data[i]["descr"]
            listOfEvents[i].change1 = data[i]["change"]["globalTemp"]
            listOfEvents[i].change2 = data[i]["change"]["ggc"]
            listOfEvents[i].change3 = data[i]["change"]["seaLevel"]
            listOfEvents[i].change4 = data[i]["change"]["deaths"]
            listOfEvents[i].weighting1 = data[i]["parameterWeighting"]["globalTemp"]
            listOfEvents[i].weighting2 = data[i]["parameterWeighting"]["ggc"]
            listOfEvents[i].weighting3 = data[i]["parameterWeighting"]["seaLevel"]
            listOfEvents[i].propability = listOfEvents[i].calculatePropability(
                listOfEvents[i].weighting1, 
                listOfEvents[i].weighting2, 
                listOfEvents[i].weighting3
            )
    
    def checkPropabilities(self):
        for i in range(len(listOfEvents)):
            listOfEvents[i].propabilityCheck(listOfEvents[i].propability)

simulation = Simulation()
simulation.initialise()

# --- Hilfsfunktion für Farben ---
def berechne_farbe(x, min_val, max_val):
    if x < 1/3 * max_val:
        return (0, 255, 0)   # Grün
    elif 1/3 * max_val <= x < 2/3 * max_val:
        return (255, 220, 0) # Gelb
    elif 2/3 * max_val <= x:
        return (255, 0, 0)   # Rot
    return (0, 0, 0)

# --- Simulation Schritt ---
def simulation_step():
    global events
    events.clear()  # Clear events from previous iteration
    simulation.checkPropabilities()
    
    # Only add "nothing happened" if no events were added
    if len(events) == 0:
        events.append("In dieser Iteration ist nichts weiteres passiert.")

# --- GUI starten ---
def starten_gui():
    global ggc, globalTemp, seaLevel, deaths
    
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Climate++ Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    
    running = True
    events_log = []
    weltuntergang = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulation aktualisieren
        if not weltuntergang:
            simulation_step()
            
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
        text1 = font.render(f"Treibhausgase: {ggc:.2f} ppm", True, berechne_farbe(ggc, 250, 40000))
        text2 = font.render(f"Temperatur: {globalTemp:.2f} °C", True, berechne_farbe(globalTemp, 0, 5))
        text3 = font.render(f"Meeresspiegel: {seaLevel:.2f} m", True, berechne_farbe(seaLevel, 0, 1))
        text4 = font.render(f"Todesfälle: {deaths}", True, (0, 0, 0))

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
        clock.tick(1)  # 1 Update pro Sekunde

    pygame.quit()

if __name__ == "__main__":
    starten_gui()