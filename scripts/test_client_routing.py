"""Pruebas del enrutamiento por proyecto, dominio y verificacion (sin Orca, sin IA, sin red)."""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("altiora_orca_dispatch", ROOT / "scripts" / "orca-dispatch.py")
assert SPEC is not None and SPEC.loader is not None
dispatcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dispatcher)
from preambra_v2_routing import decide_mode, risk_signals  # noqa: E402

CAROUSEL = "Produce el carrusel C1 de 6 láminas con Pillow, caption y texto alternativo; no publicar"


class RiskTest(unittest.TestCase):
    def test_negated_publish_is_not_critical(self):
        for msg in ("no publicar", "sin publicar nada", "Nunca borrar archivos", "no se debe eliminar el original"):
            self.assertEqual(risk_signals(msg), [], msg)

    def test_affirmative_publish_is_critical(self):
        self.assertEqual(risk_signals("Publicar el carrusel hoy"), ["publicar"])
        self.assertEqual(risk_signals("Desplegar en producción"), ["desplegar", "en producción"])

    def test_negation_does_not_hide_a_real_risk(self):
        self.assertEqual(risk_signals("No tocar el CSS pero borrar la base de datos"), ["borrar"])

    def test_mixed_negations_and_imperatives(self):
        # V3: imperativos, push/merge, secretos y negaciones que no cruzan otro verbo ni otra clausula.
        cases = {
            "sin revisar publicar en vivo": ["publicar"],
            "no borres nada pero publica el post": ["publica"],
            "no esperes: borra el repo": ["borra"],
            "elimina los archivos": ["elimina"],
            "haz push a main": ["push"],
            "sube el .env al repo": [".env"],
            "instala graphify": ["instala"],
            "no te olvides de publicar": ["publicar"],
        }
        for msg, expected in cases.items():
            self.assertEqual(risk_signals(msg), expected, msg)
        for msg in ("no hagas push", "no instales nada ni gastes", "Redacta el borrador del carrusel",
                    "ahorro de tokens en la sesion", "envío de quesos a la GAM"):
            self.assertEqual(risk_signals(msg), [], msg)

    def test_production_of_content_is_not_critical(self):
        self.assertEqual(risk_signals("Producción de 4 carruseles"), [])

    def test_decide_mode_reports_signals(self):
        streams = dispatcher.classify_message(CAROUSEL, projects={})
        d = decide_mode(CAROUSEL, streams)
        self.assertEqual(d["risk"], "standard")
        self.assertEqual(d["risk_signals"], [])
        self.assertFalse(d["requires_human_approval"])


class DomainTest(unittest.TestCase):
    def test_carousel_task_is_client_content_not_nextjs(self):
        streams = dispatcher.classify_message(CAROUSEL, projects={})
        self.assertEqual([s["domain"] for s in streams], ["client-content"])
        spec = streams[0]["spec"]
        self.assertNotIn("npm run check", spec)
        self.assertNotIn("components/", spec)
        self.assertNotIn("nextjs-architecture", spec)

    def test_web_task_keeps_web_domain_and_npm_check(self):
        streams = dispatcher.classify_message("Crear componente React con Tailwind para la landing", projects={})
        self.assertEqual(streams[0]["domain"], "brand-copy-frontend")
        self.assertIn("npm run check", streams[0]["spec"])

    def test_short_keywords_need_word_boundaries(self):
        self.assertFalse(dispatcher.keyword_hit("ui", "construir una estrategia"))
        self.assertTrue(dispatcher.keyword_hit("ui", "mejorar la ui del panel"))

    def test_mixed_web_and_content_keeps_both(self):
        streams = dispatcher.classify_message("Carrusel para Instagram y componente React de la landing", projects={})
        self.assertEqual({s["domain"] for s in streams}, {"client-content", "brand-copy-frontend"})


class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "projects.json"
        path.write_text(json.dumps({
            "demo": {"keywords": ["demo-cliente"], "owned_paths": ["clientes/demo/produccion/"],
                     "verification": "python validar.py"},
        }), encoding="utf-8")
        self.projects = dispatcher.load_projects(str(path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_project_overrides_paths_and_verification(self):
        streams = dispatcher.classify_message("Revisar el calendario de demo-cliente", projects=self.projects)
        self.assertEqual(len(streams), 1)
        s = streams[0]
        self.assertEqual((s["domain"], s["project"]), ("client-content", "demo"))
        self.assertIn("clientes/demo/produccion/", s["spec"])
        self.assertIn("python validar.py", s["spec"])
        self.assertNotIn("npm run check", s["spec"])

    def test_missing_or_broken_projects_file_is_ignored(self):
        self.assertEqual(dispatcher.load_projects(str(Path(self.tmp.name) / "no-existe.json")), {})
        bad = Path(self.tmp.name) / "bad.json"
        bad.write_text("{no es json", encoding="utf-8")
        self.assertEqual(dispatcher.load_projects(str(bad)), {})


if __name__ == "__main__":
    unittest.main()
