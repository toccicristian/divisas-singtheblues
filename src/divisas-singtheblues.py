#!/usr/bin/python3

import requests
import sys

ayuda=f"""
    obtiene de dolarapi.com los valores para una o todas las divisas especificadas.

    SINTAXIS:
        {sys.argv[0]} opcion
    opciones:
        --todas/-t          devuelve todas las divisas
        --csv/-c            devuelve los resultados en formato csv
                            (separador default ";", se puede especificar -c=,)

        oficial/blue/       devuelve las divisas especificadas
        bolsa/mayorista/
        contadoconliqui/
        cripto/tarjeta
"""

urlbase="https://dolarapi.com/v1/dolares"
dir=["oficial","blue","bolsa","contadoconliqui","tarjeta","mayorista","cripto"]


def existe_argumento(argumento):
    if len([arg for arg in sys.argv if arg==argumento])>0:
        return True
    return False

def argumento_comienza_con(cadena):
    if len([arg for arg in sys.argv if arg.lower().startswith(cadena.lower())])>0:
        return True
    return False


def extrae_valor_argumento(argumento, asignador="="):
    if not argumento.endswith(asignador):
        return False
    for arg in sys.argv:
        if arg.startswith(argumento):
            return arg.split(asignador)[1]


def formatea_casa(casa):
    sep=";"
    if argumento_comienza_con("-c="):
        separador=extrae_valor_argumento("-c=")
    if existe_argumento("--csv") or existe_argumento("-c") or argumento_comienza_con("-c="):
        return f"{casa['nombre']}{sep}{casa['compra']}{sep}{casa['venta']}{sep}{casa['fechaActualizacion']}"

    return f"{casa['nombre'].ljust(23)} Compra:{str(casa['compra']).rjust(8)} Venta:{str(casa['venta']).rjust(8)} Fecha de Actualizacion:{casa['fechaActualizacion'].rjust(24)}\n"

for argum in ["--help","--ayuda","-h"]:
    if existe_argumento(argum):
        print(f"{ayuda}")
        sys.exit()

response = requests.get(urlbase)
resultados=""
for casa in response.json():
    if existe_argumento(casa['casa']) or existe_argumento("-t") or existe_argumento("--todas") or len(sys.argv)==1:
        resultados=resultados+formatea_casa(casa)

print(resultados)

