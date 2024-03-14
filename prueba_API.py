import requests
import json
import time
import signal, sys
from datetime import datetime

def quitar(sig, frame):
    print("se interrumpio la operacion. CTRL+C")
    sys.exit()
signal.signal(signal.SIGINT, quitar)

def fecha_hora(hora):
    time_format="%Y-%m-%dT%H:%M:%S.%fZ"
    newhora=datetime.strptime(hora,time_format)
    lasthour= str(newhora)[:-7]
    return lasthour
    
    
def main():
    datos_raw= requests.get("https://api.datos.gob.mx/v1/condiciones-atmosfericas")
    if int(datos_raw.status_code) != 200:
        print("Error no se pudo completar la solicitud")
        
    datos=json.loads(datos_raw.text)

    for dato in datos['results']:
        print(f"""---El {fecha_hora(dato['date-insert'])} en {dato['name']}, {dato['state']} habia:
    Una humedad de {dato['relativehumidity']}%
    Una probabilidad de {dato['probabilityofprecip']}% de lluvia
    Y se pronosticaban {dato['skydescriptionlong']}\n""")
    
    guardar= input("Desea guardar los datos?[Y/N]")
    
    if guardar=="Y" or guardar=="y":
        with open("savedata.json","w") as archivo:
            archivo.write(json.dumps(datos['results']))
            

if __name__ == "__main__":
    main()