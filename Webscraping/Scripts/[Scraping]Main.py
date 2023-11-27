import subprocess

comando_instalacion = "pip install -r requirements.txt"
print("INSTALANDO PAQUETES NECESARIOS PARA EJECUTAR EL PROYECTO")
try:
    subprocess.run(comando_instalacion, shell=True, check=True)
    print("PAQUETES INSTALADOS CORRECTAMENTE.")
except subprocess.CalledProcessError as e:
    print(f"ERROR AL INSTALAR LOS PAQUETES: {e}")


subprocess.run(["python", "Webscraping/Scripts/[Scraping]PIB_per_capita.py"])
subprocess.run(["python", "Webscraping/Scripts/[Scraping]Puntos_De_Carga.py"])
subprocess.run(["python", "Webscraping/Scripts/[Scraping]Gasoline_Diesel.py"])
subprocess.run(["python", "Webscraping/Scripts/[Scraping]Model_Per_Year.py"])
subprocess.run(["python", "Webscraping/Scripts/[Scraping]Electricity_In_Countries.py"])
subprocess.run(["python", "Webscraping/Scripts/[Scraping]Vehiculos.py"])
subprocess.run(["python", "Webscraping/Scripts/[Scraping]Level_Of_Studies.py"])
subprocess.run(["python", "Webscraping/Scripts/[Scraping]CO2.py"])