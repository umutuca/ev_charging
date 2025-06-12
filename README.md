# EV Laddstation – Pythonklient

Detta är en terminalbaserad Python-applikation som kommunicerar med en simulerad laddstation via ett Flask-API. Projektet simulerar laddning av ett elbilsbatteri baserat på elpris och hushållets energiförbrukning under ett dygn.

## Funktioner

- ✅ Hämta aktuell status för laddstation, elpris och hushållsförbrukning
- 🔋 Visa aktuell batterinivå i procent
- ⚡ Starta och stoppa laddning manuellt
- 🔁 Automatisk laddning:
  - Endast vid låg hushållsförbrukning (< 11 kW)
  - Endast vid lägsta elpris under dygnet och förbrukning < 11 kW
  - Kombination av båda villkoren
- ♻️ Återställ batteriet till 20% via /discharge-endpoint
- 📊 Visa 24-timmars översikt av elpris och hushållsbelastning

## Användning

1. Starta Flask-servern (`charging_simulation.py`)
2. Kör denna klient (`client_terminal.py`)
3. Följ instruktionerna i menyn

### Exempel på menyval:

print("\n=== EV LADDSTATION – MENY ===")
print("1. Visa laddstationens status")
print("2. Visa aktuell hushållsförbrukning")
print("3. Starta laddning manuellt")
print("4. Stoppa laddning manuellt")
print("5. Visa batterinivå")
print("6. Automatisk laddning (både lågpris + låg last)")
print("7. Automatisk laddning (endast låg hushållsförbrukning)")
print("8. Automatisk laddning (endast lägsta elpris + förbrukning < 11kW)")
print("9. Visa elpris per timme (24h)")
print("10. Visa hushållets förbrukning (24h)")
print("11. Avsluta")
print("12. Återställ batteri till 20% (discharge)")
