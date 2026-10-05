"""
Red Bayesiana Simple para Deteccion de Phishing
Estudiante: José Eduardo De La Cuba Zambrano


Objetivo:
Calcular la probabilidad de que un sitio web sea phishing a partir de
tres evidencias:
1. URL sospechosa
2. HTTPS ausente
3. Solicitud de credenciales

Las probabilidades utilizadas son simuladas con fines academicos.
"""

# ============================================================
# SECCION 1: PROBABILIDAD INICIAL DE PHISHING
# ============================================================
# Aqui se define la probabilidad inicial de que un sitio sea phishing
# antes de observar cualquier evidencia.


P_PHISHING = {
    True: 0.25,
    False: 0.75
}


# ============================================================
# SECCION 2: PROBABILIDADES CONDICIONALES
# ============================================================
# En una red bayesiana, cada evidencia tiene una probabilidad que
# depende de si el sitio realmente es phishing o no.

# ------------------------------------------------------------
# Probabilidad de observar una URL sospechosa
# ------------------------------------------------------------
# Primer True/False  -> indica si el sitio es phishing.
# Segundo True/False -> indica si la URL es sospechosa.
#


P_URL_SOSPECHOSA = {
    True: {True: 0.80, False: 0.20},
    False: {True: 0.25, False: 0.75}
}

# ------------------------------------------------------------
# Probabilidad de que el HTTPS este ausente
# ------------------------------------------------------------
# Si es phishing:
#   P(HTTPS ausente = Si) = 0.55
#   P(HTTPS ausente = No) = 0.45
#
# Si NO es phishing:
#   P(HTTPS ausente = Si) = 0.20
#   P(HTTPS ausente = No) = 0.80

P_HTTPS_AUSENTE = {
    True: {True: 0.55, False: 0.45},
    False: {True: 0.20, False: 0.80}
}

# ------------------------------------------------------------
# Probabilidad de que el sitio solicite credenciales
# ------------------------------------------------------------
# Si es phishing:
#   P(Solicita credenciales = Si) = 0.75
#   P(Solicita credenciales = No) = 0.25
#
# Si NO es phishing:
#   P(Solicita credenciales = Si) = 0.30
#   P(Solicita credenciales = No) = 0.70

P_CREDENCIALES = {
    True: {True: 0.75, False: 0.25},
    False: {True: 0.30, False: 0.70}
}


# ============================================================
# SECCION 3: FUNCION PARA LEER RESPUESTAS DEL USUARIO
# ============================================================
# Esta funcion muestra una pregunta y obliga al usuario a responder
# "s" o "n".
#
# Devuelve:
#   True  -> cuando el usuario responde Si
#   False -> cuando el usuario responde No

def leer_si_no(mensaje):
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()

        if respuesta in ("s", "si"):
            return True

        if respuesta in ("n", "no"):
            return False

        # Si el usuario escribe otro valor, la pregunta se repite.
        print("Entrada no valida. Escriba 's' o 'n'.")


# ============================================================
# SECCION 4: CALCULO DE LA PROBABILIDAD CONJUNTA
# ============================================================
# Esta funcion calcula la probabilidad de una combinacion completa
# de eventos.
#
# Formula utilizada:
#
# P(Phishing) *
# P(URL | Phishing) *
# P(HTTPS | Phishing) *
# P(Credenciales | Phishing)
#
# Se hace este calculo una vez suponiendo que el sitio SI es phishing
# y otra vez suponiendo que NO es phishing.

def calcular_probabilidad_conjunta(
    phishing,
    url_sospechosa,
    https_ausente,
    solicita_credenciales
):
    # Comenzamos con la probabilidad inicial de phishing o no phishing.
    prob = P_PHISHING[phishing]

    # Multiplicamos por la probabilidad de la evidencia "URL sospechosa".
    prob *= P_URL_SOSPECHOSA[phishing][url_sospechosa]

    # Multiplicamos por la probabilidad de la evidencia "HTTPS ausente".
    prob *= P_HTTPS_AUSENTE[phishing][https_ausente]

    # Multiplicamos por la probabilidad de que solicite credenciales.
    prob *= P_CREDENCIALES[phishing][solicita_credenciales]

    # Devolvemos la probabilidad conjunta obtenida.
    return prob


# ============================================================
# SECCION 5: INFERENCIA BAYESIANA
# ============================================================
# Esta es la parte principal del programa.
#
# Se calculan dos probabilidades:
#
# 1. Probabilidad de las evidencias suponiendo que ES phishing.
# 2. Probabilidad de las evidencias suponiendo que NO ES phishing.
#
# Luego ambas probabilidades se normalizan para obtener:
#
# P(Phishing | evidencias)
# P(No Phishing | evidencias)
#
# La normalizacion hace que ambas probabilidades sumen 1.

def inferir_phishing(
    url_sospechosa,
    https_ausente,
    solicita_credenciales
):
    # Caso 1: suponemos que el sitio SI es phishing.
    prob_phishing = calcular_probabilidad_conjunta(
        True,
        url_sospechosa,
        https_ausente,
        solicita_credenciales
    )

    # Caso 2: suponemos que el sitio NO es phishing.
    prob_no_phishing = calcular_probabilidad_conjunta(
        False,
        url_sospechosa,
        https_ausente,
        solicita_credenciales
    )

    # Sumamos ambos resultados.
    # Este valor sirve como denominador para normalizar.
    total = prob_phishing + prob_no_phishing

    # Probabilidad posterior de que SI sea phishing.
    posterior_phishing = prob_phishing / total

    # Probabilidad posterior de que NO sea phishing.
    posterior_no_phishing = prob_no_phishing / total

    # Retornamos ambos resultados.
    return posterior_phishing, posterior_no_phishing


# ============================================================
# SECCION 6: CLASIFICACION DEL NIVEL DE RIESGO
# ============================================================
# Convierte la probabilidad numerica en una descripcion sencilla.
#
# 75 % o mas       -> Alto riesgo
# Entre 50 y 74 %  -> Riesgo moderado
# Menor de 50 %    -> Bajo riesgo

def clasificar_riesgo(probabilidad):
    if probabilidad >= 0.75:
        return "ALTO RIESGO"

    elif probabilidad >= 0.50:
        return "RIESGO MODERADO"

    else:
        return "BAJO RIESGO"


# ============================================================
# SECCION 7: CONVERSION DE BOOLEANOS A TEXTO
# ============================================================
# Python utiliza True y False internamente.
# Para mostrar resultados mas faciles de leer se transforman en
# "Si" y "No".

def texto_booleano(valor):
    return "Si" if valor else "No"


# ============================================================
# SECCION 8: PROGRAMA PRINCIPAL
# ============================================================
# La funcion main() controla el flujo general del programa:
#
# 1. Muestra el titulo y la estructura de la red.
# 2. Solicita las evidencias al usuario.
# 3. Ejecuta la inferencia bayesiana.
# 4. Muestra las probabilidades obtenidas.
# 5. Clasifica el nivel de riesgo.

def main():

    # Encabezado del programa.
    print("=" * 58)
    print("     RED BAYESIANA SIMPLE - DETECCION DE PHISHING")
    print("=" * 58)

    # Representacion textual de la estructura de la red bayesiana.
    print("""
Estructura de la red:

                         PHISHING
                       /    |     \\
                      v     v      v
             URL sospechosa HTTPS  Credenciales
    """)

    print("Ingrese las evidencias observadas en el sitio web:\n")

    # --------------------------------------------------------
    # Entrada de evidencias
    # --------------------------------------------------------

    # Pregunta si la direccion URL parece sospechosa.
    url_sospechosa = leer_si_no(
        "¿La URL presenta caracteristicas sospechosas?"
    )

    # Pregunta si el sitio carece de HTTPS.
    https_ausente = leer_si_no(
        "¿El sitio tiene HTTPS ausente?"
    )

    # Pregunta si el sitio solicita usuario, contrasena u otros datos.
    solicita_credenciales = leer_si_no(
        "¿El sitio solicita credenciales?"
    )

    # --------------------------------------------------------
    # Inferencia
    # --------------------------------------------------------
    # Enviamos las evidencias a la funcion que calcula las
    # probabilidades posteriores.

    prob_phishing, prob_no_phishing = inferir_phishing(
        url_sospechosa,
        https_ausente,
        solicita_credenciales
    )

    # --------------------------------------------------------
    # Mostrar las evidencias ingresadas
    # --------------------------------------------------------

    print("\n" + "-" * 58)
    print("EVIDENCIAS OBSERVADAS")
    print("-" * 58)

    print(
        f"URL sospechosa        : "
        f"{texto_booleano(url_sospechosa)}"
    )

    print(
        f"HTTPS ausente         : "
        f"{texto_booleano(https_ausente)}"
    )

    print(
        f"Solicita credenciales : "
        f"{texto_booleano(solicita_credenciales)}"
    )

    # --------------------------------------------------------
    # Mostrar los resultados de la inferencia
    # --------------------------------------------------------

    print("\n" + "-" * 58)
    print("RESULTADO DE LA INFERENCIA")
    print("-" * 58)

    # Multiplicamos por 100 para convertir la probabilidad a porcentaje.
    print(
        f"P(Phishing | evidencias)    = "
        f"{prob_phishing * 100:.2f}%"
    )

    print(
        f"P(No Phishing | evidencias) = "
        f"{prob_no_phishing * 100:.2f}%"
    )

    # Muestra la clasificacion: bajo, moderado o alto riesgo.
    print(
        f"Clasificacion               = "
        f"{clasificar_riesgo(prob_phishing)}"
    )

    # Aclaracion importante para el trabajo academico.
    print("\nNota:")
    print("Las probabilidades utilizadas son simuladas y se emplean")
    print("unicamente con fines academicos.")

    print("=" * 58)


# ============================================================
# SECCION 9: PUNTO DE INICIO DEL PROGRAMA
# ============================================================
# Esta condicion permite ejecutar main() solo cuando este archivo
# se ejecuta directamente con:
#
# python red_bayes_phishing_comentado.py
#
# Si el archivo se importa desde otro programa, main() no se ejecuta
# automaticamente.

if __name__ == "__main__":
    main()
