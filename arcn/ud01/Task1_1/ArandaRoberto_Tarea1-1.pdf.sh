#!/usr/bin/env bash

# Autor/a: Roberto Aranda Lopez
# Fecha: 21/10/2026
# Uso: cambia_tipo_ec2.sh [-y] ID_INSTANCIA TIPO_NUEVO

set -uo pipefail
export AWS_PAGER=""
export AWS_DEFAULT_REGION="us-east-1"

ETIQUETA="Propietario"
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

validar_tipo() {
    local generation size
    IFS='.' read -r generation size <<< "$TYPE"

    case "$generation" in
        t2|t3) ;;
        *) exit_error_report "generacion '$generation' no valida (t2 o t3)" 5 ;;
    esac

    case "$size" in
        nano|micro|small|medium|large) ;;
        *) exit_error_report "tamano '$size' no valido (nano, micro, small, medium o large)" 5 ;;
    esac
}

obtener_info() {
    local info
    info=$(aws ec2 describe-instances --instance-ids "$ID" \
    --query "${FILTERJSONDESCINST}.[State.Name, InstanceType, Tags[?Key=='$ETIQUETA']|[0].Value]" \
    --output text) || exit_error_report "la instancia $ID no existe o no es accesible" 2

    [ -n "$info" ] && [ "$info" != "None" ] || exit_error_report "la instancia $ID no existe o no es accesible" 2

    read -r ESTADO TIPO_ACTUAL DUENO <<< "$info"
}

comprobar_instancia() {
    [ "$DUENO" = "$PROPIETARIO" ] || exit_error_report "la instancia $ID no tiene la etiqueta $ETIQUETA=$PROPIETARIO" 3

    case "$ESTADO" in
        terminated|shutting-down) exit_error_report "la instancia $ID esta en estado '$ESTADO'" 4 ;;
    esac

    if [ "$TIPO_ACTUAL" = "$TYPE" ]; then
        echo "La instancia $ID ya es de tipo $TYPE, no hay nada que hacer"
        exit 0
    fi
}

confirmar_cambio() {
    local respuesta
    echo "Instancia: $ID | Estado: $ESTADO | Tipo: $TIPO_ACTUAL -> $TYPE"

    [ "$CONFIRMAR" -eq 1 ] || return 0

    read -r -p "La instancia se detendra. ¿Confirmas el cambio? [s/N]: " respuesta
    case "$respuesta" in
        s|S|si|SI|Si) ;;
        *) echo "Cancelado por el usuario"; exit 6 ;;
    esac
}

detener_instancia() {
    local inicio
    T_STOP=0

    case "$ESTADO" in
        running|pending)
            echo "Deteniendo la instancia..."
            inicio=$(date +%s)
            aws ec2 stop-instances --instance-ids "$ID" > /dev/null || exit_error_report "AWS fallo al detener la instancia" 7
            ;;
        stopping)
            echo "La instancia ya se esta deteniendo, esperando..."
            inicio=$(date +%s)
            ;;
        *) return 0 ;;
    esac

    aws ec2 wait instance-stopped --instance-ids "$ID" || exit_error_report "AWS fallo esperando a que se detenga" 7
    T_STOP=$(( $(date +%s) - inicio ))
}

cambiar_tipo() {
    echo "Cambiando el tipo a $TYPE..."
    aws ec2 modify-instance-attribute --instance-id "$ID" \
        --instance-type Value="$TYPE" || exit_error_report "AWS fallo al cambiar el tipo" 7
}

arrancar_instancia() {
    local inicio
    echo "Arrancando la instancia..."
    inicio=$(date +%s)
    aws ec2 start-instances --instance-ids "$ID" > /dev/null || exit_error_report "AWS fallo al arrancar la instancia" 7
    aws ec2 wait instance-running --instance-ids "$ID" || exit_error_report "AWS fallo esperando a que arranque" 7
    T_START=$(( $(date +%s) - inicio ))
}

mostrar_tiempos() {
    echo "------------------------------------------"
    echo "Cambio completado: $ID ahora es $TYPE"
    echo "Tiempo en detenerse: ${T_STOP}s"
    echo "Tiempo en arrancar:  ${T_START}s"
    echo "------------------------------------------"
}

# Comienzo script

CONFIRMAR=1
while getopts ":y" opt; do
    case "$opt" in
        y) CONFIRMAR=0 ;;
        *) echo "ERROR: opcion desconocida -$OPTARG" >&2; uso ;;
    esac
done
shift $((OPTIND - 1))

[ $# -eq 2 ] || uso
ID=$1
TYPE=$2

validar_tipo

# 1a parte
obtener_info
comprobar_instancia
confirmar_cambio
detener_instancia

# 2a parte
cambiar_tipo
arrancar_instancia
mostrar_tiempos

exit 0