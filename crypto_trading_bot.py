# -IMPORTACIÓN DE PAQUETES- #
import requests
import json
import hmac
import hashlib


# -FUNCIONES- #
def conector():
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    url: str = ""
    datos_conexion: str = ""
    datos_json: list = [""]

    # -ALGORITMO- #
    # Descripción General: Se conecta al servidor
    #                      Se obtienen todas las monedas del market con el ticker
    #                      Se devuelve una lista con un diccionario en su interior
    url = "https://openapi.bitmart.com/v2/ticker?symbol="
    try:
        datos_conexion = requests.request("GET", url)
        if datos_conexion.status_code == 200:
            print("200 - Conexión Al Servidor Realizada Con Éxito")
            datos_json = json.loads(datos_conexion.text)
        else:
            print("Fallo Conexión Al Servidor. Error: " + datos_conexion.status_code)
    except:
        print("Excepción: Fallo Conexión Al Servidor")  # Con esta except atrapo fallos como no hay conexión a internet

    return datos_json


def lista_reducida_ordenada(datos_json: list):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    simbolo_moneda: str = ""
    lista_reducida: list = [""]
    lista_ordenada: list = [""]  # Va a ser una lista que dentro va a tener diccionarios
    datos_json_reducido: dict = {
        'symbol_id': "",
        'base_volume': "",
        'current_price': "",
        'highest_price': "",
        'lowest_price': "",
        'fluctuation': ""
    }

    # -ALGORITMO- #
    # Descripción General: Recibe el ticker completo del servidor
    #                      Va a obtener solo las monedas que sean ETH
    #                      Se crea una nueva lista solo con las monedas ETH
    #                      Devuelve una lista ordenada de monedas ETH por el
    #                      mayor volumen operado de las ultimas 24hs
    #                      'symbol_id' sin formato
    #                      'base_volume' dos dígitos
    #                      'current_price' ocho dígitos
    #                      'highest_price' ocho dígitos
    #                      'lowest_price' ocho dígitos
    #                      'fluctuation' dos dígitos

    for i in datos_json:
        simbolo_moneda = i['symbol_id']
        if simbolo_moneda.find("_ETH") != -1:  # Solo para aquellas monedas que tengan en su nombre "_ETH"
            datos_json_reducido['symbol_id'] = i['symbol_id']
            datos_json_reducido['base_volume'] = float("{0:.2f}".format(float(i['base_volume'])))
            # Paso a float aca x q después con lambda no anda
            # Es la única forma que encontré que funcionara bien - float despues fomato dos decimales y float de nuevo
            datos_json_reducido['current_price'] = "{0:.8f}".format(float(i['current_price']))
            datos_json_reducido['highest_price'] = "{0:.8f}".format(float(i['highest_price']))
            datos_json_reducido['lowest_price'] = "{0:.8f}".format(float(i['lowest_price']))
            datos_json_reducido['fluctuation'] = "{0:.2f}".format(float(i['fluctuation']))
            lista_reducida.append(datos_json_reducido.copy())  # Se pasan los datos del json_reducido a una lista
    lista_reducida.pop(0)  # Se borra el primer elemento que es la inicialización de la variable
    lista_ordenada = sorted(lista_reducida, key=lambda dato: dato['base_volume'], reverse=True)

    return lista_ordenada


def obtener_primer_puesto(lista_ordenada: list):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    primer_puesto: list = [""]
    primer_puesto_a: dict = {}

    # -ALGORITMO- #
    # Descripción General: Obtiene el primer puesto y sus respectivos valores
    #                      primer_puesto obtiene un único elemento debido a q tenemos un diccionario dentro de la lista
    #                      primer_puesto_a obtiene el primer valor que es la moneda con los valores json_reducido
    #                      dos dígitos decimales para el volumen operado

    primer_puesto = lista_ordenada[:1]
    primer_puesto_a = primer_puesto[0]
    print(
        "La moneda con más volumen en las últimas 24hs es: "
        + primer_puesto_a['symbol_id']
        + ". Cuyo volumen operado es: "
        + str("{0:.2f}".format(primer_puesto_a['base_volume']))
        + " ETH"
    )

    return primer_puesto_a


def fluctuacion_porcentaje(valor_fluctuacion: float):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    fluctuacion_porcentaje: float = 0

    # -ALGORITMO- #
    # Descripción General: Devuelve la variación en porcentaje de la moneda
    #                      El valor de respuesta es en porcentaje y con dos decimales

    fluctuacion_porcentaje = "{0:.2f}".format(valor_fluctuacion * 100)
    if float(fluctuacion_porcentaje) < 0:
        print(
            "La variación es: "
            + str(fluctuacion_porcentaje)
            + " %. Negativo"
        )
    else:
        print(
            "La variación es: "
            + str(fluctuacion_porcentaje)
            + " %. Positivo"
        )
    # No sé porqué si le puse que diera dos valores decimales muestra solo un decimal
    # Al darle formato de dos decimales lo pasa a string, si justo ahí lo paso a float va a mostrar un solo decimal
    # Al hacer el print la variable fluctuacion_porcentaje es string no float
    return


def variacion_porcentaje_menor(valor_menor: float, valor_actual: float):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    # -VALORES INICIALES DE VARIABLES LOCALES- #
    # -ALGORITMO- #
    # Descripción General: Devuelve el valor del MENOR valor de la moneda en la moneda que le corresponde
    #                      Devuelve la variación del MENOR valor de la moneda en porcentaje
    #                      El valor de respuesta es en porcentaje y con dos decimales

    variable_temporal = (float(valor_menor) * 100) / float(valor_actual)
    variacion_porcentaje_menor = "{0:.2f}".format(variable_temporal - 100)
    print(
        "El valor más bajo es: "
        + str("{0:.8f}".format(valor_menor))
        + " ETH y representa el: "
        + str(variacion_porcentaje_menor)
        + "% del valor actual"
    )
    # Forzar los ocho decimales o los dos decimales según corresponda
    return


def variacion_porcentaje_mayor(valor_mayor: float, valor_actual: float):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    variable_temporal: float = 0
    variacion_porcentaje_mayor: float = 0

    # -ALGORITMO- #
    # Descripción General: Devuelve el valor del MAYOR valor de la moneda en la moneda que le corresponde
    #                      Devuelve la variación del MAYOR valor de la moneda en porcentaje
    #                      El valor de respuesta es en porcentaje y con dos decimales

    variable_temporal = (float(valor_mayor) * 100) / float(valor_actual)
    variacion_porcentaje_mayor = "{0:.2f}".format(variable_temporal - 100)
    print(
        "El valor más alto es: "
        + str("{0:.8f}".format(valor_mayor))
        + " ETH y representa el: "
        + str(variacion_porcentaje_mayor)
        + "% del valor actual"
    )
    return


def calcular_valor_de_compra(valor_menor_de_compra: float):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    # -VALORES INICIALES DE VARIABLES LOCALES- #
    # -ALGORITMO- #
    # Descripción General: Calcula el valor de compra de la moneda en cuestión
    #                      El porcentaje se establece acá, actualmente 65%
    #                      El valor debe ser con ocho valores decimales

    valor_de_compra = (valor_menor_de_compra * 65) / 100
    print(
        "El valor de compra sugerido es: "
        + str("{0:.8f}".format(valor_de_compra))
        + " que representa el 65 % del MENOR valor de compra actual"
    )
    # 2021.02.18 Volver a re pensar este algoritmo tiene que ser un porcentaje más real
    return


def calcular_valor_de_venta(valor_mayor_de_venta: float):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    # -VALORES INICIALES DE VARIABLES LOCALES- #
    # -ALGORITMO- #
    # Descripción General: Calcula el valor de venta de la moneda en cuestión
    #                      El porcentaje se establece acá, actualmente 65%
    #                      El valor debe ser con ocho valores decimales

    valor_de_venta = (valor_mayor_de_venta * 65) / 100
    print(
        "El valor de venta sugerido es: "
        + str("{0:.8f}".format(valor_de_venta))
        + " que representa el 65 % del MAYOR valor de compra actual"
    )
    # 2021.02.18 Volver a re pensar este algoritmo tiene que ser un porcentaje más real
    return


def validez_certificado():
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    f: str = ''
    mensaje: str = ''

    # -ALGORITMO- #
    # Descripción General: Devuelve la fecha de caducidad del certificado que permite realizar las transacciones

    f = open('./txt/vigencia-certificado.txt', 'r')
    mensaje = f.read()
    print("El certificado vence: " + str(mensaje) + " Faltan tantos días")
    f.close()

    # Falta que calcule cuántos días más restan
    # Tiene que estar sincronizado con la hora del servidor
    return


def valor_ethereum():
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    f: str = ''
    valor_ethereum: str = ''

    # -ALGORITMO- #
    # Descripción General: Devuelve el valor en dólares de la moneda Ethereum

    f = open('./txt/valor-ethereum.txt', 'r')
    valor_ethereum = f.read()
    print("La cotización actual de Ethereum es: " + str(valor_ethereum))
    f.close()
    # Este valor debo agregarlo a mano actualmente
    # Encontrar la forma de obtener este valor automáticamente
    # De paso aprovechar para usar un histórico del precio con valor y fecha en el txt donde se guarda la info
    # Acá hay que averiguar cómo leer solamente de la primera línea donde estaría el valor y la fecha
    # y de eso solamente el valor
    return valor_ethereum


def buys_sells(valor_actual: float, simbolo_id):
    # -DEFINICIÓN DE VARIABLES LOCALES- #

    buys_sells_lista_reducida: list = [""]
    buys_sells_datos_json_reducido: dict = {
        'amount': "",
        'total': "",
        'price': "",
        'count': "",
    }

    # -ALGORITMO- #
    # Descripción General: Esto lo hice para obtener información para generar mejor las ordenes de compra y venta
    #                      En la web la información de las ordenes que aparecen ocho a la venta y ocho a la compra
    #                      salen de este mismo json
    #                      buys_sells_datos_json es un diccionario que tiene tiene "buys" y tiene "sells" de la moneda
    #                      moneda en cuestión. Cada uno a su vez es una lista que tiene diccionarios con los valores
    #                      finales
    #                      En la web se muestran ocho para arriba y ocho para abajo podré posicionarme ahi, conviene?
    #                      EL Json ya viene ordenado por el precio de mayor a menor por lo que no es necesario mayores
    #                      modificaciones puedo tomar los primero ocho o dieciséis de la lista buys o sells
    #                      De acá puedo sacar un valor promedio de las cantidades ofrecidas de la moneda en cuestión
    #                      De acá puedo sacar los ocho o los dieciséis valores que aparecen en la web

    url = "https://openapi.bitmart.com/v2/symbols/" + simbolo_id + "/orders?precision=8"
    #   Ver bien el tipo de dato que recibe la url, lo pasé así nomas
    buys_sells_datos_basicos = requests.request("GET", url)
    if buys_sells_datos_basicos.status_code != 200:
        print("Falló la consulta con precisión de 8 dígitos intentando con 6")
        # print("El código en buys sells es: " + str(buys_sells_datos_basicos.status_code))
        url = "https://openapi.bitmart.com/v2/symbols/" + simbolo_id + "/orders?precision=6"
        buys_sells_datos_basicos = requests.request("GET", url)
        if buys_sells_datos_basicos.status_code != 200:
            print("Falló la consulta con precisión de 6 dígitos intentando con 4")
            # print("El código en buys sells es: " + str(buys_sells_datos_basicos.status_code))
            url = "https://openapi.bitmart.com/v2/symbols/" + simbolo_id + "/orders?precision=4"
            buys_sells_datos_basicos = requests.request("GET", url)
    buys_sells_datos_json = json.loads(buys_sells_datos_basicos.text)

    # 2021.02.18 con el simbolo_id primero tengo que consultar la cantidad de decimales que permite la moneda
    # Luego recién ahí meter la precisión en la URL
    # Me tira un error "Invalid precision. Precision must be in the range 2,4 investigar la API a ver qué es
    return buys_sells_datos_json


def buys(buys_sells_datos_json):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    # -VALORES INICIALES DE VARIABLES LOCALES- #
    # -ALGORITMO- #
    # Descripción General: Recibe el json que contiene los valores de buys y sell de la moneda en cuestión
    #                      Va a mostrar las ocho primeras ofertar para comprar la moneda en cuestión
    #                      Va a mostrar en porcentaje el valor en referencia a la cotización del momento
    #                      Va a mostrar el valor promedio de las cantidades de las monedas que se ofrecen
    #                      Esta información va a servir para hacer una oferta que aparezca entre los primeros 8
    for i in buys_sells_datos_json:
        if i == "buys":
            print("- BUYS (Verde) -")

            buys_precio_8vo_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][7]['price']))
            buys_porcentaje_8vo_puesto = "{0:.2f}".format(
                (float(buys_precio_8vo_puesto) * 100) / float(valor_actual) - 100)
            print("El 8vo puesto tiene un valor de :" + buys_precio_8vo_puesto + " Representa: " + str(
                buys_porcentaje_8vo_puesto) + "% del valor actual de la moneda")

            buys_precio_7mo_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][6]['price']))
            buys_porcentaje_7mo_puesto = "{0:.2f}".format(
                (float(buys_precio_7mo_puesto) * 100) / float(valor_actual) - 100)
            print("El 7mo puesto tiene un valor de :" + buys_precio_7mo_puesto + " Representa: " + str(
                buys_porcentaje_7mo_puesto) + "% del valor actual de la moneda")

            buys_precio_6to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][5]['price']))
            buys_porcentaje_6to_puesto = "{0:.2f}".format(
                (float(buys_precio_6to_puesto) * 100) / float(valor_actual) - 100)
            print("El 6to puesto tiene un valor de :" + buys_precio_6to_puesto + " Representa: " + str(
                buys_porcentaje_6to_puesto) + "% del valor actual de la moneda")

            buys_precio_5to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][4]['price']))
            buys_porcentaje_5to_puesto = "{0:.2f}".format(
                (float(buys_precio_5to_puesto) * 100) / float(valor_actual) - 100)
            print("El 5to puesto tiene un valor de :" + buys_precio_5to_puesto + " Representa: " + str(
                buys_porcentaje_5to_puesto) + "% del valor actual de la moneda")

            buys_precio_4to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][3]['price']))
            buys_porcentaje_4to_puesto = "{0:.2f}".format(
                (float(buys_precio_4to_puesto) * 100) / float(valor_actual) - 100)
            print("El 4to puesto tiene un valor de :" + buys_precio_4to_puesto + " Representa: " + str(
                buys_porcentaje_4to_puesto) + "% del valor actual de la moneda")

            buys_precio_3er_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][2]['price']))
            buys_porcentaje_3er_puesto = "{0:.2f}".format(
                (float(buys_precio_3er_puesto) * 100) / float(valor_actual) - 100)
            print("El 3er puesto tiene un valor de :" + buys_precio_3er_puesto + " Representa: " + str(
                buys_porcentaje_3er_puesto) + "% del valor actual de la moneda")

            buys_precio_2do_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][1]['price']))
            buys_porcentaje_2do_puesto = "{0:.2f}".format(
                (float(buys_precio_2do_puesto) * 100) / float(valor_actual) - 100)
            print("El 2do puesto tiene un valor de :" + buys_precio_2do_puesto + " Representa: " + str(
                buys_porcentaje_2do_puesto) + "% del valor actual de la moneda")

            buys_precio_1er_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][0]['price']))
            buys_porcentaje_1er_puesto = "{0:.2f}".format(
                (float(buys_precio_1er_puesto) * 100) / float(valor_actual) - 100)
            print("El 1er puesto tiene un valor de :" + buys_precio_1er_puesto + " Representa: " + str(
                buys_porcentaje_1er_puesto) + "% del valor actual de la moneda")

            valor_8_buys = float(buys_sells_datos_json['buys'][7]['amount'])
            valor_7_buys = float(buys_sells_datos_json['buys'][6]['amount'])
            valor_6_buys = float(buys_sells_datos_json['buys'][5]['amount'])
            valor_5_buys = float(buys_sells_datos_json['buys'][4]['amount'])
            valor_4_buys = float(buys_sells_datos_json['buys'][3]['amount'])
            valor_3_buys = float(buys_sells_datos_json['buys'][2]['amount'])
            valor_2_buys = float(buys_sells_datos_json['buys'][1]['amount'])
            valor_1_buys = float(buys_sells_datos_json['buys'][0]['amount'])
            resultado_buys = (valor_8_buys
                              +
                              valor_7_buys
                              +
                              valor_6_buys
                              +
                              valor_5_buys
                              +
                              valor_4_buys
                              +
                              valor_3_buys
                              +
                              valor_2_buys
                              +
                              valor_1_buys
                              ) / 8
            print("El promedio de moneda para comprar es de: " + str("{0:.2f}".format(resultado_buys)))

    # 2021.02.18 En la última parte tendría que validar de descartar el valor más alto y el más bajo
    # para sacar un mejor promedio
    return


def sells(buys_sells_datos_json):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    # -VALORES INICIALES DE VARIABLES LOCALES- #
    # -ALGORITMO- #
    # Descripción General: Recibe el json que contiene los valores de buys y sell de la moneda en cuestión
    #                      Va a mostrar las ocho primeras ofertar para vender la moneda en cuestión
    #                      Va a mostrar en porcentaje el valor en referencia a la cotización del momento
    #                      Va a mostrar el valor promedio de las cantidades de las monedas que se ofrecen
    #                      Esta información va a servir para hacer una oferta que aparezca entre los primeros 8
    for i in buys_sells_datos_json:
        if i == "sells":
            print("- SELLS (Rojo) -")
            sells_precio_8vo_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][7]['price']))
            sells_porcentaje_8vo_puesto = "{0:.2f}".format(
                (float(sells_precio_8vo_puesto) * 100) / float(valor_actual) - 100)
            print("El 8vo puesto tiene un valor de :" + sells_precio_8vo_puesto + " Representa: " + str(
                sells_porcentaje_8vo_puesto) + "% del valor actual de la moneda")

            sells_precio_7mo_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][6]['price']))
            sells_porcentaje_7mo_puesto = "{0:.2f}".format(
                (float(sells_precio_7mo_puesto) * 100) / float(valor_actual) - 100)
            print("El 7mo puesto tiene un valor de :" + sells_precio_7mo_puesto + " Representa: " + str(
                sells_porcentaje_7mo_puesto) + "% del valor actual de la moneda")

            sells_precio_6to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][5]['price']))
            sells_porcentaje_6to_puesto = "{0:.2f}".format(
                (float(sells_precio_6to_puesto) * 100) / float(valor_actual) - 100)
            print("El 6to puesto tiene un valor de :" + sells_precio_6to_puesto + " Representa: " + str(
                sells_porcentaje_6to_puesto) + "% del valor actual de la moneda")

            sells_precio_5to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][4]['price']))
            sells_porcentaje_5to_puesto = "{0:.2f}".format(
                (float(sells_precio_5to_puesto) * 100) / float(valor_actual) - 100)
            print("El 5to puesto tiene un valor de :" + sells_precio_5to_puesto + " Representa: " + str(
                sells_porcentaje_5to_puesto) + "% del valor actual de la moneda")

            sells_precio_4to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][3]['price']))
            sells_porcentaje_4to_puesto = "{0:.2f}".format(
                (float(sells_precio_4to_puesto) * 100) / float(valor_actual) - 100)
            print("El 4to puesto tiene un valor de :" + sells_precio_4to_puesto + " Representa: " + str(
                sells_porcentaje_4to_puesto) + "% del valor actual de la moneda")

            sells_precio_3er_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][2]['price']))
            sells_porcentaje_3er_puesto = "{0:.2f}".format(
                (float(sells_precio_3er_puesto) * 100) / float(valor_actual) - 100)
            print("El 3er puesto tiene un valor de :" + sells_precio_3er_puesto + " Representa: " + str(
                sells_porcentaje_3er_puesto) + "% del valor actual de la moneda")

            sells_precio_2do_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][1]['price']))
            sells_porcentaje_2do_puesto = "{0:.2f}".format(
                (float(sells_precio_2do_puesto) * 100) / float(valor_actual) - 100)
            print("El 2do puesto tiene un valor de :" + sells_precio_2do_puesto + " Representa: " + str(
                sells_porcentaje_2do_puesto) + "% del valor actual de la moneda")

            sells_precio_1er_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][0]['price']))
            sells_porcentaje_1er_puesto = "{0:.2f}".format(
                (float(sells_precio_1er_puesto) * 100) / float(valor_actual) - 100)
            print("El 1er puesto tiene un valor de :" + sells_precio_1er_puesto + " Representa: " + str(
                sells_porcentaje_1er_puesto) + "% del valor actual de la moneda")

            valor_8_sells = float(buys_sells_datos_json['sells'][7]['amount'])
            valor_7_sells = float(buys_sells_datos_json['sells'][6]['amount'])
            valor_6_sells = float(buys_sells_datos_json['sells'][5]['amount'])
            valor_5_sells = float(buys_sells_datos_json['sells'][4]['amount'])
            valor_4_sells = float(buys_sells_datos_json['sells'][3]['amount'])
            valor_3_sells = float(buys_sells_datos_json['sells'][2]['amount'])
            valor_2_sells = float(buys_sells_datos_json['sells'][1]['amount'])
            valor_1_sells = float(buys_sells_datos_json['sells'][0]['amount'])

            # Cargar esos valores en una lista
            # Buscar el maximo y el mínimo y borrarlos
            lista = [0, 1, 2, 3, 4, 5, 6, 7]
            for i in lista:
                # 2021.02.19 Esta poronga del for no lo entiendo
                # Querìa que el i se moviera con los valores de la posición de la lista y no pude
                # Se mueve por el valor que tiene adentro la lista por eso va del cero al siete
                lista[i] = float(buys_sells_datos_json['sells'][i]['amount'])
            indice_mayor_valor = lista.index(max(lista))
            indice_menor_valor = lista.index(min(lista))
            indice_menor = int(indice_menor_valor) - 1
            print(lista)
            del (lista[indice_mayor_valor])  # Que pasa si hay dos valores iguales? - Rta: Explota
            del (lista[indice_menor])  # Que pasa si hay dos valores iguales?
            # print(lista.index(max(lista)))
            print(lista)
            promedio = float(sum(lista)) / float(len(lista))
            print("El promedio de moneda para vender es de: " + str("{0:.2f}".format(promedio)))
            # 2021.02.19 Creo que puedo tomar los 10 primeros valores y borrar dos veces los valores mayores y menores
            """
            resultado_sells = (
                               valor_8_sells
                               +
                               valor_7_sells
                               +
                               valor_6_sells
                               +
                               valor_5_sells
                               +
                               valor_4_sells
                               +
                               valor_3_sells
                               +
                               valor_2_sells
                               +
                               valor_1_sells
                               ) / 8
            print("El promedio de moneda para vender es de: " + str("{0:.2f}".format(resultado_sells)))
            """

    # 2021.02.18 En la última parte tendría que validar de descartar el valor más alto y el más bajo
    # para sacar un mejor promedio

    # 2020.11.24 Tengo que capturar el valor puntual de "price" para saber la diferencia con el valor de cotización
    # Tengo que capturar el valor puntual de "amount / total" para saber la cantidad que conviene
    # Porqué aparecen cantidades con decimales en la web, no era que solo se pueden ofrecer cantidades enteras?
    # Una vez que tengo la diferencia en porcentual verificar si genera ganancia

    # Esto me sirve. De aca tengo que sacar el promedio de las cantidades ofrecidas
    # Puedo sacar los porcentajes de ganancia de cada puesto
    return


def diferencias_porcentuales_buys_cells(buys_sells_datos_json):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    # Completar faltan todas las variables

    # -VALORES INICIALES DE VARIABLES LOCALES- #
    # Completar faltan todas las variables

    # -ALGORITMO- #
    # Descripción General: Esto lo hice para obtener información para generar mejor las ordenes de compra y venta
    #                      En la web la información de las ordenes que aparecen ocho a la venta y ocho a la compra
    #                      salen de este mismo json
    #                      buys_sells_datos_json es un diccionario que tiene tiene "buys" y tiene "sells" de la moneda
    #                      moneda en cuestión. Cada uno a su vez es una lista que tiene diccionarios con los valores
    #                      finales
    #                      En la web se muestran ocho para arriba y ocho para abajo podré posicionarme ahi, conviene?
    #                      EL Json ya viene ordenado por el precio de mayor a menor por lo que no es necesario mayores
    #                      modificaciones puedo tomar los primero ocho o dieciséis de la lista buys o sells
    #                      De acá puedo sacar un valor promedio de las cantidades ofrecidas de la moneda en cuestión
    #                      De acá puedo sacar los ocho o los dieciséis valores que aparecen en la web

    for i in buys_sells_datos_json:
        if i == "buys":
            buys_precio_8vo_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][7]['price']))
            buys_porcentaje_8vo_puesto = "{0:.2f}".format(
                (float(buys_precio_8vo_puesto) * 100) / float(valor_actual) - 100)

            buys_precio_7mo_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][6]['price']))
            buys_porcentaje_7mo_puesto = "{0:.2f}".format(
                (float(buys_precio_7mo_puesto) * 100) / float(valor_actual) - 100)

            buys_precio_6to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][5]['price']))
            buys_porcentaje_6to_puesto = "{0:.2f}".format(
                (float(buys_precio_6to_puesto) * 100) / float(valor_actual) - 100)

            buys_precio_5to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][4]['price']))
            buys_porcentaje_5to_puesto = "{0:.2f}".format(
                (float(buys_precio_5to_puesto) * 100) / float(valor_actual) - 100)

            buys_precio_4to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][3]['price']))
            buys_porcentaje_4to_puesto = "{0:.2f}".format(
                (float(buys_precio_4to_puesto) * 100) / float(valor_actual) - 100)

            buys_precio_3er_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][2]['price']))
            buys_porcentaje_3er_puesto = "{0:.2f}".format(
                (float(buys_precio_3er_puesto) * 100) / float(valor_actual) - 100)

            buys_precio_2do_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][1]['price']))
            buys_porcentaje_2do_puesto = "{0:.2f}".format(
                (float(buys_precio_2do_puesto) * 100) / float(valor_actual) - 100)

            buys_precio_1er_puesto = "{0:.8f}".format(float(buys_sells_datos_json['buys'][0]['price']))
            buys_porcentaje_1er_puesto = "{0:.2f}".format(
                (float(buys_precio_1er_puesto) * 100) / float(valor_actual) - 100)
        if i == "sells":
            sells_precio_8vo_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][7]['price']))
            sells_porcentaje_8vo_puesto = "{0:.2f}".format(
                (float(sells_precio_8vo_puesto) * 100) / float(valor_actual) - 100)

            sells_precio_7mo_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][6]['price']))
            sells_porcentaje_7mo_puesto = "{0:.2f}".format(
                (float(sells_precio_7mo_puesto) * 100) / float(valor_actual) - 100)

            sells_precio_6to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][5]['price']))
            sells_porcentaje_6to_puesto = "{0:.2f}".format(
                (float(sells_precio_6to_puesto) * 100) / float(valor_actual) - 100)

            sells_precio_5to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][4]['price']))
            sells_porcentaje_5to_puesto = "{0:.2f}".format(
                (float(sells_precio_5to_puesto) * 100) / float(valor_actual) - 100)

            sells_precio_4to_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][3]['price']))
            sells_porcentaje_4to_puesto = "{0:.2f}".format(
                (float(sells_precio_4to_puesto) * 100) / float(valor_actual) - 100)

            sells_precio_3er_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][2]['price']))
            sells_porcentaje_3er_puesto = "{0:.2f}".format(
                (float(sells_precio_3er_puesto) * 100) / float(valor_actual) - 100)

            sells_precio_2do_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][1]['price']))
            sells_porcentaje_2do_puesto = "{0:.2f}".format(
                (float(sells_precio_2do_puesto) * 100) / float(valor_actual) - 100)

            sells_precio_1er_puesto = "{0:.8f}".format(float(buys_sells_datos_json['sells'][0]['price']))
            sells_porcentaje_1er_puesto = "{0:.2f}".format(
                (float(sells_precio_1er_puesto) * 100) / float(valor_actual) - 100)

            print("- Diferencias porcentuales buys - sells")
            variable_temporal_8vo = float(buys_porcentaje_8vo_puesto) * -1

            print("La diferencia del 8vo puesto de compra al 8vo puesto de venta es de "
                  + str("{0:.2f}".format(variable_temporal_8vo + float(sells_porcentaje_8vo_puesto)))
                  + "%"
                  )

            variable_temporal_7mo = float(buys_porcentaje_7mo_puesto) * -1

            print("La diferencia del 7mo puesto de compra al 7mo puesto de venta es de "
                  + str("{0:.2f}".format(variable_temporal_7mo + float(sells_porcentaje_7mo_puesto)))
                  + "%"
                  )

            variable_temporal_6to = float(buys_porcentaje_6to_puesto) * -1

            print("La diferencia del 6to puesto de compra al 6to puesto de venta es de "
                  + str("{0:.2f}".format(variable_temporal_6to + float(sells_porcentaje_6to_puesto)))
                  + "%"
                  )

            variable_temporal_5to = float(buys_porcentaje_5to_puesto) * -1

            print("La diferencia del 5to puesto de compra al 5to puesto de venta es de "
                  + str("{0:.2f}".format(variable_temporal_5to + float(sells_porcentaje_5to_puesto)))
                  + "%"
                  )

            variable_temporal_4to = float(buys_porcentaje_4to_puesto) * -1

            print("La diferencia del 4to puesto de compra al 4to puesto de venta es de "
                  + str("{0:.2f}".format(variable_temporal_4to + float(sells_porcentaje_4to_puesto)))
                  + "%"
                  )

    # 2021.02.18 No sé porqué hice solo hasta el 4to puesto
    # No sé porqué la última parte de este código tiene que estar dentro del "if" de sell para funcionar
    return


def valor_historico_moneda(symbol_id: str, valor_mayor: float, valor_menor: float):
    # -DEFINICIÓN DE VARIABLES LOCALES- #
    url = str
    datos_conexion = str
    datos_json = list
    f = str
    #    valor_historico_moneda = dict
    # -VALORES INICIALES DE VARIABLES LOCALES- #
    url = ""
    datos_conexion = ""
    datos_json = [""]
    f = ''
    valor = {}
    valor['historico_moneda'] = []

    #    valor = {
    #        'symbol_id': "",
    #        'date': "",
    #        'highest_price': "",
    #        'lowest_price': "",
    #    }
    # -ALGORITMO- #
    # Descripción General: Guarda en un txt el mayor y menor valor de la moneda
    #                      Los valores symbol_id highest_price y loewst_price vienen de otras consultas
    #                      Se realiza la consulta de la hora del servidor para almacenar ese dato

    url = "https://openapi.bitmart.com/v2/time"
    datos_conexion = requests.request("GET", url)
    datos_json = json.loads(datos_conexion.text)
    server_time = datos_json['server_time']

    valor['historico_moneda'].append("{'symbol_id':'" + str(symbol_id) + "'," + "'date':'" + str(
        server_time) + "'," + "'highest_price':'" + str(valor_mayor) + "'," + "'lowest_price':'" + str(
        valor_menor) + "'" + "}")

    with open('./txt/valor-historico-mayor-menor.txt', 'a') as f:
        json.dump(valor['historico_moneda'], f)

    # 2020.12.01 Ahora anda, pero sobre escribe todo el archivo falta que guarde lo que tiene y luego
    # guarde todo junto

    # 2020.11.30 Lo que puedo intentar es tomar el contenido del txt guardarlo en una variable
    # luego levantar el nuevo texto y concatenar el nuevo texto con el viejo
    # y finalmente volver a escribir el txt con todo el texto nuevo y viejo

    # Ver bien la sintaxis del json que aca se arma. En algunos casos lleva coma en otros no
    # También muy importante el cierre de paréntesis y de llaves y corchetes ojo con eso

    # De paso aprovechar para usar un histórico del precio con valor y fecha en el txt donde se guarda la info
    # Acá hay que averiguar cómo leer solamente de la primera línea donde estaría el valor y la fecha
    # y de eso solamente el valor

    # Voy a tener que crear un histórico para cada moneda. En este caso empiezo a trabajar con la moneda que mas
    # volumen de operaciones tiene, pero luego serán diferentes monedas y eso me obligará a crear diferentes
    # archivos para cada moneda a menos que aprenda a manipular los archivos de texto y guarde todo en un solo
    # archivo txt
    # pienso en algo como  Nombre_Moneda fecha valor mayor valor menor
    # con esos campos luego puedo hacer los cálculos necesarios
    # o crear mi propio json con esa info que sea guardada en el txt y luego la pueda cargar y manipular
    return


def create_sha256_signature():
    # Esto sirve para crear la primera firma que permite realizar las transacciones restringidas en el servidor
    # la acces_key del sitio web en el código es la api_key

    f = open('./txt/aut_api_key.txt', 'r')
    api_key = f.read()
    f.close()

    f = open('./txt/aut_secret_key.txt', 'r')
    secret_key = f.read()
    f.close()

    f = open('./txt/aut_memo.txt', 'r')
    memo = f.read()
    f.close()

    mensaje = api_key + ':' + secret_key + ':' + memo

    firma = hmac.new(secret_key.encode('utf-8'), mensaje.encode('utf-8'), hashlib.sha256).hexdigest()
    print(firma)

    # 2021.11.17 Hacer que se guarde en un archivo txt
    return


def create_sha256_signature(timestamp, query_string):
    # -ALGORITMO- #
    # Descripción General: Sirve para crear la firma para realizar compra venta de criptos
    #                      Es utilizada por la función "place_sell_order()"

    f = open('./txt/aut_memo.txt', 'r')
    memo = f.read()
    f.close()

    f = open('./txt/aut_secret_key.txt', 'r')
    secret_key = f.read()
    f.close()

    mensaje = timestamp + "#" + memo + "#" + str(query_string)

    digest = hmac.new(secret_key.encode('UTF-8'),
                      mensaje.encode('UTF-8'), hashlib.sha256)

    firma = digest.hexdigest()
    print(firma)

    return firma


def access_token():
    # la acces_key del sitio web en el código es la api_key

    f = open('./txt/aut_api_key.txt', 'r')
    api_key = f.read()
    f.close()

    f = open('./txt/aut_signature.txt', 'r')
    firma = f.read()
    f.close()

    url = "https://openapi.bitmart.com/v2/authentication"

    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": firma
    }

    response = requests.post(url, data=data)
    print(response.content)

    return


def wallet():
    # Se hace la consulta a la billetera para conocer la disponibilidad de criptos
    # la acces_key del sitio web en el código es la api_key

    url = "https://api-cloud.bitmart.com/account/v1/wallet?account_type=1"

    f = open('./txt/aut_api_key.txt', 'r')
    api_key = f.read()
    f.close()

    data = {
        "Content-Type": "application/json",
        "X-BM-KEY": api_key
    }

    response = requests.get(url, headers=data)

    print(response.status_code)
    print(response.content)

    return


def place_sell_order():
    # La hora del servidor la resolví tomando la hora del mismo server y poniendo esa hora en la petición
    # Lo resolví asi porque me pareció lo más práctico la demora de la consulta del servidor seria de segundos
    # El servidor va a tener tolerancia de hasta un minuto, o sea es un montón de tiempo a mi favor en este caso

    url_hora = "https://api-cloud.bitmart.com/system/time"
    s = requests.request("GET", url_hora)
    s_json = json.loads(s.text)

    hora = str(s_json['data']['server_time'])

    data = {
        "symbol": "TRX_ETH",
        "side": "sell",
        "type": "limit",
        "size": "49",
        "price": "0.00002590"
    }
    data_txt = json.dumps(data)
    print(data_txt)
    #        "amount": amount, Este valor asi como se ve no aparece debe ser el size
    firma = create_sha256_signature(hora, data_txt)

    url = "https://api-cloud.bitmart.com/spot/v1/submit_order"

    f = open('./txt/aut_api_key.txt', 'r')
    api_key = f.read()
    f.close()

    headers = {
        "Content-Type": "application/json",
        "X-BM-TIMESTAMP": hora,
        "X-BM-KEY": api_key,
        "X-BM-SIGN": firma
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.content)
    print(response.status_code)

    # 2021.11.17 Los datos para realizar la compra están harcodeados. Arreglar
    return


if __name__ == '__main__':
    # -DEFINICIÓN DE VARIABLES#
    datos_json: list = [""]
    lista_ordenada: list = ""
    primer_puesto: dict = {
        'symbol_id': "",
        'base_volume': "",
        'current_price': "",
        'highest_price': "",
        'lowest_price': "",
        'fluctuation': ""
    }
    valor_fluctuacion: float = 0
    valor_actual: float = 0
    valor_menor: float = 0
    valor_mayor: float = 0

    while True:
        seleccion = int(input("""
         ====================================
        |  0 - Conectarse                    |
        |  1 - Cotización Ethereum           |
        |  2 - Ticker                        |
        |  3 - Comprar                       |
        |  4 - Vender                        |
        |  5 - Consultar Billetera           |
        |  6 - Consultar Validez Certificado |
        |  7 - Crear Firma                   |
        |  8 - Salir                         |
         ====================================
        """))

        if seleccion == 0:  # Conectarse
            datos_json = conector()  # Obtiene el ticker
        elif seleccion == 1:  # Cotización Ethereum
            valor_ethereum()
        elif seleccion == 2:  # Ticker
            # Obtener Ticker y la moneda con más volumen de operación de las ú1ltimas 24hs
            datos_json = conector()  # Obtiene el ticker

            # Obtiene lista todas las monedas ETH con mayor volumen 24hs
            lista_ordenada = lista_reducida_ordenada(datos_json)

            # Obtiene el primer puesto de las monedas ETH con mayor vol24hs
            primer_puesto_a = obtener_primer_puesto(lista_ordenada)

        elif seleccion == 3:  # Comprar
            pass
        elif seleccion == 4:  # Vender
            # place_sell_order()
            # Ojo con esto ver que esté bien antes de hacer el place sell order
            # Lo que está ahora está hardcodeado... pero funciona!
            pass
        elif seleccion == 5:  # Consultar Billetera
            wallet()
        elif seleccion == 6:  # Consultar Validez Certificado
            validez_certificado()
        elif seleccion == 7:  # Crear Firma
            # create_sha256_signature()
            pass
        elif seleccion == 8:  # Salir
            break

    # valor_fluctuacion = float(primer_puesto_a['fluctuation'])
    # valor_actual = float(primer_puesto_a['current_price'])
    # valor_menor = float(primer_puesto_a['lowest_price'])
    # valor_mayor = float(primer_puesto_a['highest_price'])
    # symbol_id = primer_puesto_a['symbol_id']

    # Calculos varios
    # Todos estos cálculos son solo para esta moneda que es la que mayor volumen operó en las últimas 24hs

    # fluctuacion_porcentaje(valor_fluctuacion)  # Muestra la variación en porcentaje de la moneda
    # print("El valor actual es: " + str("{0:.8f}".format(valor_actual)) + " ETH")
    # variacion_porcentaje_menor(valor_menor, valor_actual)  # Muestra el menor valor y el porcentaje del valor actual
    # variacion_porcentaje_mayor(valor_mayor, valor_actual)  # Muestra el mayor valor y el porcentaje del valor actual
    # calcular_valor_de_compra(valor_menor) # 2021.02.18 Mejorar este algoritmo
    # calcular_valor_de_venta(valor_mayor) # 2021.02.18 Mejorar este algoritmo

    # Estas cuatro funciones funcionan todas dependiendo del JSON que trae la primera
    # 2021.02.18 Hasta el momento la falla principal parece ser la cantidad de decimales que permite la moneda

    # buys_sells_datos_json = buys_sells(valor_actual, symbol_id)
    # buys(buys_sells_datos_json)
    # sells(buys_sells_datos_json)
    # diferencias_porcentuales_buys_cells(buys_sells_datos_json) # Revisar el funcionamiento, solo trajo del 8vo al 4to

    # valor_historico_moneda(symbol_id, valor_mayor, valor_menor)
    # print("El valor en dólares para comprar sería: " + valor_ethereum() * )

    # access_token() #Este lo hice andar una sola vez, ver cuándo haría falta hacerlo andar
