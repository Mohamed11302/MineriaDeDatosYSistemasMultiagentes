import subprocess

comando_instalacion = "pip install -r ../requirements.txt"
print("INSTALANDO PAQUETES NECESARIOS PARA EJECUTAR EL PROYECTO")
try:
    subprocess.run(comando_instalacion, shell=True, check=True)
    print("PAQUETES INSTALADOS CORRECTAMENTE.")
except subprocess.CalledProcessError as e:
    print(f"ERROR AL INSTALAR LOS PAQUETES: {e}")


subprocess.run(["python", "Scraping_PIB_per_capita.py"])
subprocess.run(["python", "Scraping_Puntos_De_Carga.py"])
subprocess.run(["python", "Scraping_Diesel_Gasoline.py"])
subprocess.run(["python", "Scraping_Model_Per_Year.py"])
subprocess.run(["python", "Scraping_Electricity_In_Countries.py"])
subprocess.run(["python", "Scraping_Vehiculos.py"])
subprocess.run(["python", "Scraping_Estudios.py"])
subprocess.run(["python", "Scraping_CO2.py"])