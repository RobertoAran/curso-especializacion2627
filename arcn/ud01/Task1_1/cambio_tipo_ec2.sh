#!/usr/bin/env bash

# Autor/a: Roberto Aranda Lopez
# Fecha: 21/10/2026
# Uso: cambia_tipo_ec2.sh [-y] ID_INSTANCIA TIPO_NUEVO

set -uo pipefail
export AWS_PAGER=""

PROPIETARIO="RobertoA"
FILTERJSONDESCINST="Reservations[0].Instances[0]"

exit_error_report() {
echo "ERROR: $1" >&2
exit "$2"
}

uso() {
echo "Uso: $(basename "$0") [-y] ID_INSTANCIA TIPO_NUEVO" >&2
exit 1
}

[ $# -eq 2 ] || uso
ID=$1
TYPE=$2

take_limits() {
    IFS='.' read -r generation weight <<< "$TYPE"

    case "$generation" in t1|t2) ;;
        *) exit_error_report "Error 5 - tipo de generacion no valida" 5 ;;
    esac

    case "$weight" in nano|micro|small|medium|large) ;; 
        *) exit_error_report "Error 5 - peso no valido" 5 ;;
    esac
}

#Comienzo script

take_limits