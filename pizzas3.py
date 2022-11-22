# Qué hay que comprar para la semana que viene
"""
- The order_details tables has 48621 rows containing order details regarding
pizza type and order quantity.
- The orders table record the datetime indicators of the 21351 orders.
- The pizza_types table specifies the category, ingredients information about
the 33 different pizza types offered by the pizza place.
- The pizzas table has 97 rows containing the pricing details of pizza based on
the size and pizza type
"""

import pandas as pd
import xml.etree.ElementTree as ET
import warnings


warnings.filterwarnings("ignore")


def extract_csv():

    fechas = pd.read_csv('orders.csv', sep=';')
    pedidos = pd.read_csv('pizzas.csv', sep=',')
    detalles = pd.read_csv('order_details.csv', sep=';')
    ingredientes = pd.read_csv('pizza_types.csv', sep=',', encoding='Windows-1252')

    informe = informe_de_datos(fechas, pedidos, detalles, ingredientes)

    return (fechas, pedidos, detalles, ingredientes, informe)


def transform_csv(fechas, pedidos, detalles, ingredientes):

    # Primero ordenamos los id y posteriormente reestablecemos
    # los índices del dataframe

    fechas = fechas.sort_values('order_id')
    fechas.index = [i for i in range(fechas.shape[0])]

    detalles = detalles.sort_values('order_details_id')
    detalles = detalles.dropna()
    detalles.index = [i for i in range(detalles.shape[0])]

    # En fechas no transformamos las horas ya que esa columna no se va a
    # utilizar para nada
    # Transformamos las fechas todas al mismo formato
    # Si en alguno da error lo cambiamos por un null

    for i in fechas.index:

        fechas.loc[i, 'date'] = pd.to_datetime(fechas['date'].iloc[i], errors='coerce')

    # Vamos a sustituir los nats por el valor que se haya podido transformar
    # antes

    fi = pd.to_datetime('2016-01-01')

    for i in fechas.index:

        if str(fechas['date'].iloc[i]) == str(pd.NaT):
            fechas.loc[i, 'date'] = fi

        else:
            fi = fechas['date'].iloc[i]

    # Para el dataframe de detalles, primero nos quitaremos todos los NaN
    # y posteriormente nos quitaremos todos los negativos en la columna de
    # orders, reemplazándolos por su valor absoluto -> Asumimos que se
    # equivocaron al introducir los datos

    # detalles = detalles.dropna()

    # Reemplazamos os números escritos con letras por números enteros
    # Habiendo visto los datos los únicos números que aparecen a mano
    # son one y two

    detalles['quantity'].replace(to_replace=r'[O-o][N-n][E-e]', value=1, regex=True,inplace=True)
    detalles['quantity'].replace(to_replace=r'[T-t][W-w][O-o]', value=2, regex=True,inplace=True)

    # Obtengo los índices de aquellos números negativos en cantidad

    for i in detalles.index:

        try:
            detalles.loc[i, 'quantity'] = abs(int(detalles['quantity'].iloc[i]))
        except:
            ...

    detalles['pizza_id'] = detalles['pizza_id'].str.replace(' ', '_')
    detalles['pizza_id'] = detalles['pizza_id'].str.replace('-', '_')
    detalles['pizza_id'] = detalles['pizza_id'].str.replace('@', 'a')
    detalles['pizza_id'] = detalles['pizza_id'].str.replace('0', 'o')
    detalles['pizza_id'] = detalles['pizza_id'].str.replace('3', 'e')

    # Vamos a querer tener todos los datos en un único dataframe
    # Modificaremos el de order details pues es el más completo
    # Le añadiremos una nueva columna que sea el número de la semana
    # asociado a la fecha del pedido. Añadiremos una
    # columna por cada posible ingrediente de la pizza

    dias = []
    num_semana = []

    for fecha in fechas['date']:
        dia = pd.to_datetime(fecha, dayfirst=True)
        dias.append(dia.day_of_week)
        num_semana.append(dia.week)

    fechas['semana'] = num_semana
    fechas['dia_semana'] = dias

    # Nos guardamos para cada order_id en detalles su fecha
    # asociada

    semanas = []
    dia_semana = []

    for s in detalles['order_id']:

        indice = fechas[fechas['order_id'] == s].index
        semana = fechas['semana'].iloc[indice]
        d = fechas['dia_semana'].iloc[indice]

        semanas.append(int(semana))
        dia_semana.append(int(d))

    detalles['semana'] = semanas
    detalles['dia'] = dia_semana

    # Obtenemos todos los posibles ingredientes que emplea
    # en la elaboración de sus pizzas

    lista_ingredientes = []
    for ingrediente in ingredientes['ingredients']:
        varios = ingrediente.split(',')
        lista_ingredientes += varios

    set_ingredientes = set(lista_ingredientes)

    # Creamos una columna por cada ingrediente en detalles
    # Almacenamos en un diccionario el índice de cada ingrediente

    indices = dict()

    for i in set_ingredientes:
        detalles[i] = [0 for i in detalles.index]
        indice = detalles.columns.get_loc(i)
        indices[i] = indice

    # Para cada tipo de pizza en order detail, les sumamos
    # las cantidades a sus ingredientes correspondientes
    # Para las s sumaremos una unidad de cada ingrediente
    # Para las m sumaremos 2 y para las L sumaremos 3

    tipos_de_pizzas = pedidos['pizza_id'].tolist()
    tamanos = ['s', 'm', 'l', 'xl', 'xxl']
    ing_asociados = dict()

    for tipo in tipos_de_pizzas:

        tamano = tipo.split('_')[-1]
        ingredientes_str = ingredientes[ingredientes['pizza_type_id'] == tipo[:-len(tamano)-1]]['ingredients'].tolist()[0]
        lista_ingredientes_comprar = ingredientes_str.split(',')
        ing_asociados[tipo] = lista_ingredientes_comprar

    # Sumamos la cantidad de cada ingrediente que ha necesitado cada pedido

    for i in detalles.index:

        try:
            pedido = detalles['pizza_id'].iloc[i]
            cantidad = detalles['quantity'].iloc[i]
            ing = ing_asociados[pedido]
            tamano = pedido.split('_')[-1]

            for j in ing:
                detalles.loc[i, j] += cantidad * (tamanos.index(tamano) + 1)

        except:
            ...

    return detalles


def load_csv(datos):

    # El dataframe obtenido en el transform csv
    pass


def extract():

    # Extrae los datos finales ya trabajados de la pizería
    pass


def transform(datos):

    ingredientes = datos.columns.values
    ingredientes = ingredientes[6:]

    # Nuestro predict será la media de las modas de cada ingrediente

    suma_semana = datos.pivot_table(index='semana', aggfunc='sum')
    suma_semana_ingredientes = suma_semana[ingredientes]
    modas = suma_semana_ingredientes.mode().mean().round().tolist()

    # Creamos un dataframe con el valor calculado para cada ingrediente

    d = {'Ingredientes:': ingredientes, 'Unidades a comprar:': modas}
    res = pd.DataFrame(data=d)

    return res


def load(res, informe):

    # Guarda el resultado como un XML junto con el informe de datos

    root = ET.Element("Mavens_Pizza", name='Reporte')

    compra = ET.SubElement(root, 'categoria', nombre='Compra proxima semana')
    inf = ET.SubElement(root, 'informe', name='Informe de calidad de los Datos')

    for i in res.index:

        ingrediente = ET.SubElement(compra, "ingrediente", nombre=str(res.loc[i, 'Ingredientes:']))
        predict = ET.SubElement(ingrediente, "prediccion", cantidad=str(res.loc[i, 'Unidades a comprar:']))

    for key in informe:

        nombres_columnas = informe[key]['Nulls'].keys()
        df = ET.SubElement(inf, 'df', name=key)

        for column in nombres_columnas:

            columna = ET.SubElement(df, 'columna', name=column)
            nulls = ET.SubElement(columna, 'nulls', numero=str(informe[key]['Nulls'][column]))
            nans = ET.SubElement(columna, 'nans', numero=str(informe[key]['NaNs'][column]))
            tipos = ET.SubElement(columna, 'tipo', tipo=str(informe[key]['Tipos'][column]))

    ET.indent(root)
    arbol = ET.ElementTree(root)
    arbol.write("reporte.xml")


def informe_de_datos(fechas, pedidos, detalles, ingredientes):

    # Primero vemos el número de NaNs y de Nulls de cada df
    # Agregamos también el tipo de cada columna

    fichero = open('informe_calidad_datos.txt', 'w')
    informe = {}

    dfs = [fechas, pedidos, detalles, ingredientes]
    nombres = ['orders.csv', 'pizzas.csv', 'order_details.csv', 'pizza_types.csv']

    for df in range(len(dfs)):

        valores = {}

        null = {}
        nan = {}

        columnas = dfs[df].columns.values.tolist()

        tipos_columna = {}

        for c in columnas:

            tipos = dfs[df][c].dtypes
            nulls = dfs[df][c].isnull().sum()
            nans = dfs[df][c].isna().sum()

            tipos_columna[c] = tipos
            null[c] = nulls
            nan[c] = nans

        valores['Nulls'] = null
        valores['NaNs'] = nan
        valores['Tipos'] = tipos_columna

        informe[nombres[df]] = valores

    return informe


if __name__ == '__main__':

    fechas, pedidos, detalles, ingredientes, informe = extract_csv()
    datos = transform_csv(fechas, pedidos, detalles, ingredientes)
    res = transform(datos)
    load(res, informe)
