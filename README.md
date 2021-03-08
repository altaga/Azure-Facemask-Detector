# Azure Facemask Detector

Implementación real de un servicio de detección de cubre bocas powereado por Azure ML, Function App y Azure API Management Service.

- [Azure Facemask Detector](#azure-facemask-detector)
- [AzureML Model Training](#azureml-model-training)
- [Azure Model Deployment](#azure-model-deployment)
- [Azure Function App Deployment as API](#azure-function-app-deployment-as-api)
- [Azure API implementation](#azure-api-implementation)
  - [Hardware Tested with the API](#hardware-tested-with-the-api)
  - [Devices Tested with the webapp](#devices-tested-with-the-webapp)

# AzureML Model Training

El modelo de inteligencia artifial se entreno en la plataforma de Machine Learning de Azure, todas las caracteristicas de el environment de entrenamiento fueron las siguientes:

Azure ML Settings:

- Compute Attributes:
  -  Region: centralus
  -  Virtual machine size:
     -  STANDARD_DS2_V2 (2 Cores, 7 GB RAM, 14 GB Disk)
  - Processing Unit:
     -  CPU - General purpose
  - Kernel:
    - Python 3.6.9

Todo el codigo estara en el siguiente enlace:



Una vez los descargues tendrás que ponerlo en la interfaz de Azure de la siguiente forma.

<img src="./Images/ML.png">

Una Vez hecho esto podremos correr el entrenamiento sin problema, el codigo ya esta diseñado para bajar la base de datos se nuestro repositorio.

https://github.com/altaga/Facemask-Opt-Dataset

Una vez inicie el entrenamiento hay que poner mucha atencion al Link que aparecera en la interfaz, ya que con este link podremos acceder al model cuando termine el programa de ejecutarse.

<img src="./Images/MLlink.png">

Una vez termine el entrenamiento podremos descargar nuestro modelo de la siguiente forma.

<img src="./Images/MLdownload.png">

Ahora pasaremos a mostrar como realizamos el despliegue de nuestro modelo en una Function App.

# Azure Model Deployment
 
Azure Function App:

  - Python 3.7
  - Linux
  - Tflite Interpreter 1.0.1

# Azure Function App Deployment as API

Descripcion:

# Azure API implementation

Todos los Dispositivos mencionados a continuación consumen la API montada en Azure. La API recibe imágenes con el Encoding Base64.

Example Image:

<img src="Images/logo.png">

Example Base64 Encoding (32 x 32):

    iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAASlQTFRFAAAAAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHHGAHLGAHLGAHLGAHLGAHLGAHTHAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAG7IAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHPGAHLGAHLGAHLGAHLGAHLGAHLGAHLIAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLGAHLFAHLGAHLGAHLGAHLGAHLGAHHGAHLGAHLGAHLGAHLGAHPHAHLGAHLGAHLGAHLGAHLGAHHGAHLGAHLGAHLGAHLGAHPGAHLGAHLGAHLGAHLGAHLG+gRtQQAAAGN0Uk5TACgSNKgPi/sxNrQHsv/QAZxHHNFdAunbJ+fKA1NrM+hZqu0QAtoFCPWWeUr+E+8KrMOibgHPUvQf8+QLxn5N/Hhc/Rh2+B4D456lVkEHLh2jEQRkpEz6XhVLgdTsF0Jxm71nKNQClAAAAP5JREFUeJxjYBiWgJEJvzwzCwMrPnk2dg5OLtzS3Dy8fPwCvIK45IWEeXlFRMV4xbmxy0tI8vJKScvw8vLKYpWXkwdKKTAoAkklZSzyKqpAGXE1dQ0gxauJRYEWSEKEQRtE8epwYMjr6gHF5fUZDMAKeA350RUYgYSNGUxMIQp4zdBdyA4UNAe6zcISosDKGlWBDUjQFsSys4eocECRdwQJOTmD2S4QBa5uSPLuHiAhWBx4QlR4ISnwBov4QHm+fBAVfnB5f5AXeQPg/EBVsALTIJhAcAgIMCJMDA0DqwjHCC0GhojIKINoqE95Y1CjJDYuPiGRTxgZJGExYmgCAEWHHVydzkRzAAAAAElFTkSuQmCC

## Hardware Tested with the API

  - ESP32 Cam
  - RPI4 with Camera
  
## Devices Tested with the webapp

(la pagina web consume directamente de la misma API):

- Web App Tested: https://polite-bush-0d957ae10.azurestaticapps.net/
  - Samsung Galaxy S10+
  - iPhone
  - Desktop
