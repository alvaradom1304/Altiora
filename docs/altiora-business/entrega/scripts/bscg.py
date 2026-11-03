#!/usr/bin/env python3
"""BSCG · Business Scope Coverage Gate.

Evalúa si lo que Altiora sabe de una empresa alcanza para la decisión pedida.
Norma: docs/altiora-business/entrega/CONTEXT-FIRST-BSCG.md. No inventa datos:
solo clasifica lo que el archivo de entrada declara y detecta contradicciones.

Uso: python bscg.py archivo.json [--json]
Salida: 0 PASS · 10 CONDITIONAL · 20 HOLD · 2 entrada inválida.
"""
import argparse
import json
import sys

ESTADOS = {"VERIFIED", "REPORTED", "INFERRED", "UNKNOWN", "CONFLICTED", "OUTDATED"}
FIABLES = {"VERIFIED", "REPORTED"}
VALORES = {"SI", "PARCIAL", "NO"}
ALCANCES = {"empresa_completa", "campana", "producto"}
CRITERIOS = [
    "modelo_negocio", "categorias_revisadas", "productos_principales", "hechos_vs_supuestos",
    "objetivos", "decisores", "riesgos", "datos_para_priorizar", "alternativas",
    "respuesta_negocio_completo",
]
MANUALES = ["modelo_negocio", "productos_principales", "hechos_vs_supuestos", "objetivos",
            "decisores", "riesgos", "alternativas"]
CRITICOS = {
    "empresa_completa": {"modelo_negocio", "categorias_revisadas", "objetivos", "decisores",
                         "datos_para_priorizar", "respuesta_negocio_completo"},
    "campana": {"hechos_vs_supuestos", "objetivos", "decisores"},
    "producto": {"hechos_vs_supuestos", "objetivos", "decisores"},
}
DATOS_PRIORIZAR = ("ventas", "margen")
INVENTARIO = ("inventario",)


class EntradaInvalida(Exception):
    pass


def _ratio(buenas, total):
    if total == 0 or buenas == 0:
        return "NO"
    return "SI" if buenas == total else "PARCIAL"


def evaluar(d):
    """Devuelve un dict con resultado, criterios, hallazgos y preguntas."""
    for k in ("empresa", "decision", "alcance_decision", "categorias"):
        if k not in d:
            raise EntradaInvalida(f"falta el campo '{k}'")
    if d["alcance_decision"] not in ALCANCES:
        raise EntradaInvalida(f"alcance_decision debe ser uno de {sorted(ALCANCES)}")
    errores, avisos = [], []
    cats = d["categorias"]
    manual = d.get("criterios_manuales", {})
    for k in MANUALES:
        v = manual.get(k, {}).get("valor")
        if v not in VALORES:
            raise EntradaInvalida(f"criterios_manuales.{k}.valor debe ser SI, PARCIAL o NO")

    # Estados válidos y «VERIFIED» solo con evidencia, no con una declaración.
    def revisar_estado(nombre, estado, fuente_tipo):
        if estado not in ESTADOS:
            raise EntradaInvalida(f"estado inválido en {nombre}: {estado}")
        if estado == "VERIFIED" and fuente_tipo in (None, "", "declaracion"):
            errores.append(f"{nombre}: marcado VERIFIED pero su fuente es una declaración (debe ser REPORTED)")

    for c in cats:
        revisar_estado(f"categoria '{c['nombre']}'", c.get("origen_declaracion", "UNKNOWN"), c.get("fuente_tipo"))
        for campo, est in c.get("datos", {}).items():
            revisar_estado(f"{c['nombre']}.{campo}", est, c.get("fuente_tipo_datos"))
    usadas_no_fiables = []
    for a in d.get("afirmaciones", []):
        revisar_estado(f"afirmación '{a['texto'][:50]}'", a.get("estado", "UNKNOWN"), a.get("fuente_tipo"))
        if a.get("usada_en_decision") and a.get("estado") not in FIABLES:
            usadas_no_fiables.append(a["texto"])

    # Criterios calculados a partir de los datos.
    total = len(cats)
    c2 = _ratio(sum(1 for c in cats if c.get("revisada")), total)
    c8 = _ratio(sum(1 for c in cats if all(c.get("datos", {}).get(x, "UNKNOWN") in FIABLES for x in DATOS_PRIORIZAR)), total)
    if d["alcance_decision"] == "empresa_completa":
        c10 = "SI" if (c2 == "SI" and c8 == "SI") else ("NO" if c2 == "NO" else "PARCIAL")
    else:
        c10 = "SI"
    c4 = manual["hechos_vs_supuestos"]["valor"]
    if usadas_no_fiables and c4 == "SI":
        c4 = "PARCIAL"
    crit = {k: manual[k]["valor"] for k in MANUALES}
    crit["hechos_vs_supuestos"] = c4
    crit.update(categorias_revisadas=c2, datos_para_priorizar=c8, respuesta_negocio_completo=c10)

    # Una cobertura declarada como SI que los datos contradicen es un error, no una opinión.
    for k, v in d.get("declarado", {}).items():
        if k in crit and v == "SI" and crit[k] != "SI":
            errores.append(f"se declara '{k}' = SI pero los datos dan {crit[k]}")

    criticos = CRITICOS[d["alcance_decision"]]
    if errores or any(crit[k] == "NO" for k in criticos):
        resultado = "HOLD"
    elif any(crit[k] == "PARCIAL" for k in criticos) or any(v != "SI" for v in crit.values()) or usadas_no_fiables:
        resultado = "CONDITIONAL"
    else:
        resultado = "PASS"

    sin_revisar = [c["nombre"] for c in cats if not c.get("revisada")]
    sin_datos = {c["nombre"]: [x for x in DATOS_PRIORIZAR + INVENTARIO
                               if c.get("datos", {}).get(x, "UNKNOWN") not in FIABLES] for c in cats}
    sin_datos = {k: v for k, v in sin_datos.items() if v}
    preguntas = _preguntas(crit, cats, sin_revisar, sin_datos, d["alcance_decision"], d.get("preguntas_extra", []))
    return {
        "empresa": d["empresa"], "decision": d["decision"], "alcance_decision": d["alcance_decision"],
        "resultado": resultado, "criterios": crit, "errores": errores,
        "afirmaciones_no_fiables_usadas": usadas_no_fiables,
        "categorias_sin_revisar": sin_revisar, "categorias_sin_datos": sin_datos, "preguntas": preguntas,
    }


def _preguntas(crit, cats, sin_revisar, sin_datos, alcance, extra):
    p = []
    if crit["decisores"] != "SI":
        p.append(("Quién decide y aprueba el gasto", "sin decisor no hay propuesta ni cobro posibles"))
    if crit["objetivos"] != "SI":
        p.append(("Qué tendría que pasar en 30 días para que valga la pena (con número)", "define el criterio de éxito"))
    if alcance == "empresa_completa":
        p.append(("Qué categorías o líneas vende hoy, sin sugerirlas, y cuáles dejaron más dinero el último mes",
                  "confirma el alcance real del negocio antes de priorizar"))
        for n in sin_revisar:
            p.append((f"¿'{n}' es una línea comercial activa? Unidades, precio y costo del último mes",
                      "solo hay referencia declarada, no datos comerciales"))
        for n, faltan in sin_datos.items():
            if n not in sin_revisar:
                p.append((f"{n}: {', '.join(faltan)} del último mes", "sin esto no se puede priorizar con rentabilidad"))
    p.append(("Capacidad de inversión y caja libre al mes tras reponer inventario", "define qué solución es sostenible"))
    p.extend((q, "dato pedido por el proyecto") for q in extra)
    return [{"prioridad": i + 1, "pregunta": q, "por_que": w} for i, (q, w) in enumerate(p)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("archivo")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.archivo, encoding="utf-8") as f:
            r = evaluar(json.load(f))
    except (OSError, json.JSONDecodeError, EntradaInvalida, KeyError) as e:
        print(f"ENTRADA INVÁLIDA: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"BSCG {r['resultado']} · {r['empresa']} · decisión: {r['decision']} ({r['alcance_decision']})")
        print("Criterios:", ", ".join(f"{k}={v}" for k, v in r["criterios"].items()))
        for e in r["errores"]:
            print("ERROR:", e)
        if r["categorias_sin_revisar"]:
            print("Categorías sin revisar:", ", ".join(r["categorias_sin_revisar"]))
        for n, f in r["categorias_sin_datos"].items():
            print(f"Sin datos · {n}: {', '.join(f)}")
        for q in r["preguntas"]:
            print(f"  {q['prioridad']}. {q['pregunta']}  [{q['por_que']}]")
    return {"PASS": 0, "CONDITIONAL": 10, "HOLD": 20}[r["resultado"]]


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
