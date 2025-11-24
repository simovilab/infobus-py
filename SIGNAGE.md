# Signage.md

Es necesario tener docker-compuse

# Intrucciones para la capacidad y uso del CLI de signage

Para los comandos se realiza el llamado por medio de "docker-compose run signage"
Inicialmente se tienen uno comandos informativos, --help 


1. **docker-compose run signage --help**

Este comando mostrara todos los comandos iniciales de signage, que incluye: list, custom, route, station, stop, vehicle


2. **docker-compose run signage list**

El comando *docker-compose run signage list* muestra las plantillas disponibles.


3. **docker-compose run signage station**

El comando *docker-compose run signage station --help* muestra las opciones que ofrece esta plantilla, los str van entre comillas("")

  --template TEXT         : Plantilla a usar, esta incompleta ya que siempre usa la "station_modular" por defecto al usar el camando *station*

  --format                : Formato de salida, las opciones son svg, png o pdf, para svg es el predeterminado, por lo que este comando no es necesario    colocarlo cuando se quiere svg; ejemplo: --format pdf

  --size TEXT             Tamaño en formato WxH, esta incompleto, ya que siempre usa las medidas de las plantillas, ejemplo: --size 200x100

  --dpi INTEGER           DPI para PNG, cuando se usa *--format png* se tiene la opcion de colocar los dpi, por defecto son 300, ejemplo: --dpi 300

  --theme TEXT            Tema de colores (aun no implementado)

  --lang TEXT             Idioma (aun no implementado)

  --qr-url TEXT           URL para código QR, se coloca la URL la cual se desea que direccione el codigo QR generado, 
  ejemplo: --qr-url "https://maps.google.com/?q=Plaza+Central"

  -o, --output TEXT       Archivo de salida, se coloca el nombre del archivo a generar con su respectiva terminación; ejemplo (si --format png): --output prueba_station.png

  --station-name TEXT     Nombre de la estación (requerido), nombre de la estacion que aparece en la señal generada, funciona como titulo principal de la señal, ejemplo: --station-name "Estación"
  
  --line-name TEXT        Nombre de la línea, nombre o numero de la linea de la estacion, sirve como subtitulo de la señal, ejemplo: --line-name "L1"
  
  --help                  Show this message and exit.

A continuacion se muestran 3 ejemplos con los diferentes formatos donde se utilizan todas las opciones impementadas:

 docker-compose run signage station --station-name "Estación" --line-name "L1" --qr-url "https://maps.google.com/?q=Plaza+Central" --output prueba_station.svg 

 docker-compose run signage station --station-name "Estación" --line-name "L1" --qr-url "https://maps.google.com/?q=Plaza+Central" --format png --dpi 300 --output prueba_station.png

 docker-compose run signage station --station-name "Estación" --line-name "L1" --qr-url "https://maps.google.com/?q=Plaza+Central" --format pdf --output prueba_station.pdf

Las señales generadas se muestran en la carpeta *output*



4. **docker-compose run signage stop**

El comando *docker-compose run signage stop --help* muestra las opciones que ofrece esta plantilla, los str van entre comillas("")

  --template TEXT         : Plantilla a usar, esta incompleta ya que siempre usa la "stop_vertical" por defecto al usar el camando *stop*

  --format                : Formato de salida, las opciones son svg, png o pdf, para svg es el predeterminado, por lo que este comando no es necesario    colocarlo cuando se quiere svg; ejemplo: --format pdf

  --size TEXT             Tamaño en formato WxH, esta incompleto, ya que siempre usa las medidas de las plantillas, ejemplo: --size 200x100

  --dpi INTEGER           DPI para PNG, cuando se usa *--format png* se tiene la opcion de colocar los dpi, por defecto son 300, ejemplo: --dpi 300

  --theme TEXT            Tema de colores (aun no implementado)

  --lang TEXT             Idioma (aun no implementado)

  --qr-url TEXT           URL para código QR, se coloca la URL la cual se desea que direccione el codigo QR generado, 
  ejemplo: --qr-url "https://maps.google.com/?q=Plaza+Central"

  -o, --output TEXT       Archivo de salida, se coloca el nombre del archivo a generar con su respectiva terminación; ejemplo (si --format png): --output prueba_stop.png

  --stop-name TEXT        Nombre de la estación (requerido), nombre de la parada que aparece en la señal generada, funciona como titulo principal de la señal, ejemplo: --stop-name "Parada Final"
  
  --stop-code TEXT        Código de la parada (requerido), código o numero de la parada, sirve como subtitulo de la señal generada, 
  ejemplo: --stop-code "FINAL-001"
  
  --help                  Show this message and exit.

A continuacion se muestran 3 ejemplos con los diferentes formatos donde se utilizan todas las opciones impementadas:

 docker-compose run signage stop --stop-name "Parada Final" --stop-code "FINAL-001" --qr-url "https://maps.google.com/?q=Plaza+Central" --output prueba_stop.svg

 docker-compose run signage stop --stop-name "Parada Final" --stop-code "FINAL-001" --qr-url "https://maps.google.com/?q=Plaza+Central" --format pdf --output prueba_stop.pdf

 docker-compose run signage stop --stop-name "Parada Final" --stop-code "FINAL-001" --qr-url "https://maps.google.com/?q=Plaza+Central" --format png --dpi 300 --output prueba_stop.png

Las señales generadas se muestran en la carpeta *output*



5. **docker-compose run signage vehicle**

El comando *docker-compose run signage vehicle --help* muestra las opciones que ofrece esta plantilla, los str van entre comillas("")

  --template TEXT         : Plantilla a usar, esta incompleta ya que siempre usa la "vehicle_interior" por defecto al usar el camando *vehicle*

  --format                : Formato de salida, las opciones son svg, png o pdf, para svg es el predeterminado, por lo que este comando no es necesario    colocarlo cuando se quiere svg; ejemplo: --format pdf

  --size TEXT             Tamaño en formato WxH, esta incompleto, ya que siempre usa las medidas de las plantillas, ejemplo: --size 200x100

  --dpi INTEGER           DPI para PNG, cuando se usa *--format png* se tiene la opcion de colocar los dpi, por defecto son 300, ejemplo: --dpi 300

  --theme TEXT            Tema de colores (aun no implementado)

  --lang TEXT             Idioma (aun no implementado)

  --qr-url TEXT           URL para código QR, se coloca la URL la cual se desea que direccione el codigo QR generado, 
  ejemplo: --qr-url "https://maps.google.com/?q=Plaza+Central"

  -o, --output TEXT       Archivo de salida, se coloca el nombre del archivo a generar con su respectiva terminación; ejemplo (si --format png): --output prueba_vehicle.png

  --route-number TEXT     Numero de la ruta (requerido), numero de la ruta que aparece en la señal generada, funciona como titulo principal de la señal, ejemplo: --route-number "R5"
  
  --destination TEXT      Nombre del destino o la ruta, nombre del destino o la ruta , sirve como subtitulo de la señal, ejemplo: --destination "Centro"
  
  --help                  Show this message and exit.

A continuacion se muestran 3 ejemplos con los diferentes formatos donde se utilizan todas las opciones impementadas:

 docker-compose run signage vehicle --route-number "R5" --destination "Centro" --qr-url "https://maps.google.com/?q=Plaza+Central" --format png --dpi 300 --output prueba_vehicle.png

 docker-compose run signage vehicle --route-number "R5" --destination "Centro" --qr-url "https://maps.google.com/?q=Plaza+Central" --format pdf --output prueba_vehicle.pdf

 docker-compose run signage vehicle --route-number "R5" --destination "Centro" --qr-url "https://maps.google.com/?q=Plaza+Central" --output prueba_vehicle.svg


Las señales generadas se muestran en la carpeta *output*



6. **docker-compose run signage route**
(INCOMPLETA)(REDUNDANTE)

El proposito de este comando era tener la capacidad de de crear una señal de una ruta usando como base otras plantillas, sin embargo, esto lo mismo que usar la opcion del comando de "vehicle" o otra plantilla por lo que es redundante, lo unico que cambia es que el nombre de la ruta se utiliza *--route-name* en vez de *--route-number* y que usa *--template* para selecionar una plantilla, puede servir para una futura plantilla nueva en un futuro mas no aporta nada diferente de "vehicle".

Ejemplo completo:
 docker-compose run signage route --template "vehicle_interior" --route-name "UCR" --route-number "R6" --qr-url "https://maps.google.com/?q=Plaza+Central" --format png --output prueba_route.png


Las señales generadas se muestran en la carpeta *output*



7. **docker-compose run signage custom**
(INCOMPLETA)

Este opcion esta imcompleta,el proposito de esta opcion es en un futuro personalizar algunas caracteristicas de una señal sin usar mantener los atributos de algunas plantillas, aunque puede ser sustutuidos en un futuro por mas comandos en CLI de cada plantilla.

Con *docker-compose run signage custom --help* se muestra los posibles comandos, sin embargo, solo funcionan por ahora --template, --format, --qr-url y --output

Comandos que funcionan:
 --template : Plantilla base, se usa una de las mencionas en *docker-compose run signage list*; ejemplo: --template "vehicle_interior"

 --format   : Formato del archivo a generar, esta las opciones png, svg o pdf, para svg es el predeterminado, por lo que este comando no es necesario   colocarlo cuando se queire svg; ejemplo: --format png

 --qr-url   : Se coloca la URL la cual se desea que direccione el codigo QR generado, ejemplo: --qr-url "https://maps.google.com/?q=Plaza+Central"

 --output   : Se coloca el nombre del archivo a generar con su respectiva terminación; ejemplo (si --format png): --output NOMBRE.png

Estos serian los comandos que funcionan por ahora, por lo esta funcion solo sirve para genenrar un QR en el formato que se desea.
Ejemplo completo: docker-compose run signage custom --template "vehicle_interior" --qr-url "https://maps.google.com/?q=Plaza+Central" --format png --output prueba.png


Las señales generadas se muestran en la carpeta *output*
