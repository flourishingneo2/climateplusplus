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

    def get_random_value(self, change_value):
        """Get a random value from array range or return 0 if value is 0"""
        if isinstance(change_value, list):
            # If it's an array, return random value between min and max
            return random.uniform(change_value[0], change_value[1])
        elif change_value == 0:
            # If it's 0, return 0 (no change)
            return 0
        else:
            # If it's a single value, return it as is
            return change_value

    def effects(self, change1, change2, change3, change4, eventText):
        global globalTemp, ggc, seaLevel, deaths, events
        
        # Get random values for each parameter
        actual_change1 = self.get_random_value(change1)
        actual_change2 = self.get_random_value(change2)
        actual_change3 = self.get_random_value(change3)
        actual_change4 = self.get_random_value(change4)
        
        # Apply changes
        globalTemp += actual_change1
        ggc += actual_change2
        seaLevel += actual_change3
        deaths += int(actual_change4)
        
        print("\n\n")
        print(eventText)
        print(f"  ΔTemp: {actual_change1:.3f}°C, ΔGGC: {actual_change2:.2f} ppm, ΔSea: {actual_change3:.4f} m, ΔDeaths: {int(actual_change4)}")
        print("\n")
        
        if self.name == "Saeureregen":
            events.append("Säureregen tritt auf! Wasser und Sauerstoff in der Atmosphäre verbinden sich vermehrt mit Schwefeloxiden und Stickoxiden und fallen als Regen nieder.")
        elif self.name == "Gletscherschmelzung":
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
            return True
        else:
            return False
    
    def trigger(self):
        self.effects(self.change1, self.change2, self.change3, self.change4, self.eventText)

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
        triggered_events = []
        
        for i in range(len(listOfEvents)):
            while True:
                # Recalculate probability based on current conditions
                listOfEvents[i].propability = listOfEvents[i].calculatePropability(
                listOfEvents[i].weighting1,
                listOfEvents[i].weighting2,
                listOfEvents[i].weighting3
                )
                if listOfEvents[i].propabilityCheck(listOfEvents[i].propability):
                    triggered_events.append(listOfEvents[i])
                else:
                    break
        
        # Only trigger each event once
        for event in triggered_events:
            event.trigger()

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

def draw_gradient_rect(surface, color1, color2, rect):
    """Draw a vertical gradient rectangle"""
    for y in range(rect.height):
        blend = y / rect.height
        r = int(color1[0] * (1 - blend) + color2[0] * blend)
        g = int(color1[1] * (1 - blend) + color2[1] * blend)
        b = int(color1[2] * (1 - blend) + color2[2] * blend)
        pygame.draw.line(surface, (r, g, b), 
                        (rect.x, rect.y + y), 
                        (rect.x + rect.width, rect.y + y))

def draw_rounded_rect(surface, color, rect, radius=15):
    """Draw a rounded rectangle"""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

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
    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("Climate++ Simulation")
    clock = pygame.time.Clock()
    
    # Fonts
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)
    
    running = True
    events_log = []  # List of tuples: (event_text, is_recent)
    weltuntergang = False
    recent_event_count = 0  # Track how many recent events we have

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Enter-Taste für nächsten Schritt
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not weltuntergang:
                    # Simulation aktualisieren
                    simulation_step()
                    
                    # Mark all existing events as old
                    events_log = [(text, False) for text, _ in events_log]
                    recent_event_count = 0
                    
                    # Neue Ereignisse ins Log aufnehmen (marked as recent)
                    for e in events:
                        events_log.insert(0, (e, True))  # Am Anfang einfügen mit recent=True
                        recent_event_count += 1
                        if len(events_log) > 15:  # mehr Platz für Events
                            events_log.pop()  # Letztes Element entfernen
                    
                    # Prüfen ob Maximalwerte überschritten
                    if ggc > MAX_GGC or globalTemp > MAX_TEMP or seaLevel > MAX_SEALEVEL or deaths > MAX_DEATHS:
                        weltuntergang = True
                        events_log.insert(0, ("!!! WELTUNTERGANG !!!", True))  # Am Anfang einfügen
                        recent_event_count += 1
                        if len(events_log) > 15:
                            events_log.pop()  # Letztes Element entfernen
        
        # Hintergrund mit Gradient
        draw_gradient_rect(screen, (15, 20, 35), (25, 35, 55), pygame.Rect(0, 0, 1200, 700))
        
        # Title
        title = font_large.render("CLIMATE++ SIMULATION", True, (255, 255, 255))
        title_shadow = font_large.render("CLIMATE++ SIMULATION", True, (0, 0, 0))
        screen.blit(title_shadow, (52, 22))
        screen.blit(title, (50, 20))
        
        # Stats Panel
        panel_rect = pygame.Rect(30, 90, 550, 280)
        draw_rounded_rect(screen, (35, 45, 65), panel_rect)
        pygame.draw.rect(screen, (80, 90, 110), panel_rect, 3, border_radius=15)
        
        # Stats Title
        stats_title = font_medium.render("Klimadaten", True, (200, 200, 200))
        screen.blit(stats_title, (50, 100))
        
        # Individual stat boxes
        y_pos = 150
        
        # Treibhausgase
        ggc_color = berechne_farbe(ggc, 250, 40000)
        ggc_box = pygame.Rect(50, y_pos, 500, 30)
        draw_rounded_rect(screen, (25, 30, 45), ggc_box, 8)
        text1 = font_small.render(f"🌫️  Treibhausgase: {ggc:.2f} ppm", True, ggc_color)
        screen.blit(text1, (60, y_pos + 3))
        
        # Temperatur
        y_pos += 40
        temp_color = berechne_farbe(globalTemp, 0, 5)
        temp_box = pygame.Rect(50, y_pos, 500, 30)
        draw_rounded_rect(screen, (25, 30, 45), temp_box, 8)
        text2 = font_small.render(f"🌡️  Temperatur: {globalTemp:.2f} °C", True, temp_color)
        screen.blit(text2, (60, y_pos + 3))
        
        # Meeresspiegel
        y_pos += 40
        sea_color = berechne_farbe(seaLevel, 0, 1)
        sea_box = pygame.Rect(50, y_pos, 500, 30)
        draw_rounded_rect(screen, (25, 30, 45), sea_box, 8)
        text3 = font_small.render(f"🌊  Meeresspiegel: {seaLevel:.2f} m", True, sea_color)
        screen.blit(text3, (60, y_pos + 3))
        
        # Todesfälle
        y_pos += 40
        deaths_box = pygame.Rect(50, y_pos, 500, 30)
        draw_rounded_rect(screen, (25, 30, 45), deaths_box, 8)
        text4 = font_small.render(f"💀  Todesfälle: {deaths:,}", True, (255, 100, 100))
        screen.blit(text4, (60, y_pos + 3))
        
        # Events Panel
        events_panel_rect = pygame.Rect(30, 390, 1140, 280)
        draw_rounded_rect(screen, (35, 45, 65), events_panel_rect)
        pygame.draw.rect(screen, (80, 90, 110), events_panel_rect, 3, border_radius=15)
        
        # Events Title
        events_title = font_medium.render("Ereignisse", True, (200, 200, 200))
        screen.blit(events_title, (50, 400))
        
        # Ereignisse anzeigen
        y_offset = 450
        for i, (e, is_recent) in enumerate(events_log):
            if is_recent:
                # Recent events in bright cyan/yellow
                event_color = (255, 220, 80)
                prefix = "▶ "
            else:
                # Old events in darker gray
                event_color = (150, 150, 150)
                prefix = "  "
            
            event_text = font_small.render(f"{prefix}{e}", True, event_color)
            screen.blit(event_text, (60, y_offset))
            y_offset += 32
            
            if y_offset > 640:  # Don't overflow the panel
                break
        
        # Instructions/Status
        if weltuntergang:
            status_box = pygame.Rect(620, 90, 550, 280)
            draw_rounded_rect(screen, (80, 20, 20), status_box)
            pygame.draw.rect(screen, (200, 50, 50), status_box, 3, border_radius=15)
            
            text5 = font_medium.render("🔥 WELTUNTERGANG! 🔥", True, (255, 200, 200))
            screen.blit(text5, (700, 180))
            
            try:
                example_gif.render(screen, (800 - example_gif.get_width() * 0.5, 100))
                example_gif.speed = 3
            except:
                pass
        else:
            status_box = pygame.Rect(620, 90, 550, 280)
            draw_rounded_rect(screen, (35, 45, 65), status_box)
            pygame.draw.rect(screen, (80, 90, 110), status_box, 3, border_radius=15)
            
            text5 = font_medium.render("⏸️  Bereit für nächsten Schritt", True, (150, 255, 150))
            text6 = font_small.render("Drücke ENTER ⏎", True, (200, 200, 200))
            screen.blit(text5, (640, 170))
            screen.blit(text6, (750, 220))

        pygame.display.flip()
        clock.tick(60)  # 60 FPS für responsive GUI

    pygame.quit()

if __name__ == "__main__":
    starten_gui()