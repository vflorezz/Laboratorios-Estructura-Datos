"""
graficas.py

Lee resultados/resultados.csv (generado por experimentos.py), calcula las estadisticas
(promedio y desviación estándar de las repeticiones) y genera:
  - resultados/tabla_resumen.csv      (todas las estadisticas)
  - resultados/graficas/*.png         (las graficas)

Como correrlo (en la misma carpeta que experimentos.py) usar la terminal:
    pip install pandas matplotlib      (solo la primera vez)
    python graficas.py
"""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")                       # genera imagenes sin abrir ventanas
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------------------
# CONFIGURACION (debe coincidir con experimentos.py)
# ----------------------------------------------------------------------------------------
RUTA_CSV = sys.argv[1] if len(sys.argv) > 1 else os.path.join("resultados", "resultados.csv")
CARPETA = os.path.dirname(RUTA_CSV) or "."
CARPETA_GRAFICAS = os.path.join(CARPETA, "graficas")
M_RANGOS = 100                              # consultas por rango en cada prueba
RANGOS = ["muy_chico", "chico", "mediano", "enorme"]
PARTE_RANGO = {"muy_chico": "0,1%", "chico": "1%", "mediano": "10%", "enorme": "50%"}
N_FIJO_RANGOS = 10000                       # N usado para la grafica "tiempo vs tamano del rango"

NOMBRE = {"Lista": "Lista (búsqueda secuencial)",
          "ABB": "ABB (árbol binario de búsqueda)",
          "B+": "Árbol B+ (grado 50)"}
NOMBRE_CORTO = {"Lista": "Lista", "ABB": "ABB", "B+": "Árbol B+"}
COLOR = {"Lista": "#d62728", "ABB": "#1f77b4", "B+": "#2ca02c"}
MARCADOR = {"Lista": "o", "ABB": "s", "B+": "^"}
ESTILO_ORDEN = {"aleatorio": "-", "ordenado": "--"}
ESTRUCTURAS = ["Lista", "ABB", "B+"]

# ----------------------------------------------------------------------------------------
# LECTURA Y ESTADISTICAS
# ----------------------------------------------------------------------------------------
df = pd.read_csv(RUTA_CSV)
os.makedirs(CARPETA_GRAFICAS, exist_ok=True)
for archivo in os.listdir(CARPETA_GRAFICAS):          # borra gráficas de corridas anteriores para que no se mezclen
    if archivo.endswith(".png"):
        os.remove(os.path.join(CARPETA_GRAFICAS, archivo))
N_REP = int(df["repeticion"].max())
M = int(df["M"].iloc[0])
TAMANOS = sorted(df["N"].unique())

# Se pasan los tiempos a unidades faciles de leer
df["busqueda_us"] = df["t_busqueda_s"] / df["M"] * 1e6          # microsegundos POR busqueda
df["insercion_ms"] = df["t_insercion_s"] * 1e3                  # milisegundos (insertar los N)
df["listado_ms"] = df["t_listado_s"] * 1e3                      # milisegundos (listar los N)
for t in RANGOS:
    df[f"rango_{t}_ms"] = df[f"t_rango_{t}_s"] / M_RANGOS * 1e3  # milisegundos POR consulta de rango


def atipicos_iqr(serie):
    """Cuenta valores atipicos con la regla del rango intercuartilico (1,5 x IQR)."""
    q1, q3 = serie.quantile([0.25, 0.75])
    iqr = q3 - q1
    return int(((serie < q1 - 1.5 * iqr) | (serie > q3 + 1.5 * iqr)).sum())


def estadisticas(columna):
    d = df.dropna(subset=[columna])
    g = d.groupby(["orden", "estructura", "N"])[columna]
    t = g.agg(n="count", promedio="mean", desv="std", mediana="median").reset_index()
    t["atipicos"] = g.apply(atipicos_iqr).values
    return t


OPERACIONES = [("busqueda_us", "búsqueda por ID", "microsegundos por búsqueda")]
OPERACIONES += [("insercion_ms", "inserción de N estudiantes", "milisegundos (total)"),
                ("listado_ms", "listado ordenado de N estudiantes", "milisegundos")]
OPERACIONES += [(f"rango_{t}_ms", f"búsqueda por rango ({PARTE_RANGO[t]} de los IDs)", "milisegundos por consulta")
                for t in RANGOS]
OPERACIONES += [("altura", "altura del árbol", "niveles")]

ST = {col: estadisticas(col) for col, _, _ in OPERACIONES}

filas = []
for col, nombre_op, unidad in OPERACIONES:
    s = ST[col].copy()
    s.insert(0, "operacion", nombre_op)
    s.insert(1, "unidad", unidad)
    filas.append(s)
tabla = pd.concat(filas, ignore_index=True).rename(columns={
    "n": "ejecuciones", "promedio": "promedio", "desv": "desv_estandar",
    "mediana": "mediana", "atipicos": "atipicos_IQR"})
tabla.to_csv(os.path.join(CARPETA, "tabla_resumen.csv"), index=False, float_format="%.6g", encoding="utf-8-sig")
print("Tabla resumen:", os.path.join(CARPETA, "tabla_resumen.csv"))


def pendiente(st, est, orden):
    """Pendiente de la recta ajustada a log10(promedio) vs log10(N): es el 'exponente' de N en la escala log-log."""
    d = st[(st.estructura == est) & (st.orden == orden)].dropna(subset=["promedio"])
    d = d[d["promedio"] > 0]
    if len(d) < 3:
        return None
    return float(np.polyfit(np.log10(d["N"].astype(float)), np.log10(d["promedio"]), 1)[0])


def etq(st, est, orden, texto):
    """Agrega la pendiente al texto de la leyenda."""
    p = pendiente(st, est, orden)
    return texto if p is None else f"{texto} (pendiente {p:.2f})".replace(".", ",")


filas_p = []
for col, nombre_op, unidad in OPERACIONES:
    if col == "altura":
        continue
    for orden in ["aleatorio", "ordenado"]:
        for est in ["Lista", "ABB", "B+"]:
            p = pendiente(ST[col], est, orden)
            if p is not None:
                filas_p.append({"operacion": nombre_op, "orden": orden, "estructura": est, "pendiente_log_log": round(p, 3)})
pd.DataFrame(filas_p).to_csv(os.path.join(CARPETA, "pendientes.csv"), index=False, encoding="utf-8-sig")
print("Pendientes:", os.path.join(CARPETA, "pendientes.csv"))

# ----------------------------------------------------------------------------------------
# FUNCIONES PARA DIBUJAR
# ----------------------------------------------------------------------------------------
def miles(n):
    return f"{int(n):,}".replace(",", ".")


def serie(st, estructura, orden):
    return st[(st.estructura == estructura) & (st.orden == orden)].sort_values("N")


def curva(ax, d, x, estructura, orden, etiqueta, y="promedio", barras=True):
    """Dibuja una curva con barras de error (+-1 desviación estándar)."""
    if d.empty:
        return
    inferior = np.minimum(d["desv"], d[y] * 0.95)               # evita que la barra baje de 0 (escala log)
    ax.errorbar(d[x], d[y], yerr=[inferior, d["desv"]] if barras else None,
                color=COLOR[estructura], marker=MARCADOR[estructura], linestyle=ESTILO_ORDEN[orden],
                markersize=5, linewidth=1.6, capsize=3, label=etiqueta)


def formato(ax, titulo, xlabel, ylabel, log_x=True, log_y=True, ticks_n=True):
    ax.set_title(titulo, fontsize=10)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if log_x:
        ax.set_xscale("log")
    if log_y:
        ax.set_yscale("log")
    if ticks_n and log_x:
        ax.set_xticks(TAMANOS)
        ax.set_xticklabels([miles(n) for n in TAMANOS], rotation=45, fontsize=8)
        ax.xaxis.set_minor_locator(NullLocator())
    ax.grid(True, which="major", alpha=0.35)
    _, etiquetas = ax.get_legend_handles_labels()
    if len(etiquetas) > 4:                       # leyendas largas: se ponen debajo para no tapar las curvas
        ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=2)
    else:
        ax.legend(fontsize=8)


def guardar(fig, nombre, titulo, pie):
    fig.suptitle(titulo, fontsize=12, fontweight="bold")
    pie = textwrap.fill(pie, width=int(fig.get_figwidth() * 13))
    fig.text(0.5, 0.012, pie, ha="center", va="bottom", fontsize=8, color="#444444")
    fig.tight_layout(rect=[0, 0.10, 1, 0.96])
    ruta = os.path.join(CARPETA_GRAFICAS, nombre)
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    print("  ", ruta)


PIE_BASE = f"Promedio de {N_REP} repeticiones; barras = ±1 desviación estándar; ejes en escala logarítmica."
PIE_BUSQUEDA = PIE_BASE + f" Cada repetición hace M = {miles(M)} búsquedas."
PIE_PEND = " Pendiente de la leyenda: recta ajustada en escala log-log (≈ 1 lineal, ≈ 2 cuadrática, cerca de 0 crecimiento muy lento)."

# ----------------------------------------------------------------------------------------
# GRAFICAS (5)
# ----------------------------------------------------------------------------------------
print("Graficas:")

# 1. Busqueda por ID vs N (IDs aleatorios)
fig, ax = plt.subplots(figsize=(8, 5.5))
for est in ESTRUCTURAS:
    curva(ax, serie(ST["busqueda_us"], est, "aleatorio"), "N", est, "aleatorio", etq(ST["busqueda_us"], est, "aleatorio", NOMBRE[est]))
formato(ax, "IDs insertados en orden aleatorio", "Cantidad de estudiantes N", "Tiempo por búsqueda (microsegundos)")
guardar(fig, "01_busqueda_vs_N.png", "Búsqueda por ID: tiempo vs. N",
        PIE_BUSQUEDA + PIE_PEND)

# 2. Efecto del orden de insercion en la busqueda
fig, ax = plt.subplots(figsize=(8, 5.5))
for est in ESTRUCTURAS:
    for orden in ["aleatorio", "ordenado"]:
        curva(ax, serie(ST["busqueda_us"], est, orden), "N", est, orden, etq(ST["busqueda_us"], est, orden, f"{NOMBRE_CORTO[est]}, IDs {orden}s"))
formato(ax, "Mismo color = misma estructura; línea punteada = IDs ordenados", "Cantidad de estudiantes N",
        "Tiempo por búsqueda (microsegundos)")
guardar(fig, "02_efecto_del_orden_busqueda.png", "Búsqueda por ID: IDs aleatorios vs. IDs ordenados",
        PIE_BUSQUEDA + PIE_PEND)

# 3. Altura vs N
fig, ax = plt.subplots(figsize=(8, 5.5))
for est, orden in [("ABB", "aleatorio"), ("ABB", "ordenado"), ("B+", "aleatorio"), ("B+", "ordenado")]:
    curva(ax, serie(ST["altura"], est, orden), "N", est, orden, f"{NOMBRE_CORTO[est]}, IDs {orden}s")
ax.plot(np.array(TAMANOS, dtype=float), np.log2(np.array(TAMANOS, dtype=float)), color="black", linestyle=":",
        linewidth=1.3, label="Referencia: log2(N)")
formato(ax, "Mismo color = misma estructura; línea punteada = IDs ordenados", "Cantidad de estudiantes N",
        "Altura (número de niveles)")
guardar(fig, "03_altura_vs_N.png", "Altura del árbol vs. N",
        PIE_BASE + " Altura = número de niveles (solo la raíz = 1).")

# 4. Insercion vs N
fig, axs = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
for ax, orden in zip(axs, ["aleatorio", "ordenado"]):
    for est in ESTRUCTURAS:
        curva(ax, serie(ST["insercion_ms"], est, orden), "N", est, orden, etq(ST["insercion_ms"], est, orden, NOMBRE_CORTO[est]))
    formato(ax, f"IDs {orden}s", "Cantidad de estudiantes N", "Tiempo total de inserción (milisegundos)")
guardar(fig, "04_insercion_vs_N.png", "Inserción de los N estudiantes: tiempo total vs. N", PIE_BASE + PIE_PEND)

# 5. Listado ordenado vs N
fig, axs = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
for ax, orden in zip(axs, ["aleatorio", "ordenado"]):
    for est in ESTRUCTURAS:
        curva(ax, serie(ST["listado_ms"], est, orden), "N", est, orden, etq(ST["listado_ms"], est, orden, NOMBRE_CORTO[est]))
    formato(ax, f"IDs {orden}s", "Cantidad de estudiantes N", "Tiempo de listado (milisegundos)")
guardar(fig, "05_listado_vs_N.png", "Listado de todos los estudiantes en orden ascendente de ID: tiempo vs. N",
        PIE_BASE + " El listado se mide una sola vez por repetición. Lista: sorted(); ABB: recorrido inorden; B+: recorrido de las hojas enlazadas." + PIE_PEND)

# 6. Busqueda por rango (dos paneles, IDs aleatorios)
fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
for est in ESTRUCTURAS:
    curva(axs[0], serie(ST["rango_chico_ms"], est, "aleatorio"), "N", est, "aleatorio", etq(ST["rango_chico_ms"], est, "aleatorio", NOMBRE_CORTO[est]))
formato(axs[0], "Rango chico (1% de los IDs), según N", "Cantidad de estudiantes N",
        "Tiempo por consulta de rango (milisegundos)")
for est in ESTRUCTURAS:
    puntos = []
    for t in RANGOS:
        d = df[(df.estructura == est) & (df.orden == "aleatorio") & (df.N == N_FIJO_RANGOS)]
        puntos.append({"N": d[f"k_rango_{t}"].mean(), "promedio": d[f"rango_{t}_ms"].mean(),
                       "desv": d[f"rango_{t}_ms"].std()})
    curva(axs[1], pd.DataFrame(puntos), "N", est, "aleatorio", NOMBRE_CORTO[est])
formato(axs[1], f"Según el tamaño del rango (N = {miles(N_FIJO_RANGOS)})", "Estudiantes devueltos por consulta",
        "Tiempo por consulta de rango (milisegundos)", ticks_n=False)
guardar(fig, "06_busqueda_por_rango.png", "Búsqueda por rango (IDs aleatorios)",
        PIE_BASE + f" {M_RANGOS} consultas por repetición. Derecha: rangos de 0,1%, 1%, 10% y 50% de los IDs." + PIE_PEND)

print("Listo.")