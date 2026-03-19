# Guia QGIS para trasladar el caso a un plano real

## Objetivo

Usar un plano real del edificio en QGIS para ubicar los puntos P1, P2 y P3 y documentar el ejercicio con una capa vectorial reutilizable.

## Material fuente incluido

- `puntos_medida_template.csv`: plantilla editable para importar puntos en QGIS.
- `puntos_medida_template.geojson`: alternativa vectorial lista para abrir directamente en QGIS.

## Flujo recomendado

1. Obtener el plano del edificio en PDF, imagen o CAD exportado a una imagen.
2. Si el plano no esta georreferenciado, abrir QGIS y usar el Georreferenciador para ajustarlo con puntos de control.
3. Definir un sistema de referencia adecuado:
   - Si es un plano local de edificio, puede usarse un sistema local cartesiano.
   - Si el edificio ya esta en cartografia campus, usar el CRS del proyecto institucional.
4. Elegir uno de los dos formatos fuente:
   - CSV si se quiere editar rapidamente en hoja de calculo antes de importar.
   - GeoJSON si se quiere abrir directamente como capa vectorial con atributos.
5. Si se usa CSV, asignar las columnas `x_m` e `y_m` como coordenadas del punto.
6. Revisar que los puntos P1, P2 y P3 coincidan con entrada, aula y semisotano reales.
7. Completar o corregir atributos de perdidas por tramo con datos reales de obra.
8. Simbolizar la capa por tipo de punto o por estado de cobertura.
9. Componer un mapa de entrega con:
   - titulo
   - leyenda
   - escala grafica
   - flecha norte
   - cuadro de observaciones

## Campos sugeridos de la capa

- `id_punto`: codigo corto, por ejemplo `P1`.
- `nombre`: nombre descriptivo del punto.
- `nivel`: planta o semisotano.
- `uso`: entrada, aula, archivo, etc.
- `x_m`, `y_m`: coordenadas del plano.
- `z_m`: cota o altura relativa opcional.
- `dist_horizontal_m`: distancia horizontal a la estacion base.
- `fachada_db`, `paredes_db`, `forjados_db`, `extra_db`: perdidas asignadas.
- `servicio_objetivo`: voz o datos basicos.
- `observaciones`: notas de campo.

## Recomendacion docente

Mantener la correspondencia entre tabla, plano y conclusion final usando siempre los codigos `P1`, `P2` y `P3`. Si el ejercicio se amplifica con mas puntos, seguir la misma nomenclatura.
