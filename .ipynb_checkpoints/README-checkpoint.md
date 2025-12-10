# Blender-Python Trainingsdatensynthese

## Shell Skript zum Headless Ausführen von Blender

```sh
"C:\Program Files\WindowsApps\BlenderFoundation.Blender_5.0.0.0_x64__ppwjx1n5r4v9t\Blender\blender.exe" -b playground.blend --python playground.py
-> Zugriff verweigert
```

Sollte auf ML laufen, Blender.exe sollte aber als Path Variable hinterlegt sein, damit man das einfach mit `blender ...` aufrufen kann.

## Training

![Deformable-DETR](https://github.com/fundamentalvision/Deformable-DETR)

ca. 100k Trainingsdaten, also 1000 Kistenstapel mit je 100 Bildern.

## Vorgehen generell

- Ausnutzen, dass das vollautomatisch läuft
- Wenn ein PoC einigermaßen vielversprechend ist, sollte man noch weiter versuchen das zu optimieren
- dazu könnte man ein Jupyter Notebook schreiben, dass die Terminal befehle fürs erstellen von Trainingsdaten ausführt
  - jedes mal mit unterschiedlichen Parametern wie:
    - Anzahl Trainingsdaten
    - Anzahl Kisten pro Stapel
    - Anzahl von Stapeln nebeneinander
    - Verhältnis Bilder pro Stapel
    - mit und ohne Hintergrund
    - mit und ohne Wagen


Hallo von ML2!