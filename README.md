# Mavens-Pizza-2016-xml
Con el código de este repositorio se limpian los datos de 'Mavens Pizza' de 2016 para posteriormente realizar una predicción sobre los ingredientes que deberán comprar. Se realizará un informe de calidad de los datos que se devolverá en formato txt y se devolverá también un xml con la predicción de los ingredientes la calidad de los datos.

Este repositorio contiene los siguientes ficheros necesarios para la ejecución:
- **"requirements.txt"**: contiene todas las librerías necesarias para la ejecución del programa
- **"orders.csv"**: contiene los datos relacionados a las fechas de cada pedido
- **"order_details.csv"**: contiene los datos relacionados a la cantidad y tipo de pizza de cada pedido concreto
- **"pizzas.csv"**: contiene información relacionada con los distintos tipos de pizza de la pizzería como su tamaño y su precio
- **"pizza_types.csv"**: incluye los datos relacionados con la categoría de cada tipo de pizza y los ingredientes que contiene
- **"pizzas3.py"**: contiene el código que se debe de ejecutar para obtener la predicción de los ingredientes que deberá de comprar la pizzaría. El programa consta de dos ETL, una para la extracción y el tratado de los datos y otra para la elaboración de la predicción. En lo relacionado al tratado de los datos, el programa los manipula hasta obtener un único dataframe que contenga la información de cada pedido, la semana y día de la semana en el que se realizó y los ingredientes requeridos para la preparación de ese pedido en concreto. Para la realización de la predicción lo que hace el programa es establecer la predicción como la media de las modas de cada ingrediente por semana, es decir, calcula el total de cada ingrediente necesitado cada semana del año y se queda con la moda de cada ingrediente. En caso de empate hace la media de las modas. El programa también realiza un análisis de la calidad de los datos contenidos en los ".csv" de Mavens Pizza. Para dicho análisis tiene en cuenta valores como el número de nulls y de nans de cada fichero. Una vez realizado el análisis de los datos se procede a realizar una limpieza exhaustiva en las fechas, poniéndolas todas en el mismo formato, y en los pedidos, transformando valores de pedidos negativos a positivos y modificando los nombres de las pizzas pedidas para que todas estén escritas como en el csv de pizza_types (para ello se cambian espacios por "_", "0" por "o" y otros muchos caracteres más). Tanto la predicción como el informe de la calidad de los datos se almacenará en un fichero ".xml" ("reporte.xml").

Y tras su ejecución el programa genera los siguientes ficheros de salida:
- **"informe_calidad_datos.txt"**: contiene el análisis de la calidad de los datos de la pizzería
- **"reporte.xml"**: contendrá una categoría denominada reporte que a su vez tendrá el nombre de cada ingrediente y su cantidad predicha y contendrá también un apartado de informe de calidad de los datos. Dentro de la parte del informe primero se hará referencia al nombre del fichero al que corresponde el análisis y dentro de ese fichero se almacenará el análisis columna a columna. De cada columna se dirá el número de nans, de nulls y el tipo.

### Ejecución del programa:

Primero se deberá hacer un pip install -r requirements.txt para que se descarguen todas las librerías necesarias para el programa. Posteriormente ya se podrá ejecutar el fichero "pizzas3.py" que tardará aproximadamente un minuto en devolver la predicción.
