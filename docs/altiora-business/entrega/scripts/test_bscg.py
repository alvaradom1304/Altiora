"""Regresión del BSCG. Caso obligatorio: El Tilichero (2026-11-03).

El incidente: existía una campaña destacada de audífonos, pero el negocio tiene categorías
adicionales conocidas. El sistema debe reconocer que la campaña no representa a toda la empresa,
nombrar las categorías sin cubrir y pedir los datos comerciales antes de priorizar.
Las entradas de incidente están congeladas aquí a propósito: no dependen de los datos vivos.
"""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import bscg  # noqa: E402

VIVO = AQUI.parents[3] / "projects" / "tilicheros" / "COBERTURA-NEGOCIO.json"
SIN_DATOS = {"ventas": "UNKNOWN", "margen": "UNKNOWN", "inventario": "UNKNOWN"}
OK_MANUAL = {k: {"valor": "SI", "evidencia": "x"} for k in bscg.MANUALES}


def incidente_tilichero():
    """Estado de conocimiento cuando se priorizaba por la campaña de audífonos."""
    cat = lambda n, rev: {"nombre": n, "origen_declaracion": "REPORTED", "fuente": "fundador",
                          "fuente_tipo": "declaracion", "revisada": rev, "datos": dict(SIN_DATOS)}
    return {
        "empresa": "El Tilichero CR", "decision": "Qué categoría impulsar", "alcance_decision": "empresa_completa",
        "criterios_manuales": copy.deepcopy(OK_MANUAL),
        "categorias": [cat("Gaming", False), cat("Tecnología", True), cat("Bebés", False), cat("Anime", False)],
        "afirmaciones": [{"texto": "Los audífonos son la categoría que más vende", "estado": "INFERRED",
                          "fuente": "campaña", "fuente_tipo": "documento", "usada_en_decision": True}],
        "declarado": {"categorias_revisadas": "SI", "respuesta_negocio_completo": "SI"},
    }


def negocio_completo():
    cat = lambda n: {"nombre": n, "origen_declaracion": "VERIFIED", "fuente": "libro de ventas",
                     "fuente_tipo": "documento", "fuente_tipo_datos": "documento", "revisada": True,
                     "datos": {"ventas": "VERIFIED", "margen": "REPORTED", "inventario": "REPORTED"}}
    return {"empresa": "Sintética S.A.", "decision": "Priorizar", "alcance_decision": "empresa_completa",
            "criterios_manuales": copy.deepcopy(OK_MANUAL), "categorias": [cat("A"), cat("B")], "afirmaciones": []}


class RegresionTilichero(unittest.TestCase):
    def test_la_campana_no_representa_a_toda_la_empresa(self):
        r = bscg.evaluar(incidente_tilichero())
        self.assertNotEqual(r["resultado"], "PASS")
        self.assertEqual(r["resultado"], "HOLD")

    def test_identifica_las_categorias_sin_cubrir(self):
        r = bscg.evaluar(incidente_tilichero())
        self.assertEqual(set(r["categorias_sin_revisar"]), {"Gaming", "Bebés", "Anime"})

    def test_rechaza_declarar_cobertura_que_los_datos_contradicen(self):
        r = bscg.evaluar(incidente_tilichero())
        self.assertTrue(any("categorias_revisadas" in e for e in r["errores"]))
        self.assertTrue(any("respuesta_negocio_completo" in e for e in r["errores"]))

    def test_no_trata_una_inferencia_como_dato(self):
        r = bscg.evaluar(incidente_tilichero())
        self.assertEqual(r["afirmaciones_no_fiables_usadas"], ["Los audífonos son la categoría que más vende"])
        self.assertEqual(r["criterios"]["hechos_vs_supuestos"], "PARCIAL")

    def test_pide_los_datos_comerciales_antes_de_priorizar(self):
        preguntas = " ".join(q["pregunta"] for q in bscg.evaluar(incidente_tilichero())["preguntas"])
        for cat in ("Bebés", "Anime", "Gaming", "Tecnología"):
            self.assertIn(cat, preguntas)
        self.assertIn("categorías", preguntas)

    def test_pregunta_por_el_decisor_cuando_no_se_conoce(self):
        d = incidente_tilichero()
        d["criterios_manuales"]["decisores"]["valor"] = "NO"
        preguntas = [q["pregunta"] for q in bscg.evaluar(d)["preguntas"]]
        self.assertTrue(any(p.startswith("Quién decide") for p in preguntas))

    def test_aunque_todo_lo_manual_diga_si_los_datos_mandan(self):
        d = incidente_tilichero()
        d.pop("declarado")
        d["afirmaciones"] = []
        r = bscg.evaluar(d)
        self.assertEqual(r["criterios"]["datos_para_priorizar"], "NO")
        self.assertEqual(r["resultado"], "HOLD")


class ComportamientoGeneral(unittest.TestCase):
    def test_control_positivo_negocio_completo_pasa(self):
        self.assertEqual(bscg.evaluar(negocio_completo())["resultado"], "PASS")

    def test_un_criterio_no_critico_parcial_da_conditional(self):
        d = negocio_completo()
        d["criterios_manuales"]["alternativas"]["valor"] = "PARCIAL"
        self.assertEqual(bscg.evaluar(d)["resultado"], "CONDITIONAL")

    def test_decision_de_campana_solo_exige_sus_criticos(self):
        d = negocio_completo()
        d["alcance_decision"] = "campana"
        d["categorias"][1]["revisada"] = False
        r = bscg.evaluar(d)
        self.assertEqual(r["resultado"], "CONDITIONAL")
        self.assertEqual(r["criterios"]["categorias_revisadas"], "PARCIAL")

    def test_verified_sustentado_en_una_declaracion_es_error(self):
        d = negocio_completo()
        d["categorias"][0]["fuente_tipo"] = "declaracion"
        r = bscg.evaluar(d)
        self.assertEqual(r["resultado"], "HOLD")
        self.assertTrue(any("VERIFIED" in e for e in r["errores"]))

    def test_entrada_invalida(self):
        with self.assertRaises(bscg.EntradaInvalida):
            bscg.evaluar({"empresa": "x"})
        d = negocio_completo()
        d["categorias"][0]["origen_declaracion"] = "SEGURO"
        with self.assertRaises(bscg.EntradaInvalida):
            bscg.evaluar(d)

    def test_codigos_de_salida(self):
        casos = [(negocio_completo(), 0), (incidente_tilichero(), 20)]
        for datos, esperado in casos:
            with tempfile.TemporaryDirectory() as t:
                f = Path(t) / "e.json"
                f.write_text(json.dumps(datos), encoding="utf-8")
                p = subprocess.run([sys.executable, str(AQUI / "bscg.py"), str(f)], capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(p.returncode, esperado, p.stderr)


class DatosVivosDeElTilichero(unittest.TestCase):
    """Valida el archivo del proyecto, sin fijar su resultado: cambiará cuando responda el dueño."""

    def test_archivo_valido_sin_contradicciones_y_con_las_cuatro_categorias(self):
        r = bscg.evaluar(json.loads(VIVO.read_text(encoding="utf-8")))
        self.assertEqual(r["errores"], [])
        self.assertEqual(r["afirmaciones_no_fiables_usadas"], [])
        d = json.loads(VIVO.read_text(encoding="utf-8"))
        self.assertTrue({"Gaming", "Tecnología", "Bebés", "Anime"} <= {c["nombre"] for c in d["categorias"]})


if __name__ == "__main__":
    unittest.main()
