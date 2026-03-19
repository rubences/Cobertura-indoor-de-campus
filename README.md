# Cobertura-indoor-de-campus

Ejercicio de penetracion indoor adaptado a un edificio real donde interesa garantizar voz, mensajeria y acceso a plataformas digitales.

## Objetivo docente

El alumno debe estimar si la cobertura macro exterior es suficiente en distintos puntos del edificio o si hace falta refuerzo indoor mediante DAS, repetidor o small cell.

## Escenario

- Edificio de varias plantas con fachada, tabiqueria y semisotano tecnico.
- Portadora principal LTE 1800 MHz.
- Portadora de respaldo UMTS 2100 MHz.
- Extension opcional para comparar 800 MHz y 2600 MHz.
- Antena exterior a 22 m de altura.

## Conceptos que se refuerzan

- Perdida outdoor-to-indoor.
- Penetracion por fachada, paredes y forjados.
- Presupuesto de enlace.
- Comparacion entre bandas para cobertura interior.

## Entregable principal

El repositorio incluye el notebook [ejercicio_cobertura_indoor.ipynb](ejercicio_cobertura_indoor.ipynb), que contiene:

- Definicion de tres puntos de usuario: entrada, aula de segunda planta y archivo en semisotano.
- Calculo de perdidas exteriores e interiores.
- Verificacion contra umbrales de servicio para voz y datos basicos.
- Tabla de perdidas por tramo.
- Croquis simplificado del edificio con puntos de medida.
- Recomendacion final sobre macro suficiente o necesidad de refuerzo indoor.
- Comparativa opcional por banda.

## Flujo de trabajo recomendado

Instalacion de dependencias:

1. Ejecutar `python -m pip install -r requirements.txt`
2. Abrir el notebook en Jupyter.

Ejecucion del ejercicio:

1. Abrir el notebook en Jupyter.
2. Ejecutar las celdas para generar las tablas y el croquis.
3. Revisar la recomendacion final para cada punto.
4. Si se dispone de plano real, trasladar los puntos a QGIS para documentar la practica sobre cartografia o planos georreferenciados.

## Salidas esperadas al ejecutar el notebook

Se crea la carpeta `salidas` con:

- `tabla_perdidas_lte1800.csv`
- `comparativa_bandas.csv`
- `resumen_recomendaciones.csv`

## Criterio de interpretacion

- Entrada principal: normalmente cubierta por macro exterior.
- Aula de segunda planta: puede quedar cubierta para el objetivo base, aunque con menos margen.
- Semisotano: candidato natural a refuerzo indoor.

## Herramientas open source

- Python
- Jupyter
- QGIS


