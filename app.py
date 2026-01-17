import requests
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime

# Se elimina la dependencia de streamlit para evitar el error de módulo no encontrado
# En su lugar, se usa una interfaz por consola simple para mostrar los datos

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bcv():
    try:
        r = requests.get("https://www.bcv.org.ve/", verify=False, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        rate = soup.find('div', {'id': 'dolar'}).find('strong').text.strip()
        return float(rate.replace(',', '.'))
    except:
        return None

def get_binance():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {"asset":"USDT","fiat":"VES","merchantCheck":False,"page":1,"rows":10,"payTypes":[],"publisherType":None,"tradeType":"BUY"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        prices = [float(ad['adv']['price']) for ad in r.json()['data']]
        return sum(prices) / len(prices)
    except:
        return None


def main():
    print("\n🇻🇪 Monitor de Divisas")
    print(f"Actualizado: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}\n")

    bcv = get_bcv()
    binance = get_binance()

    print("🏛️ BCV")
    if bcv:
        print(f"Tasa Oficial: Bs. {bcv:,.2f}")
    else:
        print("BCV no disponible")

    print("\n🟡 Binance P2P")
    if binance:
        diff = ((binance - bcv) / bcv) * 100 if bcv else 0
        print(f"Promedio USDT: Bs. {binance:,.2f} (Delta: {diff:.2f}%)")
    else:
        print("Binance no disponible")

    print("\n🧮 Calculadora de Conversión")
    try:
        monto = float(input("Cantidad en Dólares ($): "))
        if monto < 0:
            print("Por favor, ingrese un valor positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número.")
        return

    if bcv and binance:
        print(f"\nBCV: Bs. {monto * bcv:,.2f}")
        print(f"Binance: Bs. {monto * binance:,.2f}")
    else:
        print("No hay datos suficientes para realizar la conversión.")

if __name__ == "__main__":
    main()