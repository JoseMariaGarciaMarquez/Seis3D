# Seis3D: Herramienta de Análisis de Datos Sísmicos en 3D
![ventana](https://github.com/JoseMariaGarciaMarquez/Seis3D/assets/30852961/9305405f-e180-46ee-8839-d7f77fc013e6)

## Descripción
SIS3D es una herramienta de análisis de datos sísmicos en 3D, diseñada para cargar, visualizar y realizar análisis en cubos sísmicos. La herramienta permite la visualización de secciones sísmicas y la generación de perfiles con diferentes atributos, como RMS, Amplitud Instantánea (AI), Frecuencia Instantánea (FI) y Fase Instantánea (PI).

## Requisitos
- Python 3.x
- Bibliotecas requeridas: numpy, segysak, pathlib, matplotlib, scipy, tkinter, xarray

## Instrucciones de Uso
1. **Cargar Cubo Sísmico:**
   - Haz clic en "Buscar" para seleccionar el archivo del cubo sísmico.
  ![ventana_carga](https://github.com/JoseMariaGarciaMarquez/Seis3D/assets/30852961/e567fb4c-58a0-4342-a417-756d2b7f9587)

   - Presiona "Cargar" para cargar el cubo sísmico seleccionado.
<img width="827" alt="terminal_carga" src="https://github.com/JoseMariaGarciaMarquez/Seis3D/assets/30852961/c1cfa06b-4864-4ccd-9d5b-d30f1d23edb5">

2. **Configuración de Análisis:**
   - Ingresa el espaciado en X e Y.
   - Especifica las ilines y xlines de inicio y fin.
   - Selecciona la carpeta de destino para guardar los perfiles y perfiles con atributos.
   - Elige un mapa de colores para la visualización de las secciones sísmicas.
 ![ventana_2](https://github.com/JoseMariaGarciaMarquez/Seis3D/assets/30852961/f2b662e1-7255-4e63-91fd-2ce0c5ba553c)


3. **Generar Perfiles Sísmicos:**
   - Haz clic en "Guardar perfiles" para generar y guardar perfiles sísmicos en las direcciones NW-SE y NE-SW.
![iline2113](https://github.com/JoseMariaGarciaMarquez/Seis3D/assets/30852961/bf8db0a9-f4f6-4864-996f-6e53b51bcc9c)
4. **Calcular Atributos:**
   - Selecciona un atributo (RMS, AI, FI, PI) en el menú desplegable.
   - Presiona "Calcular" para obtener el atributo seleccionado.
![ventana_atr](https://github.com/JoseMariaGarciaMarquez/Seis3D/assets/30852961/1604f158-5a00-436e-85e9-550df3cc5580)

5. **Generar Perfiles con Atributo:**
   - Elige un mapa de colores para la visualización de los perfiles con atributo.
   - Haz clic en "Guardar perfiles con atributo" para generar y guardar perfiles con el atributo seleccionado.
![ventana_atr2](https://github.com/JoseMariaGarciaMarquez/Seis3D/assets/30852961/270153c9-e88c-406d-99d1-802c0a0f9643)
![iline2113RMS](https://github.com/JoseMariaGarciaMarquez/Seis3D/assets/30852961/a49210bf-4fba-4c53-acb4-88df175682c4)

## Notas
- La herramienta utiliza la biblioteca `segysak` para cargar y procesar archivos SEGY.
- Los perfiles sísmicos y perfiles con atributos se guardan en la carpeta especificada.

## Agradecimientos
Esta herramienta utiliza varias bibliotecas de código abierto, incluyendo numpy, segysak, matplotlib, y otras, que han contribuido al desarrollo y funcionalidad de SIS3D.

