"""
DISEÑO PRELIMINAR DE MURO DE CONTENCIÓN EN VOLADIZO
Concreto armado - Sistema SI - Análisis por metro lineal

Referencias generales:
- RNE E.050: Suelos y Cimentaciones.
- RNE E.060: Concreto Armado.
- RNE E.020: Cargas.
- RNE E.030: Diseño Sismorresistente, cuando el proyecto requiera análisis sísmico.

ALCANCE Y ADVERTENCIA
---------------------
Esta herramienta realiza un predimensionamiento y verificaciones preliminares
de un muro en voladizo con relleno horizontal y cimentación horizontal.
No reemplaza el Estudio de Mecánica de Suelos, el análisis sísmico específico,
la revisión de drenaje, el diseño de juntas, detalles constructivos, estabilidad
global del talud ni la firma de un ingeniero civil colegiado y habilitado.

Unidades:
- Longitudes: m
- Pesos unitarios: kN/m³
- Sobrecarga: kPa = kN/m²
- Resistencias: MPa
- Fuerzas por metro de muro: kN/m
- Momentos por metro de muro: kN·m/m
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from math import radians, sin, cos, sqrt, tan
from pathlib import Path
from typing import Optional
import json


# ---------------------------------------------------------------------------
# UTILIDADES DE ENTRADA
# ---------------------------------------------------------------------------

def leer_float(
    mensaje: str,
    default: Optional[float] = None,
    minimo: Optional[float] = None,
    maximo: Optional[float] = None,
) -> float:
    """Lee un número real, aplicando valor por defecto y límites."""
    while True:
        sufijo = f" [{default}]" if default is not None else ""
        texto = input(f"{mensaje}{sufijo}: ").strip().replace(",", ".")
        if not texto and default is not None:
            valor = float(default)
        else:
            try:
                valor = float(texto)
            except ValueError:
                print("  Error: ingrese un número válido.")
                continue

        if minimo is not None and valor < minimo:
            print(f"  Error: el valor mínimo permitido es {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"  Error: el valor máximo permitido es {maximo}.")
            continue
        return valor


def leer_si_no(mensaje: str, default: bool = False) -> bool:
    """Lee una respuesta sí/no."""
    opcion_default = "S/n" if default else "s/N"
    while True:
        texto = input(f"{mensaje} [{opcion_default}]: ").strip().lower()
        if not texto:
            return default
        if texto in {"s", "si", "sí", "y", "yes"}:
            return True
        if texto in {"n", "no"}:
            return False
        print("  Responda S o N.")


# ---------------------------------------------------------------------------
# DATOS DEL PROYECTO
# ---------------------------------------------------------------------------

@dataclass
class Geometria:
    altura_retenida: float       # H, desde cara superior de zapata
    espesor_fuste_superior: float
    espesor_fuste_inferior: float
    espesor_zapata: float
    ancho_puntera: float
    ancho_talon: float
    profundidad_desplante: float

    @property
    def ancho_base(self) -> float:
        return self.ancho_puntera + self.espesor_fuste_inferior + self.ancho_talon


@dataclass
class SueloRelleno:
    peso_unitario: float         # gamma
    angulo_friccion: float       # phi, grados
    cohesion: float              # c, kPa; no usada en empuje permanente por seguridad
    sobrecarga: float            # q, kPa
    nivel_freatico: float        # altura de agua medida desde la base del relleno
    peso_unitario_saturado: float
    inclinacion_relleno: float   # beta; esta versión exige 0°


@dataclass
class SueloCimentacion:
    capacidad_admisible: float   # qadm, kPa
    coef_friccion_base: float    # mu
    cohesion_base: float         # ca, kPa
    peso_unitario: float
    profundidad_para_pasivo: float
    angulo_friccion: float
    usar_pasivo: bool


@dataclass
class Materiales:
    fc: float                    # MPa
    fy: float                    # MPa
    peso_concreto: float         # kN/m³
    recubrimiento_fuste: float   # m
    recubrimiento_zapata: float  # m
    diametro_barra_fuste: float  # m
    diametro_barra_zapata: float # m


@dataclass
class Criterios:
    fs_deslizamiento_min: float
    fs_volteo_min: float
    fs_capacidad_min: float
    porcentaje_pasivo: float
    phi_flexion: float
    phi_corte: float
    factor_mayoracion_tierra: float
    factor_mayoracion_sobrecarga: float
    rho_min_fuste: float
    rho_min_zapata: float
    separacion_maxima: float     # m
    incluir_sismo: bool
    kh: float
    kv: float


@dataclass
class DatosProyecto:
    nombre: str
    geometria: Geometria
    relleno: SueloRelleno
    cimentacion: SueloCimentacion
    materiales: Materiales
    criterios: Criterios


# ---------------------------------------------------------------------------
# RESULTADOS
# ---------------------------------------------------------------------------

@dataclass
class ResultadoEstabilidad:
    ka: float
    empuje_suelo: float
    empuje_sobrecarga: float
    empuje_agua: float
    empuje_sismico_incremental: float
    empuje_horizontal_total: float
    peso_total: float
    momento_resistente: float
    momento_volcante: float
    fs_deslizamiento: float
    fs_volteo: float
    excentricidad: float
    q_max: float
    q_min: float
    fs_capacidad: float
    cumple_deslizamiento: bool
    cumple_volteo: bool
    cumple_resultante: bool
    cumple_capacidad: bool


@dataclass
class ResultadoElemento:
    nombre: str
    momento_servicio: float
    momento_ultimo: float
    cortante_ultimo: float
    peralte_efectivo: float
    acero_calculado_cm2_m: float
    acero_minimo_cm2_m: float
    acero_requerido_cm2_m: float
    separacion_barra_cm: float
    resistencia_corte_kN_m: float
    cumple_corte: bool


# ---------------------------------------------------------------------------
# MECÁNICA DE SUELOS Y ESTABILIDAD
# ---------------------------------------------------------------------------

GAMMA_AGUA = 9.81  # kN/m³


def coeficiente_rankine_activo(phi_grados: float) -> float:
    """Ka de Rankine para relleno horizontal y muro vertical sin fricción."""
    phi = radians(phi_grados)
    return (1.0 - sin(phi)) / (1.0 + sin(phi))


def coeficiente_rankine_pasivo(phi_grados: float) -> float:
    phi = radians(phi_grados)
    return (1.0 + sin(phi)) / (1.0 - sin(phi))


def coeficiente_mononobe_okabe_simplificado(
    phi_grados: float, kh: float, kv: float
) -> float:
    """
    Aproximación conservadora de Ka sísmico para trasdós horizontal,
    muro vertical y fricción muro-suelo nula.

    Se usa para obtener un incremento pseudoestático aproximado:
        Delta P = 0.5 * gamma * H² * max(Kae - Ka, 0)

    Debe reemplazarse por un análisis geotécnico sísmico específico
    cuando el proyecto lo exija.
    """
    phi = radians(phi_grados)
    denominador = max(1.0 - kv, 1e-6)
    theta = radians(0.0)
    from math import atan
    theta = atan(kh / denominador)

    if theta >= phi:
        raise ValueError(
            "La combinación kh/kv produce theta >= phi; "
            "Mononobe-Okabe no es aplicable con estos datos."
        )

    raiz = sqrt(
        max(
            sin(phi) * sin(phi - theta) /
            max(cos(theta), 1e-9),
            0.0
        )
    )
    denominador_kae = cos(theta) * (1.0 + raiz) ** 2
    return cos(phi - theta) ** 2 / max(denominador_kae, 1e-9)


def analizar_estabilidad(datos: DatosProyecto) -> ResultadoEstabilidad:
    g = datos.geometria
    s = datos.relleno
    c = datos.cimentacion
    m = datos.materiales
    cr = datos.criterios

    if abs(s.inclinacion_relleno) > 1e-9:
        raise NotImplementedError(
            "Esta versión admite relleno horizontal (inclinación = 0°)."
        )

    H = g.altura_retenida
    B = g.ancho_base
    Ka = coeficiente_rankine_activo(s.angulo_friccion)

    # Empuje efectivo del suelo. Si hay agua, se separa suelo sumergido + agua.
    hw = min(max(s.nivel_freatico, 0.0), H)
    h_seco = H - hw
    gamma_sumergido = max(s.peso_unitario_saturado - GAMMA_AGUA, 0.0)

    # Integración por capas del diagrama Ka*sigma'_v:
    # capa seca triangular + capa sumergida trapezoidal
    p_seco = 0.5 * Ka * s.peso_unitario * h_seco**2
    sigma_interfaz = Ka * s.peso_unitario * h_seco
    p_sum_rect = sigma_interfaz * hw
    p_sum_tri = 0.5 * Ka * gamma_sumergido * hw**2
    P_suelo = p_seco + p_sum_rect + p_sum_tri

    # Momentos respecto a la base:
    # se integran mediante resultantes simples.
    M_suelo = 0.0
    if h_seco > 0:
        # Triángulo seco ubicado en el tramo superior:
        M_suelo += p_seco * (hw + h_seco / 3.0)
    if hw > 0:
        M_suelo += p_sum_rect * (hw / 2.0)
        M_suelo += p_sum_tri * (hw / 3.0)

    P_q = Ka * s.sobrecarga * H
    M_q = P_q * H / 2.0

    P_agua = 0.5 * GAMMA_AGUA * hw**2
    M_agua = P_agua * hw / 3.0

    P_sismo = 0.0
    M_sismo = 0.0
    if cr.incluir_sismo:
        Kae = coeficiente_mononobe_okabe_simplificado(
            s.angulo_friccion, cr.kh, cr.kv
        )
        delta_k = max(Kae - Ka, 0.0)
        P_sismo = 0.5 * s.peso_unitario * H**2 * delta_k
        # Convención usual preliminar: incremento aplicado a 0.6H.
        M_sismo = P_sismo * 0.60 * H

    P_total = P_suelo + P_q + P_agua + P_sismo
    M_volcante = M_suelo + M_q + M_agua + M_sismo

    # Pesos verticales por metro lineal y brazos desde la punta de la puntera.
    W_zapata = B * g.espesor_zapata * m.peso_concreto
    x_zapata = B / 2.0

    area_fuste = 0.5 * (
        g.espesor_fuste_superior + g.espesor_fuste_inferior
    ) * H
    W_fuste = area_fuste * m.peso_concreto
    # Aproximación del centroide horizontal del fuste en el eje de su base.
    x_fuste = g.ancho_puntera + g.espesor_fuste_inferior / 2.0

    W_suelo_talon = g.ancho_talon * H * s.peso_unitario
    x_suelo_talon = (
        g.ancho_puntera + g.espesor_fuste_inferior + g.ancho_talon / 2.0
    )

    # Sobrecarga vertical sobre el talón; estabilizadora en servicio.
    W_q_talon = g.ancho_talon * s.sobrecarga
    x_q_talon = x_suelo_talon

    W_total = W_zapata + W_fuste + W_suelo_talon + W_q_talon
    M_resistente = (
        W_zapata * x_zapata
        + W_fuste * x_fuste
        + W_suelo_talon * x_suelo_talon
        + W_q_talon * x_q_talon
    )

    # Resistencia al deslizamiento.
    R_friccion = c.coef_friccion_base * W_total
    R_adhesion = max(c.cohesion_base, 0.0) * B

    R_pasivo = 0.0
    if c.usar_pasivo and c.profundidad_para_pasivo > 0:
        Kp = coeficiente_rankine_pasivo(c.angulo_friccion)
        Dp = c.profundidad_para_pasivo
        R_pasivo_bruto = 0.5 * Kp * c.peso_unitario * Dp**2
        R_pasivo = cr.porcentaje_pasivo * R_pasivo_bruto

    R_horizontal = R_friccion + R_adhesion + R_pasivo
    fs_deslizamiento = R_horizontal / max(P_total, 1e-9)
    fs_volteo = M_resistente / max(M_volcante, 1e-9)

    # Resultante vertical y presiones de contacto.
    x_resultante = (M_resistente - M_volcante) / max(W_total, 1e-9)
    excentricidad = B / 2.0 - x_resultante

    q_prom = W_total / B
    q_max = q_prom * (1.0 + 6.0 * excentricidad / B)
    q_min = q_prom * (1.0 - 6.0 * excentricidad / B)
    fs_capacidad = c.capacidad_admisible / max(q_max, 1e-9)

    return ResultadoEstabilidad(
        ka=Ka,
        empuje_suelo=P_suelo,
        empuje_sobrecarga=P_q,
        empuje_agua=P_agua,
        empuje_sismico_incremental=P_sismo,
        empuje_horizontal_total=P_total,
        peso_total=W_total,
        momento_resistente=M_resistente,
        momento_volcante=M_volcante,
        fs_deslizamiento=fs_deslizamiento,
        fs_volteo=fs_volteo,
        excentricidad=excentricidad,
        q_max=q_max,
        q_min=q_min,
        fs_capacidad=fs_capacidad,
        cumple_deslizamiento=fs_deslizamiento >= cr.fs_deslizamiento_min,
        cumple_volteo=fs_volteo >= cr.fs_volteo_min,
        cumple_resultante=abs(excentricidad) <= B / 6.0 and q_min >= 0.0,
        cumple_capacidad=(
            q_max <= c.capacidad_admisible
            and fs_capacidad >= cr.fs_capacidad_min
        ),
    )


# ---------------------------------------------------------------------------
# DISEÑO DE CONCRETO ARMADO
# ---------------------------------------------------------------------------

def acero_flexion_rectangular(
    Mu_kNm: float,
    b_m: float,
    d_m: float,
    fc_MPa: float,
    fy_MPa: float,
    phi: float,
) -> float:
    """
    Acero requerido a flexión para sección rectangular simple.
    Devuelve As en m² por metro lineal.
    """
    if Mu_kNm <= 0:
        return 0.0

    Mu = Mu_kNm * 1e3      # N·m
    b = b_m
    d = d_m
    fc = fc_MPa * 1e6     # Pa
    fy = fy_MPa * 1e6     # Pa

    # phi*As*fy*(d - a/2) = Mu; a = As*fy/(0.85fc b)
    A = phi * fy**2 / (2.0 * 0.85 * fc * b)
    Bq = -phi * fy * d
    C = Mu
    discriminante = Bq**2 - 4.0 * A * C

    if discriminante < 0:
        raise ValueError(
            "La sección es insuficiente a flexión: aumente el espesor/peralte."
        )

    raiz1 = (-Bq - sqrt(discriminante)) / (2.0 * A)
    raiz2 = (-Bq + sqrt(discriminante)) / (2.0 * A)
    candidatos = [x for x in (raiz1, raiz2) if x > 0]
    if not candidatos:
        raise ValueError("No se pudo obtener un área de acero positiva.")
    return min(candidatos)


def resistencia_corte_concreto(
    b_m: float, d_m: float, fc_MPa: float, phi_corte: float
) -> float:
    """
    Resistencia simplificada de diseño a corte:
        phi*Vc = phi*0.17*sqrt(fc')*b*d
    con fc' en MPa, b y d en mm. Resultado kN.
    Debe verificarse contra las disposiciones completas de E.060.
    """
    b_mm = b_m * 1000.0
    d_mm = d_m * 1000.0
    vc_N = 0.17 * sqrt(fc_MPa) * b_mm * d_mm
    return phi_corte * vc_N / 1000.0


def separacion_para_acero(
    As_req_m2_m: float, diametro_m: float, separacion_maxima_m: float
) -> float:
    """Separación de barras en m, limitada por separación máxima."""
    area_barra = 3.141592653589793 * diametro_m**2 / 4.0
    if As_req_m2_m <= 0:
        return separacion_maxima_m
    s = area_barra / As_req_m2_m
    # Redondeo conservador hacia abajo cada 1 cm.
    s_redondeada = max(int(s * 100.0) / 100.0, 0.05)
    return min(s_redondeada, separacion_maxima_m)


def diseñar_elemento(
    nombre: str,
    M_servicio: float,
    V_servicio: float,
    espesor: float,
    recubrimiento: float,
    diametro: float,
    materiales: Materiales,
    criterios: Criterios,
    rho_min: float,
    factor_mayoracion: float,
) -> ResultadoElemento:
    d = espesor - recubrimiento - diametro / 2.0
    if d <= 0:
        raise ValueError(f"Peralte efectivo no válido en {nombre}.")

    Mu = factor_mayoracion * M_servicio
    Vu = factor_mayoracion * V_servicio

    As_calc = acero_flexion_rectangular(
        Mu, 1.0, d, materiales.fc, materiales.fy, criterios.phi_flexion
    )
    As_min = rho_min * 1.0 * espesor
    As_req = max(As_calc, As_min)

    phi_vc = resistencia_corte_concreto(
        1.0, d, materiales.fc, criterios.phi_corte
    )
    separacion = separacion_para_acero(
        As_req, diametro, criterios.separacion_maxima
    )

    return ResultadoElemento(
        nombre=nombre,
        momento_servicio=M_servicio,
        momento_ultimo=Mu,
        cortante_ultimo=Vu,
        peralte_efectivo=d,
        acero_calculado_cm2_m=As_calc * 1e4,
        acero_minimo_cm2_m=As_min * 1e4,
        acero_requerido_cm2_m=As_req * 1e4,
        separacion_barra_cm=separacion * 100.0,
        resistencia_corte_kN_m=phi_vc,
        cumple_corte=Vu <= phi_vc,
    )


def diseñar_fuste(datos: DatosProyecto) -> ResultadoElemento:
    g, s, m, cr = (
        datos.geometria,
        datos.relleno,
        datos.materiales,
        datos.criterios,
    )
    H = g.altura_retenida
    Ka = coeficiente_rankine_activo(s.angulo_friccion)
    hw = min(max(s.nivel_freatico, 0.0), H)
    h_seco = H - hw
    gamma_sub = max(s.peso_unitario_saturado - GAMMA_AGUA, 0.0)

    # Momento y corte en la base del fuste por componentes.
    P1 = 0.5 * Ka * s.peso_unitario * h_seco**2
    M1 = P1 * (hw + h_seco / 3.0)

    sigma_i = Ka * s.peso_unitario * h_seco
    P2 = sigma_i * hw
    M2 = P2 * hw / 2.0

    P3 = 0.5 * Ka * gamma_sub * hw**2
    M3 = P3 * hw / 3.0

    Pq = Ka * s.sobrecarga * H
    Mq = Pq * H / 2.0

    Pw = 0.5 * GAMMA_AGUA * hw**2
    Mw = Pw * hw / 3.0

    Ps = Ms = 0.0
    if cr.incluir_sismo:
        Kae = coeficiente_mononobe_okabe_simplificado(
            s.angulo_friccion, cr.kh, cr.kv
        )
        Ps = 0.5 * s.peso_unitario * H**2 * max(Kae - Ka, 0.0)
        Ms = Ps * 0.60 * H

    M_serv = M1 + M2 + M3 + Mq + Mw + Ms
    V_serv = P1 + P2 + P3 + Pq + Pw + Ps

    # Para una primera versión se usa el factor más desfavorable configurable.
    factor = max(
        cr.factor_mayoracion_tierra,
        cr.factor_mayoracion_sobrecarga,
    )

    return diseñar_elemento(
        "Fuste - acero vertical principal en cara del relleno",
        M_serv,
        V_serv,
        g.espesor_fuste_inferior,
        m.recubrimiento_fuste,
        m.diametro_barra_fuste,
        m,
        cr,
        cr.rho_min_fuste,
        factor,
    )


def diseñar_talon(datos: DatosProyecto, estabilidad: ResultadoEstabilidad) -> ResultadoElemento:
    """
    Talón como voladizo desde la cara posterior del fuste.
    Carga neta simplificada = suelo + sobrecarga + peso propio - reacción media.
    Para diseño final debe usarse la distribución real de presión del terreno.
    """
    g, s, m, cr = (
        datos.geometria,
        datos.relleno,
        datos.materiales,
        datos.criterios,
    )
    L = g.ancho_talon
    if L <= 0:
        raise ValueError("El ancho del talón debe ser mayor que cero.")

    carga_desc = (
        s.peso_unitario * g.altura_retenida
        + s.sobrecarga
        + m.peso_concreto * g.espesor_zapata
    )
    reaccion_aprox = (estabilidad.q_max + estabilidad.q_min) / 2.0
    w_neto = abs(carga_desc - reaccion_aprox)
    M_serv = w_neto * L**2 / 2.0
    V_serv = w_neto * L

    factor = max(cr.factor_mayoracion_tierra, cr.factor_mayoracion_sobrecarga)
    return diseñar_elemento(
        "Talón - acero principal superior",
        M_serv,
        V_serv,
        g.espesor_zapata,
        m.recubrimiento_zapata,
        m.diametro_barra_zapata,
        m,
        cr,
        cr.rho_min_zapata,
        factor,
    )


def diseñar_puntera(datos: DatosProyecto, estabilidad: ResultadoEstabilidad) -> ResultadoElemento:
    """
    Puntera como voladizo desde la cara frontal del fuste.
    Se adopta presión de contacto máxima como carga ascendente conservadora.
    """
    g, m, cr = datos.geometria, datos.materiales, datos.criterios
    L = g.ancho_puntera
    if L <= 0:
        raise ValueError("El ancho de la puntera debe ser mayor que cero.")

    peso_propio = m.peso_concreto * g.espesor_zapata
    w_neto = max(estabilidad.q_max - peso_propio, 0.0)
    M_serv = w_neto * L**2 / 2.0
    V_serv = w_neto * L

    return diseñar_elemento(
        "Puntera - acero principal inferior",
        M_serv,
        V_serv,
        g.espesor_zapata,
        m.recubrimiento_zapata,
        m.diametro_barra_zapata,
        m,
        cr,
        cr.rho_min_zapata,
        cr.factor_mayoracion_tierra,
    )


# ---------------------------------------------------------------------------
# INFORME
# ---------------------------------------------------------------------------

def estado(cumple: bool) -> str:
    return "CUMPLE" if cumple else "NO CUMPLE"


def generar_informe(
    datos: DatosProyecto,
    estabilidad: ResultadoEstabilidad,
    elementos: list[ResultadoElemento],
) -> str:
    g = datos.geometria
    cr = datos.criterios
    lineas = [
        "=" * 78,
        "DISEÑO PRELIMINAR DE MURO DE CONTENCIÓN EN VOLADIZO",
        f"Proyecto: {datos.nombre}",
        "=" * 78,
        "",
        "1. GEOMETRÍA",
        f"Altura retenida H                 = {g.altura_retenida:.3f} m",
        f"Ancho total de base B             = {g.ancho_base:.3f} m",
        f"Espesor de zapata                 = {g.espesor_zapata:.3f} m",
        f"Puntera / fuste base / talón      = "
        f"{g.ancho_puntera:.3f} / {g.espesor_fuste_inferior:.3f} / "
        f"{g.ancho_talon:.3f} m",
        "",
        "2. EMPUJES Y ESTABILIDAD EN SERVICIO",
        f"Ka de Rankine                     = {estabilidad.ka:.4f}",
        f"Empuje de suelo                   = {estabilidad.empuje_suelo:.2f} kN/m",
        f"Empuje por sobrecarga             = {estabilidad.empuje_sobrecarga:.2f} kN/m",
        f"Empuje hidrostático               = {estabilidad.empuje_agua:.2f} kN/m",
        f"Incremento sísmico aproximado     = "
        f"{estabilidad.empuje_sismico_incremental:.2f} kN/m",
        f"Empuje horizontal total           = "
        f"{estabilidad.empuje_horizontal_total:.2f} kN/m",
        f"Peso vertical total               = {estabilidad.peso_total:.2f} kN/m",
        "",
        f"FS deslizamiento                  = {estabilidad.fs_deslizamiento:.3f} "
        f"(mín. adoptado {cr.fs_deslizamiento_min:.2f}) "
        f"[{estado(estabilidad.cumple_deslizamiento)}]",
        f"FS volteo                         = {estabilidad.fs_volteo:.3f} "
        f"(mín. adoptado {cr.fs_volteo_min:.2f}) "
        f"[{estado(estabilidad.cumple_volteo)}]",
        f"Excentricidad e                   = {estabilidad.excentricidad:.4f} m",
        f"Límite del tercio medio B/6       = {g.ancho_base/6.0:.4f} m "
        f"[{estado(estabilidad.cumple_resultante)}]",
        f"Presión q máx. / q mín.           = "
        f"{estabilidad.q_max:.2f} / {estabilidad.q_min:.2f} kPa",
        f"FS capacidad portante calculado   = {estabilidad.fs_capacidad:.3f} "
        f"(mín. adoptado {cr.fs_capacidad_min:.2f}) "
        f"[{estado(estabilidad.cumple_capacidad)}]",
        "",
        "3. DISEÑO PRELIMINAR DE CONCRETO ARMADO",
    ]

    for r in elementos:
        lineas += [
            "-" * 78,
            r.nombre,
            f"Momento de servicio               = {r.momento_servicio:.2f} kN·m/m",
            f"Momento último                    = {r.momento_ultimo:.2f} kN·m/m",
            f"Cortante último                   = {r.cortante_ultimo:.2f} kN/m",
            f"Peralte efectivo d                = {r.peralte_efectivo:.3f} m",
            f"As calculado                      = {r.acero_calculado_cm2_m:.2f} cm²/m",
            f"As mínimo adoptado                = {r.acero_minimo_cm2_m:.2f} cm²/m",
            f"As requerido                      = {r.acero_requerido_cm2_m:.2f} cm²/m",
            f"Separación de barra seleccionada  = {r.separacion_barra_cm:.0f} cm",
            f"φVc                               = {r.resistencia_corte_kN_m:.2f} kN/m "
            f"[{estado(r.cumple_corte)}]",
        ]

    global_ok = all(
        [
            estabilidad.cumple_deslizamiento,
            estabilidad.cumple_volteo,
            estabilidad.cumple_resultante,
            estabilidad.cumple_capacidad,
            *[r.cumple_corte for r in elementos],
        ]
    )

    lineas += [
        "",
        "4. CONCLUSIÓN AUTOMÁTICA",
        f"Resultado preliminar global: {estado(global_ok)}",
        "",
        "5. VERIFICACIONES OBLIGATORIAS NO INCLUIDAS EN ESTA VERSIÓN",
        "- Estabilidad global muro-talud mediante método geotécnico apropiado.",
        "- Asentamientos totales y diferenciales.",
        "- Capacidad portante última y factores del EMS.",
        "- Licuación, expansividad, colapso, agresividad química y socavación.",
        "- Diseño sísmico definitivo y parámetros de sitio de la E.030 vigente.",
        "- Drenaje: filtro, geotextil, tubería, barbacanas e impermeabilización.",
        "- Longitudes de desarrollo, empalmes, anclajes, juntas y detallado E.060.",
        "- Punzonamiento o corte adicional cuando la geometría lo requiera.",
        "- Combinaciones de carga definitivas según uso y expediente técnico.",
        "",
        "ADVERTENCIA: Documento de predimensionamiento. Requiere revisión y firma",
        "de un ingeniero civil colegiado y habilitado, con EMS del proyecto.",
        "=" * 78,
    ]
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# SOLICITUD DE DATOS
# ---------------------------------------------------------------------------

def solicitar_datos() -> DatosProyecto:
    print("\n" + "=" * 78)
    print("MURO DE CONTENCIÓN DE CONCRETO ARMADO - INGRESO DE DATOS")
    print("Todos los valores deben provenir del proyecto y del EMS.")
    print("=" * 78)

    nombre = input("Nombre del proyecto [Muro de contención]: ").strip()
    nombre = nombre or "Muro de contención"

    print("\n[A] GEOMETRÍA DEL MURO")
    geometria = Geometria(
        altura_retenida=leer_float("Altura de terreno retenido H (m)", 3.00, 0.50),
        espesor_fuste_superior=leer_float(
            "Espesor del fuste en coronación (m)", 0.20, 0.15
        ),
        espesor_fuste_inferior=leer_float(
            "Espesor del fuste en la base (m)", 0.35, 0.20
        ),
        espesor_zapata=leer_float("Espesor de la zapata (m)", 0.40, 0.20),
        ancho_puntera=leer_float("Longitud de puntera (m)", 0.80, 0.20),
        ancho_talon=leer_float("Longitud de talón (m)", 1.60, 0.20),
        profundidad_desplante=leer_float(
            "Profundidad de desplante bajo terreno frontal (m)", 0.80, 0.0
        ),
    )

    print("\n[B] SUELO DE RELLENO / TRASDÓS - DATOS DEL EMS")
    relleno = SueloRelleno(
        peso_unitario=leer_float("Peso unitario natural γ (kN/m³)", 18.0, 5.0, 30.0),
        angulo_friccion=leer_float(
            "Ángulo de fricción interna φ (grados)", 30.0, 0.1, 50.0
        ),
        cohesion=leer_float(
            "Cohesión c (kPa; no se aprovecha en empuje permanente)", 0.0, 0.0
        ),
        sobrecarga=leer_float(
            "Sobrecarga uniforme sobre el relleno q (kPa)", 10.0, 0.0
        ),
        nivel_freatico=leer_float(
            "Altura de agua desde la base del relleno (m)", 0.0, 0.0,
            geometria.altura_retenida
        ),
        peso_unitario_saturado=leer_float(
            "Peso unitario saturado γsat (kN/m³)", 20.0, 9.81, 30.0
        ),
        inclinacion_relleno=leer_float(
            "Inclinación del relleno β (grados; esta versión requiere 0)", 0.0, 0.0, 0.0
        ),
    )

    print("\n[C] SUELO DE CIMENTACIÓN - DATOS DEL EMS")
    usar_pasivo = leer_si_no(
        "¿Desea considerar parcialmente el empuje pasivo frontal?", False
    )
    cimentacion = SueloCimentacion(
        capacidad_admisible=leer_float(
            "Capacidad portante admisible qadm (kPa)", 150.0, 1.0
        ),
        coef_friccion_base=leer_float(
            "Coeficiente de fricción concreto-suelo μ", 0.45, 0.0, 1.5
        ),
        cohesion_base=leer_float(
            "Adhesión/cohesión efectiva bajo la base ca (kPa)", 0.0, 0.0
        ),
        peso_unitario=leer_float(
            "Peso unitario del suelo frontal (kN/m³)", 18.0, 5.0, 30.0
        ),
        profundidad_para_pasivo=leer_float(
            "Profundidad efectiva para pasivo frontal Dp (m)",
            geometria.profundidad_desplante if usar_pasivo else 0.0,
            0.0,
        ),
        angulo_friccion=leer_float(
            "Ángulo de fricción del suelo frontal φf (grados)", 30.0, 0.1, 50.0
        ),
        usar_pasivo=usar_pasivo,
    )

    print("\n[D] MATERIALES")
    materiales = Materiales(
        fc=leer_float("Resistencia del concreto f'c (MPa)", 21.0, 17.0),
        fy=leer_float("Fluencia del acero fy (MPa)", 420.0, 200.0, 600.0),
        peso_concreto=leer_float(
            "Peso unitario del concreto (kN/m³)", 24.0, 20.0, 26.0
        ),
        recubrimiento_fuste=leer_float(
            "Recubrimiento del fuste (m)", 0.05, 0.025
        ),
        recubrimiento_zapata=leer_float(
            "Recubrimiento de zapata en contacto con suelo (m)", 0.075, 0.04
        ),
        diametro_barra_fuste=leer_float(
            "Diámetro barra principal del fuste (m), p.ej. 0.016", 0.016, 0.008
        ),
        diametro_barra_zapata=leer_float(
            "Diámetro barra principal de zapata (m), p.ej. 0.016", 0.016, 0.008
        ),
    )

    print("\n[E] CRITERIOS DE DISEÑO CONFIGURABLES")
    print("Los valores siguientes son criterios iniciales; deben validarse con el EMS,")
    print("la categoría del proyecto y la edición vigente del RNE.")
    incluir_sismo = leer_si_no(
        "¿Incluir incremento pseudoestático sísmico preliminar?", False
    )
    criterios = Criterios(
        fs_deslizamiento_min=leer_float(
            "FS mínimo adoptado contra deslizamiento", 1.50, 1.0
        ),
        fs_volteo_min=leer_float(
            "FS mínimo adoptado contra volteo", 2.00, 1.0
        ),
        fs_capacidad_min=leer_float(
            "FS mínimo adoptado para comparación qadm/qmax", 1.00, 1.0
        ),
        porcentaje_pasivo=leer_float(
            "Fracción utilizable del pasivo (0 a 1)", 0.50 if usar_pasivo else 0.0,
            0.0, 1.0
        ),
        phi_flexion=leer_float("Factor φ de flexión", 0.90, 0.50, 1.0),
        phi_corte=leer_float("Factor φ de corte", 0.75, 0.50, 1.0),
        factor_mayoracion_tierra=leer_float(
            "Factor preliminar de mayoración del empuje", 1.60, 1.0
        ),
        factor_mayoracion_sobrecarga=leer_float(
            "Factor preliminar de mayoración de sobrecarga", 1.60, 1.0
        ),
        rho_min_fuste=leer_float(
            "Cuantía mínima adoptada para fuste", 0.0018, 0.0001
        ),
        rho_min_zapata=leer_float(
            "Cuantía mínima adoptada para zapata", 0.0018, 0.0001
        ),
        separacion_maxima=leer_float(
            "Separación máxima adoptada de barras (m)", 0.30, 0.05
        ),
        incluir_sismo=incluir_sismo,
        kh=leer_float(
            "Coeficiente sísmico horizontal kh", 0.15 if incluir_sismo else 0.0,
            0.0, 1.0
        ),
        kv=leer_float(
            "Coeficiente sísmico vertical kv", 0.0, -0.5, 0.5
        ),
    )

    return DatosProyecto(
        nombre=nombre,
        geometria=geometria,
        relleno=relleno,
        cimentacion=cimentacion,
        materiales=materiales,
        criterios=criterios,
    )


def validar_datos(datos: DatosProyecto) -> None:
    g = datos.geometria
    if g.espesor_fuste_superior > g.espesor_fuste_inferior:
        raise ValueError(
            "El espesor superior del fuste no debe superar al espesor inferior."
        )
    if g.ancho_base <= 0:
        raise ValueError("El ancho total de base debe ser positivo.")
    if datos.relleno.nivel_freatico > g.altura_retenida:
        raise ValueError("El nivel freático no puede exceder la altura retenida.")
    if datos.materiales.recubrimiento_zapata >= g.espesor_zapata / 2:
        raise ValueError("El recubrimiento de zapata es excesivo para su espesor.")
    if datos.criterios.incluir_sismo and datos.criterios.kh <= 0:
        raise ValueError("Para análisis sísmico preliminar, kh debe ser mayor que cero.")


def guardar_json(datos: DatosProyecto, ruta: str = "datos_muro.json") -> None:
    Path(ruta).write_text(
        json.dumps(asdict(datos), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def ejecutar() -> None:
    try:
        datos = solicitar_datos()
        validar_datos(datos)

        estabilidad = analizar_estabilidad(datos)
        elementos = [
            diseñar_fuste(datos),
            diseñar_talon(datos, estabilidad),
            diseñar_puntera(datos, estabilidad),
        ]

        informe = generar_informe(datos, estabilidad, elementos)
        print("\n" + informe)

        ruta_informe = Path("informe_muro_contencion.txt")
        ruta_informe.write_text(informe, encoding="utf-8")
        guardar_json(datos)

        print("\nArchivos generados:")
        print(f"- {ruta_informe.resolve()}")
        print(f"- {Path('datos_muro.json').resolve()}")

    except (ValueError, NotImplementedError) as error:
        print(f"\nERROR DE DISEÑO: {error}")
    except KeyboardInterrupt:
        print("\nProceso cancelado por el usuario.")


if __name__ == "__main__":
    ejecutar()