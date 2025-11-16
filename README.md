# Transformaciones realizadas en los scripts de limpieza y verificacion

## 1. check_mortalidad.py
Evalua el archivo MortalidadPrematura2021.csv.
- Carga segura del CSV usando dtype=str para evitar conversiones indeseadas.
- Imprime numero de filas y columnas.
- Lista nombres de columnas.
- Muestra valores unicos de columnas clave para verificar calidad.
- No realiza transformaciones; solo inspeccion y diagnostico.

## 2. check_pm25.py
Evalua los archivos de PM25 antes de limpieza.
- Carga cada archivo PM25 bruto con dtype=str.
- Muestra forma del dataframe y primeros nombres de columnas.
- Lista valores unicos por columna para validar consistencia.
- No limpia; solo diagnostica.

## 3. check_precipitacion.py
Evalua el archivo de precipitacion.
- Carga del CSV como texto.
- Revisa columnas, duplicados, valores faltantes y tipos.
- Verifica consistencia temporal.
- No realiza transformaciones; solo inspeccion.

## 4. check_temperatura.py
Diagnostico del archivo de temperatura.
- Carga con dtype=str.
- Valida columnas esperadas, rangos de valores y presencia de nulos.
- Verifica formato de fechas y horas.
- No modifica datos.

# Scripts de limpieza

## 5. clean_mortalidad.py
Limpieza final de MortalidadPrematura2021.csv.
Transformaciones aplicadas:
- Elimina columnas no necesarias: _id, ANO, EDAD_QUINQUENAL, SUBRED.
- Renombra columnas a formato estandarizado con minusculas y guiones bajos.
- Corrige tildes y caracteres especiales.
- Normaliza texto (eps, sexo, nacionalidad, localidad).
- Convierte edad a entero cuando es posible.
- Convierte mes a entero.
- Valida que CIE10_AGRUPADA y CIE10_BASICA existan y no sean nulas.
- Elimina filas duplicadas.
- Exporta un CSV limpio listo para el modelo multidimensional.

## 6. clean_pm25.py
Limpieza del archivo PM25 2021.
Transformaciones aplicadas:
- Corrige codificacion de nombres de estaciones.
- Normaliza nombres de estaciones a minusculas sin tildes.
- Aplica diccionario direccion_por_estacion.
- Aplica diccionario localidad_por_estacion.
- Verifica que todas las estaciones del CSV esten en los diccionarios.
- Limpia columnas de fecha y hora, creando una columna datetime.
- Convierte concentraciones a numerico.
- Elimina filas con valores invalidos.
- Exporta archivo limpio a standard_spacetime.

## 7. clean_precipitacion.py
Limpieza del archivo de precipitacion.
Transformaciones:
- Normaliza nombres de columnas.
- Convierte fechas a formato datetime.
- Limpia valores no numericos en la columna precipitacion_mm.
- Elimina registros duplicados.
- Filtra valores fisicamente imposibles (negativos).
- Exporta CSV limpio.

## 8. clean_temperatura.py
Limpieza del archivo de temperatura.
Transformaciones:
- Normalizacion de nombres de columnas.
- Conversion de fecha y hora a datetime unificado.
- Conversion de la temperatura a numerico.
- Eliminacion de duplicados.
- Eliminacion de valores fuera de rango razonable.
- Exportacion del archivo procesado.

# Procesamiento avanzado de PM25

## 9. clean_unified_PM25.py
Transformaciones:
- Carga de ambos CSV limpios de PM25.
- Normaliza columnas para garantizar coincidencia entre archivos.
- Unifica en un solo dataframe.
- Elimina duplicados.
- Crea columna fecha_hora unificada en formato datetime.
- Ordena por fecha_hora y estacion.
- Exporta archivo PM25_2021_unificado.csv.

## 10. merge_pm25.py
Union de archivos horarios de PM25.
Transformaciones:
- Carga dos archivos PM25_2021_1_hourly y PM25_2021_2_hourly.
- Concatena ambos en un solo dataframe.
- Elimina duplicados.
- Convierte fecha_hora a datetime.
- Ordena por fecha_hora y estacion.
- Exporta un unico archivo PM25_2021_hourly.csv.
