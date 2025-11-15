import pygame
import random
import sys
import gif_pygame


# --- Climate Data Variables ---
ggc = 417.0        # Treibhausgaskonzentration (ppm CO2-Äquivalent)
globalTemp = 0.0  # globale Temperatur (°C)
seaLevel = 0.0     # Meeresspiegel (m)
deads = 0
#gif
example_gif = gif_pygame.load("kaboom.gif") # Load a .gif file


# --- Maximalwerte ---
MAX_GGC = 40000      # ppm
MAX_TEMP = 5      # °C
MAX_SEALEVEL = 1   # m
MAX_DEATHS = 2000000000  # 2 Milliarde

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
def simulation_step(ggc, globalTemp, seaLevel,deads):
    # Werte ändern sich leicht zufällig
    ggc += random.uniform(-0.2, 0.5)
    globalTemp += random.uniform(-0.05, 0.15)
    seaLevel += random.uniform(-0.01, 0.02)
    events = []

    # --- Ereignisse abhängig von Parametern ---
    if ggc > 500 and random.random() < 0.3:
        events.append()
    if globalTemp > 1.6 and random.random() < 0.4:
        events.append("Gletscher schmelzen so stark ab wie noch nie! Die globale Erderwärmung bringt immer mehr GLetscher zum kompletten Abschmelzen. Nicht nur der Meeresspiegel steigt durch diese Schmelzen, die Gletscher gehen auch als natürliche Süßwasserreserven und Feuchteausgleich in ihren Regionen verloren.")
    if globalTemp > 4 and random.random() < 0.5:
        events.append("Waldbrand durch extreme Hitze!")
        deads += random.randint(10000, 500000)
    if seaLevel > 0.5 and random.random() < 0.4:
        events.append("Überflutung von Küstenregionen!")
        deads += random.randint(5000, 10000)
    if globalTemp > 3.5 and random.random() < 0.3:
        events.append("Dürre durch langanhaltende Hitze!")
        deads += random.randint(1000, 1000000)
    if globalTemp > 2.25 and random.random() < 0.2:
        events.append("Permafrost taut auf")
    

    return ggc, globalTemp, seaLevel, events, deads

# --- GUI starten ---
def starten_gui():
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Climate++ Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    global ggc, globalTemp, seaLevel , deads
    running = True
    events_log = []
    weltuntergang = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulation aktualisieren
        if not weltuntergang:
            ggc, globalTemp, seaLevel, events, deads = simulation_step(ggc, globalTemp, seaLevel, deads)

            # Neue Ereignisse ins Log aufnehmen
            for e in events:
                events_log.append(e)
                if len(events_log) > 10:  # nur die letzten 10 anzeigen
                    events_log.pop(0)
            # Prüfen ob Maximalwerte überschritten
            if ggc > MAX_GGC or globalTemp > MAX_TEMP or seaLevel > MAX_SEALEVEL or deads > MAX_DEATHS:
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
        text4 = font.render(f"Todesfälle: {deads}", True, (0, 0, 0))
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
        clock.tick(2)  # 2 Updates pro Sekunde

    pygame.quit()

# --- Start ---
if __name__ == "__main__":
    starten_gui()