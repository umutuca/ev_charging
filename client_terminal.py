import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def get_info():
    print("🔵 GET /info")
    r = requests.get(f"{BASE_URL}/info")
    return r.json()

def get_price_per_hour():
    print("🔵 GET /priceperhour")
    r = requests.get(f"{BASE_URL}/priceperhour")
    return r.json()

def get_battery_percent():
    print("🔵 GET /charge")
    r = requests.get(f"{BASE_URL}/charge")
    return r.json()

def start_charging():
    print("🟢 POST /charge { 'charging': 'on' }")
    r = requests.post(f"{BASE_URL}/charge", json={"charging": "on"})
    print("↪️ Svar:", r.json())

def stop_charging():
    print("🟠 POST /charge { 'charging': 'off' }")
    r = requests.post(f"{BASE_URL}/charge", json={"charging": "off"})
    print("↪️ Svar:", r.json())

def get_base_load():
    print("🔵 GET / ad")
    r = requests.get(f"{BASE_URL}/baseload")
    return r.json()

def discharge_battery():
    print("🔻 POST /discharge { 'discharging': 'on' }")
    try:
        r = requests.post(f"{BASE_URL}/discharge", json={"discharging": "on"})
        print("↪️ Svar:", r.json())
    except Exception as e:
        print("⚠️ Fel vid anrop:", e)

def auto_charge():
    print("🔵 Automatisk laddning (lågpris + låg last)...")
    prices = get_price_per_hour()
    lowest_price = min(prices)
    info = get_info()
    current_hour = info['sim_time_hour']
    current_price = prices[current_hour]
    current_load = info['base_current_load']
    battery_percent = get_battery_percent()

    print(f"\n🕒 Timme: {current_hour}")
    print(f"💰 Elpris: {current_price} öre/kWh")
    print(f"⚡ Belastning: {current_load} kW")
    print(f"🔋 Batteri: {battery_percent}%")

    if current_price == lowest_price and current_load < 11 and 20 <= battery_percent < 80:
        print("✅ Villkor uppfyllda – laddning startas")
        start_charging()
    else:
        print("⛔ Villkor ej uppfyllda – laddning stoppas")
        stop_charging()

def auto_charge_low_load_loop():
    print("🔁 Automatisk laddning (endast låg hushållsförbrukning – loopar varje timme)")
    while True:
        info = get_info()
        current_hour = info['sim_time_hour']
        current_load = info['base_current_load']
        battery_percent = get_battery_percent()

        print(f"\n🕒 Timme: {current_hour}")
        print(f"⚡ Belastning: {current_load} kW")
        print(f"🔋 Batteri: {battery_percent}%")

        if current_load < 11 and 20 <= battery_percent < 80:
            print("✅ Villkor uppfyllda – laddning pågår")
            start_charging()
        else:
            print("⛔ Villkor ej uppfyllda – laddning stoppas")
            stop_charging()

        if battery_percent >= 80:
            print("🔋 Batteriet är fulladdat (80%). Avslutar loop.")
            stop_charging()
            break

        time.sleep(4)

def auto_charge_low_price_capped_loop():
    print("🔁 Automatisk laddning (lägsta elpris, max 11 kWh/dag – loopar varje timme)")
    total_energy_charged = 0.0  # kWh

    while True:
        prices = get_price_per_hour()
        lowest_price = min(prices)
        info = get_info()
        current_hour = info['sim_time_hour']
        current_price = prices[current_hour]
        current_load = info['base_current_load']
        battery_percent = get_battery_percent()

        print(f"\n🕒 Timme: {current_hour}")
        print(f"💰 Elpris: {current_price} öre/kWh")
        print(f"💸 Lägsta pris idag: {lowest_price} öre/kWh")
        print(f"⚡ Belastning just nu: {current_load} kW")
        print(f"🔋 Batterinivå: {battery_percent}%")
        print(f"🔌 Total laddad energi idag: {total_energy_charged:.2f} kWh")

        if (current_price == lowest_price and current_load < 11
                and 20 <= battery_percent < 80
                and total_energy_charged < 11):
            print("✅ Villkor uppfyllda – laddning startas")
            start_charging()
            time.sleep(4)  # En simuleringstimme (4 sek)
            stop_charging()
            total_energy_charged += 7.4 / 1  # 7.4 kW under 1h (simulerat)
        else:
            print("⛔ Villkor ej uppfyllda – laddning stoppas")
            stop_charging()
            time.sleep(4)

        if total_energy_charged >= 11:
            print("🛑 Maxgräns 11 kWh nådd för idag – laddning avslutas.")
            break
        if battery_percent >= 80:
            print("🔋 Batteriet är fulladdat – laddning avslutas.")
            break


        time.sleep(4)  # Vänta en simuleringstimme



def menu():
    while True:
        print("\n=== EV LADDSTATION – MENY ===")
        print("1. Visa laddstationens status")
        print("2. Visa aktuell hushållsförbrukning")
        print("3. Starta laddning manuellt")
        print("4. Stoppa laddning manuellt")
        print("5. Visa batterinivå")
        print("6. Automatisk laddning (både lågpris + låg last)")
        print("7. Automatisk laddning (endast låg hushållsförbrukning)")
        print("8. Automatisk laddning vid lägsta elpris (max 11 kWh)")
        print("9. Visa elpris per timme (24h)")
        print("10. Visa hushållets förbrukning (24h)")
        print("11. Avsluta")
        print("12. Återställ batteri till 20% (discharge)")

        val = input("Välj ett alternativ: ")

        if val == "1":
            info = get_info()
            print("↪️ Svar:", info)
        elif val == "2":
            info = get_info()
            print("Hushållets förbrukning just nu:", info['base_current_load'], "kW")
        elif val == "3":
            start_charging()
        elif val == "4":
            stop_charging()
        elif val == "5":
            battery = get_battery_percent()
            print("Batterinivå:", battery, "%")
        elif val == "6":
            auto_charge()
        elif val == "7":
            auto_charge_low_load_loop()
        elif val == "8":
            auto_charge_low_price_capped_loop()
        elif val == "9":
            prices = get_price_per_hour()
            print("\n💰 Elpris per timme (öre/kWh):")
            for i, price in enumerate(prices):
                print(f"  Timme {i:02d}: {price} öre/kWh")
        elif val == "10":
            base_load = get_base_load()
            print("\n⚡ Hushållets energiförbrukning (kW):")
            for i, val in enumerate(base_load):
                print(f"  Timme {i:02d}: {val} kW")
        elif val == "11":
            print("Avslutar...")
            break
        elif val == "12":
            discharge_battery()
        else:
            print("Ogiltigt val")

        time.sleep(1)

if __name__ == "__main__":
    menu()
