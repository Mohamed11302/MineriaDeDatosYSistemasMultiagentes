from dotenv import load_dotenv
import os
load_dotenv()
from cryptography.fernet import Fernet

def PasswordBBDD()-> str:
    clave = os.environ.get('BBDD')
    contraseña_cifrada = os.environ.get('CLAVE')
    if clave == None or contraseña_cifrada == None:
        print("[ERROR]. COMPRUEBA QUE EL ARCHIVO .env ESTA EN LA RAÍZ DEL REPOSITORIO")
        print("TERMINANDO EJECUCION....")
        os._exit(1)
    else:   
        cipher_suite = Fernet(clave)
        contraseña_descifrada = cipher_suite.decrypt(contraseña_cifrada).decode()
    return contraseña_descifrada

def Certificado()->str:
    certificado = os.environ.get('CERTIFICADO')
    if certificado == None:
        print("[ERROR]. COMPRUEBA QUE EL ARCHIVO .env ESTA EN LA RAÍZ DEL REPOSITORIO")
        print("TERMINANDO EJECUCION....")
        os._exit(1)
    return certificado
