import serial
import time
import math
# Configura el puerto serie
puerto = serial.Serial('COM5', 4800)  # Ajusta '/dev/ttyUSB0' al puerto correcto en tu sistema

def separaGradosMinutosLatitud(cadena):
    grados, minutos = cadena[:2], cadena[2:]
    return grados, minutos

hola = "aisdgjaiosdj"
print(separaGradosMinutosLatitud(hola))
def separar_gpgga(cadena_nmea):
    # Dividir la cadena en trozos utilizando la coma como delimitador
    campos = cadena_nmea.split(',')
    
    if campos[0] == '$GPGGA' and len(campos) >= 14:
        # Los campos están en el siguiente orden:
        # 0: Identificador de la sentencia
        # 1: Hora UTC
        # 2: Latitud
        # 3: Hemisferio Norte o Sur
        # 4: Longitud
        # 5: Hemisferio Este u Oeste
        # 6: Calidad del GPS (1=GPS fijo, 0=Sin fijar)
        # 7: Número de satélites utilizados
        # 8: Precisión horizontal
        # 9: Altitud sobre el nivel del mar
        # 10: Unidades de altitud (metros)
        # 11: Separación geoidal
        # 12: Unidades de separación geoidal (metros)
        # 13: Diferencia entre la altitud de la antena y el geode
        # 14: Unidades de diferencia entre la altitud de la antena y el geode
        
        # Imprimir los campos separados
        print("Hora UTC:", campos[1])
        print("Latitud:", campos[2], campos[3])
        print("Longitud:", campos[4], campos[5])
        print("Calidad del GPS:", campos[6])
        print("Número de satélites utilizados:", campos[7])
        print("Precisión horizontal:", campos[8])
        print("Altitud sobre el nivel del mar:", campos[9], campos[10])
        print("Separación geoidal:", campos[11], campos[12])
        print("Diferencia entre la altitud de la antena y el geode:", campos[13], campos[14])
        print("Latitud y longitud", gga_to_utm(float(campos[2]),float(campos[4])),"\n\n")
    else:
        print("Mala señal GPS.")
        
try:
    while True:
        # Lee una línea del puerto serie
        linea = puerto.readline()
        
        # Decodifica los datos si es necesario (depende de la configuración de tu dispositivo)
        linea_decodificada = linea.decode('utf-8').strip()  # Utiliza el método de decodificación adecuado
        
        # Imprime la línea leída
       # print(linea_decodificada)
        time.sleep(1)
        separar_gpgga(linea_decodificada)

finally:
    puerto.close()  # Asegúrate de cerrar el puerto serie cuando hayas terminado de usarlo