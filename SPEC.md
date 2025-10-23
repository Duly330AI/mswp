# Projektspezifikation: Minesweeper (Pygame Edition)

**Version:** 3.0 (Final Release)

## 1. Projektübersicht & Ziele

Dieses Dokument beschreibt die Anforderungen und Implementierung einer eigenständigen Desktop-Anwendung des klassischen Spiels "Minesweeper" unter Verwendung von Python und der Pygame-Bibliothek. Ziel ist eine originalgetreue Nachbildung der Spielmechanik und des visuellen Stils von Windows 95 Minesweeper in einem dedizierten Spielfenster mit grafischer Benutzeroberfläche.

## 2. Funktionale Anforderungen

### 2.1 UI-Elemente
- **Startmenü:** Grafisches Menü zur Auswahl der Schwierigkeitsstufe (Beginner, Intermediate, Expert)
  - Gitter-Hintergrundbild mit Kontrastoptimierung
  - Text mit halbtransparentem weißem Hintergrund für Lesbarkeit
  - Farblich codierte Buttons (grün/orange/rot)
- **Fenster:** Ein Pygame-Fenster, dessen Größe sich an die Spielfeldgröße anpasst.
- **Header-Bereich:** Enthält:
  - Minenzähler (links, 3-stellig, rot)
  - Neustart-Smiley (mitte, gelb, mit Ausdrücken)
  - Timer (rechts, 3-stellig, rot)
  - 3D beveled Kanten (Windows 95 Stil)
- **Spielfeld:** Ein Gitter aus Zellen unterhalb des Headers mit:
  - Grauer Basis-Farbe für abgedeckte Zellen
  - Hellerer Farbe für aufgedeckte Zellen
  - Schwarze Gitternetzlinien

### 2.2 Schwierigkeitsgrade
- **Anfänger (Beginner):** 9x9 Gitter, 10 Minen.
- **Fortgeschritten (Intermediate):** 16x16 Gitter, 40 Minen.
- **Profi (Expert):** 30x16 Gitter, 99 Minen.

### 2.3 Gameplay-Logik
- **Schwierigkeitswahl:** Spieler wählt Schwierigkeit vom Startmenü aus.
- **Erster Klick:** Ist immer sicher. Minen werden erst nach dem ersten Klick platziert, außerhalb eines 3x3-Bereichs um den Klick herum.
- **Linksklick:** Deckt eine Zelle auf.
  - Offenlegung von Minenanzahl oder leer (wenn 0)
  - Flood-Fill bei leer (auto-reveal benachbarte Zellen)
- **Rechtsklick:** Setzt/entfernt eine rote Fahne als Markierung.
- **Smiley-Ausdruck:**
  - 😊 Normal während des Spiels (aufwärts gerichtete Linie)
  - 😞 Verlust (abwärts gerichtete Linie)
  - 😎 Gewinn (gerade Linie mit Sonnenbrille)
- **Spielende:** Das Spiel endet bei Gewinn (alle sicheren Felder aufgedeckt) oder Verlust (Mine aufgedeckt). Die Interaktion wird danach deaktiviert.

## 3. Technische Spezifikation

### 3.1 Architektur & Technologie
- **Sprache:** Python 3.7+
- **Hauptbibliotheken:**
  - `pygame`: Rendering, Event-Handling, Sound-Support
  - `pyinstaller`: Standalone EXE-Erstellung
- **Projekt-Struktur:**
    - `main.py`: Game-Loop, DifficultyMenu, Event-Handling, Rendering
    - `board.py`: Spielfeld-Logik (Mineplatzierung, Aufdecken, Flood-Fill)
    - `cell.py`: Zellenzustand (abgedeckt, aufgedeckt, Flagge, Mine)
    - `config.py`: Konstanten (Farben, Größen, Schwierigkeitsgrade)
    - `generate_background.py`: Hilfsskript zur Generierung von Hintergrunddatei

### 3.2 Build-, Test- und Ausführungsbefehle

#### Run: Variante 1 (Entwicklung)
```powershell
# Python-Umgebung aktivieren und Abhängigkeiten installieren
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Spiel starten (öffnet Menü zur Schwierigkeitswahl)
python main.py
```

#### Run: Variante 2 (Standalone EXE)
```powershell
# Minesweeper.exe direkt ausführen (keine Python-Installation erforderlich)
.\dist\Minesweeper.exe
```

#### Build: Standalone EXE
```powershell
# PyInstaller installieren
pip install pyinstaller

# EXE mit eingepackten Assets bauen
pyinstaller --onefile --windowed --add-data "images;images" --name=Minesweeper main.py

# Ergebnis: dist\Minesweeper.exe
```

#### Test
- Keine automatisierten Tests implementiert
- Modular architekturiert für einfache Unit-Tests
- Game-Logik separat vom Rendering für testbar

### 3.3 Ressourcen
- **images/background.png:** 400x400px Gittermuster-Hintergrundbild
  - Generiert von `generate_background.py`
  - Format: PNG
  - Muster: Horizontale/vertikale Streifen für visuellen Effekt

## 4. UI/UX Spezifikation

### 4.1 Farbschema (Windows 95 Stil)
- Header & Körper: Grau (192, 192, 192)
- Beveled Highlights: Weiß (255, 255, 255)
- Beveled Shadows: Dunkelgrau (128, 128, 128)
- Abgedeckte Zellen: Mittelgrau (180, 180, 180)
- Aufgedeckte Zellen: Hellgrau (220, 220, 220)
- Text: Schwarz (0, 0, 0)
- Mine-Zähler/Timer: Rot (255, 0, 0)
- Smiley: Gelb (255, 215, 0)
- Flag: Rot (200, 0, 0)

### 4.2 Menü-Design
- Größe: 400x400px
- Hintergrund: Gittermuster mit Gradient
- Buttons: 150x50px, Farben je nach Schwierigkeit
  - Beginner: Grün (0, 150, 0)
  - Intermediate: Orange/Gold (200, 150, 0)
  - Expert: Rot (200, 0, 0)
- Text-Boxen: Halbtransparent weiß (alpha=200) mit schwarzem Text

## 5. Bekannte Limitierungen
- Keine Netwerk-Multiplayer-Unterstützung
- Keine Sound-Effekte
- Keine Highscore-Speicherung
- Keine Custom-Schwierigkeitsstufen (nur vordefinierte)

## 6. Zukünftige Erweiterungen (nicht implementiert)
- Spielstatistiken und Highscore-Tabelle
- Sound-Effekte und Musik
- Dunkler Modus
- Custom-Schwierigkeitsstufen
- Netzwerk-Multiplayer