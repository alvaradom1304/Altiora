#!/usr/bin/env python3
"""
Altiora Automated Multi-AI Orca Dispatcher (scripts/orca-dispatch.py).

Recibe un único mensaje del usuario, clasifica los flujos de trabajo necesarios
usando el catálogo de skills de Altiora (.altiora/catalog.local.json), decide
automáticamente qué IA (codex, claude o antigravity) favorece cada flujo,
separa worktrees cuando hay trabajo paralelo de escritura y despacha las tareas
en Orca CLI.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from preambra_v2_routing import decide_mode, make_handoffs

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / ".altiora" / "catalog.local.json"
ORCHESTRATION_PATH = ROOT / ".altiora" / "orchestration.json"
HANDOFF_PATH = ROOT / ".altiora" / "handoff.json"
DEFAULT_ORCA_EXE = Path(r"C:\Users\Usuario\AppData\Local\Programs\orca\resources\bin\orca.exe")


DOMAIN_RULES: list[dict[str, Any]] = [
    {
        "domain": "strategy-finance-backend",
        "title": "Estrategia, Finanzas, Outbound B2B y Backend/Automatización",
        "agent": "codex",
        "orca_agent": "codex",
        "rationale": (
            "Codex destaca en razonamiento analítico, unit economics, pricing de US$10k, "
            "investigación B2B verificable, arquitectura backend/n8n, seguridad y validación estática."
        ),
        "keywords": [
            "estrategia", "precio", "pricing", "finanzas", "margen", "calculadora",
            "10000", "10k", "roi", "unit economics", "outbound", "prospeccion",
            "prospecting", "meddicc", "discovery", "b2b", "backend", "api", "n8n",
            "webhook", "automatizacion", "automation", "python", "script", "seguridad",
            "owasp", "base de datos", "arquitectura", "check", "test", "doctor",
        ],
        "default_skills": [
            "pricing",
            "unit-economics",
            "high-ticket-offer",
            "cold-outbound-system",
            "n8n-webhook-architect",
            "altiora-os-strategy",
        ],
        "owned_paths": [
            "docs/altiora-business/",
            "scripts/",
            ".altiora/",
            "app/api/",
        ],
    },
    {
        "domain": "brand-copy-frontend",
        "title": "Marca, Copywriting, Propuestas Comerciales y UI/Frontend Next.js",
        "agent": "claude",
        "orca_agent": "claude",
        "rationale": (
            "Claude Code destaca en narrativa de marca, copywriting persuasivo, anuncios Meta Ads, "
            "propuestas de alto ticket, sistemas de diseño y componentes UI en React/Next.js."
        ),
        "keywords": [
            "marca", "brand", "branding", "copy", "copywriting", "texto", "mensaje",
            "storytelling", "propuesta", "proposal", "seguimiento", "follow-up",
            "objeciones", "meta ads", "anuncio", "campaña", "landing", "ui", "ux",
            "componente", "react", "nextjs", "next.js", "tailwind", "css", "layout",
            "cro", "conversion", "tipografia", "color", "diseño",
        ],
        "default_skills": [
            "premium-branding",
            "copywriting",
            "conversion-ux",
            "nextjs-architecture",
            "vercel-react-best-practices",
            "meta-ads-growth",
            "sales-proposal",
        ],
        "owned_paths": [
            "components/",
            "app/",
            "docs/altiora-Portfolio/",
        ],
    },
    {
        "domain": "immersive-3d-qa",
        "title": "Web Inmersiva 3D/WebGL, Motion GSAP y Auditoría Visual en Navegador",
        "agent": "antigravity",
        "orca_agent": "antigravity",
        "rationale": (
            "Antigravity + Orca Browser cubren escenas 3D (Three.js/R3F), shaders, tipografía cinética, "
            "scroll/GSAP, performance WebGL e inspección visual en vivo."
        ),
        "keywords": [
            "3d", "webgl", "three", "threejs", "r3f", "shader", "glsl", "canvas",
            "gsap", "scroll", "lenis", "motion", "animacion", "inmersiv", "cursor",
            "buttermax", "particulas", "postprocessing", "fps", "navegador", "browser",
            "captura", "screenshot", "visual", "accesibilidad", "a11y", "lighthouse",
        ],
        "default_skills": [
            "immersive-interaction-lab",
            "elite-web-experience-os",
            "threejs-experience",
            "react-three-fiber",
            "gsap-animation",
            "scroll-experience",
            "web-quality-assurance",
        ],
        "owned_paths": [
            "components/3d/",
            "components/AtmosphericCanvasOverlay.tsx",
            "public/",
        ],
    },
    {
        "domain": "cloud-data-engineering",
        "title": "Google Cloud, BigQuery, Pipelines y Data Intelligence",
        "agent": "antigravity",
        "orca_agent": "antigravity",
        "rationale": (
            "Antigravity y Codex operan el Google Cloud Data Agent Kit: BigQuery, Cloud Storage, "
            "pipelines Dataflow/Composer, bases Cloud SQL/Spanner, dbt y notebooks de datos."
        ),
        "keywords": [
            "google cloud", "gcp", "bigquery", "dataflow", "cloud storage", "gcs",
            "composer", "airflow", "spark", "dataproc", "dbt", "dataform", "spanner",
            "alloydb", "cloud sql", "firestore", "notebook", "lakehouse", "etl",
            "pipeline", "datos", "data", "warehouse", "dak",
        ],
        "default_skills": [
            "gcp-data-pipelines",
            "bigquery-data-transfer-service",
            "google-cloud-storage-bucket-architect",
            "dbt-bigquery",
            "dataform-bigquery",
            "cloud-databases-onboarding",
        ],
        "owned_paths": [
            "pipelines/",
            "data/",
            "sql/",
            "notebooks/",
        ],
    },
]


def resolve_orca_exe() -> str:
    if DEFAULT_ORCA_EXE.exists():
        return str(DEFAULT_ORCA_EXE)
    found = shutil.which("orca")
    if found:
        return found
    raise FileNotFoundError("No se encontró el binario de Orca CLI.")


def run_orca(args: list[str], timeout: int = 30) -> dict[str, Any]:
    orca_bin = resolve_orca_exe()
    cmd = [orca_bin, *args]
    if "--json" not in cmd:
        cmd.append("--json")
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    stdout = proc.stdout.strip()
    if not stdout:
        return {
            "ok": False,
            "exit_code": proc.returncode,
            "stderr": proc.stderr.strip(),
        }
    try:
        data = json.loads(stdout)
        data["exit_code"] = proc.returncode
        return data
    except json.JSONDecodeError:
        return {
            "ok": proc.returncode == 0,
            "exit_code": proc.returncode,
            "raw_stdout": stdout,
            "stderr": proc.stderr.strip(),
        }


def tokenize(text: str) -> list[str]:
    lowered = text.lower()
    return re.findall(r"[a-záéíóúñü0-9][a-záéíóúñü0-9._-]*", lowered)


def match_catalog_skills(message: str, domain_defaults: list[str], limit: int = 4) -> list[str]:
    if not CATALOG_PATH.exists():
        return domain_defaults[:limit]
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return domain_defaults[:limit]

    tokens = set(tokenize(message))
    scored: list[tuple[int, str]] = []
    seen: set[str] = set()

    for entry in catalog.get("skills", []):
        name = entry.get("name", "")
        if not name or name in seen:
            continue
        desc = (entry.get("description") or "").lower()
        score = 0
        for tok in tokens:
            if len(tok) < 3:
                continue
            if tok in name.lower():
                score += 6
            elif tok in desc:
                score += 2
        if name in domain_defaults:
            score += 3
        if score > 0:
            scored.append((score, name))
            seen.add(name)

    scored.sort(key=lambda item: (-item[0], item[1]))
    selected = [name for _, name in scored[:limit]]
    for default_skill in domain_defaults:
        if len(selected) >= limit:
            break
        if default_skill not in selected:
            selected.append(default_skill)
    return selected[:limit]


def classify_message(message: str) -> list[dict[str, Any]]:
    lowered = message.lower()
    matched_streams: list[dict[str, Any]] = []

    for rule in DOMAIN_RULES:
        hits = [kw for kw in rule["keywords"] if kw in lowered]
        if hits:
            matched_streams.append(
                {
                    "domain": rule["domain"],
                    "title": rule["title"],
                    "preferred_ai": rule["agent"],
                    "orca_worker_agent": rule["orca_agent"],
                    "rationale": rule["rationale"],
                    "matched_keywords": hits,
                    "score": len(hits),
                    "skills": match_catalog_skills(message, rule["default_skills"]),
                    "owned_paths": rule["owned_paths"],
                }
            )

    matched_streams.sort(key=lambda item: -item["score"])

    if not matched_streams:
        fallback = DOMAIN_RULES[0]
        matched_streams.append(
            {
                "domain": fallback["domain"],
                "title": fallback["title"],
                "preferred_ai": fallback["agent"],
                "orca_worker_agent": fallback["orca_agent"],
                "rationale": fallback["rationale"],
                "matched_keywords": ["general"],
                "score": 1,
                "skills": match_catalog_skills(message, fallback["default_skills"]),
                "owned_paths": fallback["owned_paths"],
            }
        )

    return finalize_streams(message, matched_streams)


def finalize_streams(message: str, streams: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Completa cada flujo: disponibilidad de la IA, worktree, esfuerzo y encargo para el worker."""
    total = len(streams)
    availability = load_ai_availability()
    for idx, stream in enumerate(streams, start=1):
        stream["stream_index"] = idx
        apply_availability(stream, availability)
        stream["worktree_strategy"] = "current" if total == 1 else "new-child"
        stream["worktree_name"] = (
            "current"
            if total == 1
            else f"wt-{stream['preferred_ai']}-{stream['domain'].split('-')[0]}"
        )
        skills_str = ", ".join(stream["skills"])
        paths_str = ", ".join(stream["owned_paths"])
        stream["task_title"] = f"[{stream['preferred_ai'].upper()}] {stream['title']}"
        # El enrutador por modelo ya trae el esfuerzo; la heurística solo se usa si falta.
        effort = stream.get("effort") or choose_effort(message, stream["domain"])
        stream["effort"] = effort
        codex_level = "xhigh" if effort == "max" else effort
        stream["effort_hint"] = EFFORT_HINTS[stream["preferred_ai"]].format(
            level=effort, level_codex=codex_level, model_hint=model_hint(stream["preferred_ai"], effort)
        )
        objective_line = f"Objetivo de este flujo: {stream['objective']}\n" if stream.get("objective") else ""
        if stream.get("depends_on"):
            deps = ", ".join(str(d) for d in stream["depends_on"])
            objective_line += f"Depende de los flujos: {deps}. Usa sus entregables como entrada; no inventes lo que ellos definen.\n"
        stream["spec"] = (
            f"Encargo del usuario: {message}\n"
            f"{objective_line}"
            f"Rol asignado: {stream['preferred_ai']} ({stream['title']}).\n"
            f"Esfuerzo de razonamiento sugerido: {effort}. {stream['effort_hint']}\n"
            f"Skills a consultar bajo demanda: {skills_str}.\n"
            f"Ámbito de archivos propios (un escritor por archivo): {paths_str}.\n"
            f"Verificación requerida antes de cerrar: npm run check."
        )

    return streams


# --- Enrutador por modelo de alto rendimiento -------------------------------------------
# Un modelo (Claude Sonnet por defecto, vía `claude -p` sin herramientas) estudia el
# encargo y decide flujos, IA, esfuerzo y skills. La salida se valida contra las reglas
# locales; si falla, se usa la heurística por palabras clave.

ROUTER_SCHEMA = {
    "type": "object",
    "properties": {
        "analysis": {"type": "string"},
        "streams": {
            "type": "array",
            "minItems": 1,
            "maxItems": 4,
            "items": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "enum": [r["domain"] for r in DOMAIN_RULES]},
                    "preferred_ai": {"type": "string", "enum": ["codex", "claude", "antigravity"]},
                    "effort": {"type": "string", "enum": ["low", "medium", "high", "xhigh", "max"]},
                    "objective": {"type": "string"},
                    "skills": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
                    "rationale": {"type": "string"},
                    "depends_on": {"type": "array", "items": {"type": "integer", "minimum": 1}},
                },
                "required": ["domain", "preferred_ai", "effort", "objective", "skills", "rationale", "depends_on"],
            },
        },
    },
    "required": ["analysis", "streams"],
}


def catalog_skill_names() -> set[str]:
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return set()
    return {e.get("name", "") for e in catalog.get("skills", []) if e.get("name")}


def build_router_prompt(message: str, availability: dict[str, Any]) -> str:
    domains = "\n".join(
        f"- {r['domain']} — {r['title']}. IA habitual: {r['agent']}. {r['rationale']} "
        f"Rutas propias: {', '.join(r['owned_paths'])}. Skills típicas: {', '.join(r['default_skills'])}."
        for r in DOMAIN_RULES
    )
    candidates = sorted(
        set(match_catalog_skills(message, [], limit=15))
        | {s for r in DOMAIN_RULES for s in r["default_skills"]}
    )
    blocked = [
        f"{ai} (hasta {info.get('exhausted_until')})"
        for ai, info in availability.items()
        if not is_available(ai, availability)
    ]
    return f"""Eres el director de enrutamiento de Altiora, una consultora de estrategia, marca, web inmersiva e IA.
Estudia el encargo con cuidado y decide cómo repartirlo entre tres IA trabajadoras.

IA disponibles y fortalezas:
- codex: razonamiento analítico, finanzas, pricing, backend, APIs, n8n, Python, seguridad y validación.
- claude: narrativa de marca, copywriting, propuestas comerciales, Meta Ads, UX y componentes React/Next.js.
- antigravity: escenas 3D/WebGL, shaders, GSAP/scroll, auditoría visual en navegador; también sirve como respaldo general con cuota independiente.
IA sin créditos ahora mismo (NO asignarlas): {', '.join(blocked) or 'ninguna'}.

Dominios válidos:
{domains}

Esfuerzo de razonamiento (elige por flujo, no por mensaje):
- low: tarea mecánica, corta y sin riesgo.
- medium: encargo concreto y acotado.
- high: diseño, arquitectura, auditoría, investigación o 3D.
- xhigh: consecuencias económicas, de datos, seguridad, producción o legales.
- max: solo si el usuario pide profundidad explícita o el riesgo es crítico.

Reglas:
- Elige el esfuerzo MÁS BAJO que cumpla el criterio de aceptación; sube solo con un motivo concreto del encargo.
- No asignes a antigravity tareas fuera de 3D/WebGL/shaders/GSAP/auditoría visual: razona caro. Úsalo fuera de ese dominio solo si codex y claude están sin créditos.
- Usa el mínimo número de flujos: uno si el encargo es de un solo dominio. Divide solo cuando haya trabajo realmente independiente.
- Cada flujo necesita un objetivo concreto y verificable, en español.
- 'depends_on' lista los números (empezando en 1, según el orden de 'streams') de los flujos cuyo resultado necesita este flujo antes de empezar; vacío si es independiente. Ordena los flujos para que las dependencias vayan antes.
- Elige skills SOLO de esta lista: {', '.join(candidates)}.
- Explica en 'analysis' qué pide realmente el usuario, qué riesgo tiene y por qué divides así.

Encargo del usuario:
<<<
{message}
>>>"""


def classify_with_model(message: str, model: str, effort: str) -> tuple[list[dict[str, Any]] | None, dict[str, Any]]:
    """Pide al modelo el plan de enrutado. Devuelve (flujos o None, metadatos del intento)."""
    meta: dict[str, Any] = {"router": "model", "model": model, "router_effort": effort}
    claude_bin = shutil.which("claude")
    if not claude_bin:
        meta["error"] = "CLI 'claude' no encontrado en el PATH"
        return None, meta

    availability = load_ai_availability()
    prompt = build_router_prompt(message, availability)
    cmd = [
        claude_bin, "-p",
        "--model", model,
        "--effort", effort,
        "--output-format", "json",
        "--json-schema", json.dumps(ROUTER_SCHEMA),
        "--tools", "",
        "--strict-mcp-config",
        "--no-session-persistence",
    ]
    try:
        # Se ejecuta fuera del repo para no cargar el CLAUDE.md del proyecto en el enrutador.
        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=300, cwd=os.environ.get("TEMP") or None,
        )
    except subprocess.TimeoutExpired:
        meta["error"] = "el enrutador superó 300 s"
        return None, meta

    try:
        envelope = json.loads(proc.stdout)
    except json.JSONDecodeError:
        meta["error"] = f"salida no JSON (exit {proc.returncode}): {proc.stdout[:300] or proc.stderr[:300]}"
        return None, meta

    meta["cost_usd"] = envelope.get("total_cost_usd")
    meta["model_used"] = next(iter(envelope.get("modelUsage", {}) or {}), None)
    plan = envelope.get("structured_output")
    if plan is None and isinstance(envelope.get("result"), str):
        try:
            plan = json.loads(envelope["result"])
        except json.JSONDecodeError:
            plan = None
    if not isinstance(plan, dict) or not plan.get("streams"):
        meta["error"] = "el modelo no devolvió un plan válido"
        return None, meta

    rules = {r["domain"]: r for r in DOMAIN_RULES}
    known_skills = catalog_skill_names()
    streams: list[dict[str, Any]] = []
    for item in plan["streams"]:
        rule = rules.get(item.get("domain"))
        ai = item.get("preferred_ai")
        if not rule or ai not in EFFORT_HINTS or item.get("effort") not in EFFORT_LEVELS:
            meta["error"] = f"flujo inválido descartado el plan: {item}"
            return None, meta
        skills = [s for s in item.get("skills", []) if not known_skills or s in known_skills]
        streams.append(
            {
                "domain": rule["domain"],
                "title": rule["title"],
                "preferred_ai": ai,
                "orca_worker_agent": ai,
                "rationale": item.get("rationale", ""),
                "objective": item.get("objective", ""),
                "matched_keywords": ["router:model"],
                "score": 0,
                "effort": item["effort"],
                "depends_on": [
                    d for d in item.get("depends_on", [])
                    if isinstance(d, int) and 1 <= d <= len(plan["streams"]) and d != len(streams) + 1
                ],
                "skills": skills or rule["default_skills"][:4],
                "owned_paths": rule["owned_paths"],
            }
        )
    meta["analysis"] = plan.get("analysis", "")
    return finalize_streams(message, streams), meta


# Niveles de esfuerzo válidos en Claude Code (`claude --effort`, verificado).
EFFORT_LEVELS = ["low", "medium", "high", "xhigh", "max"]

# Dominios donde un error sale caro (dinero, datos, producción, seguridad).
HIGH_STAKES_RE = re.compile(
    r"precio|pricing|pago|cobro|factura|finanz|margen|seguridad|owasp|produccion|producción|"
    r"datos|legal|contrato|10000|10k|unit economics|rentab"
)
# Trabajo de diseño, arquitectura o auditoría que pide razonamiento profundo.
DEEP_RE = re.compile(
    r"arquitect|auditor|diagnost|estrategia|rediseñ|refactor|integra|investiga|"
    r"compar|planific|oferta|diseñ"
)  # El tema (3D, WebGL, shaders) no sube el nivel por sí solo; lo sube lo que se pide.
# Peticiones explícitas de profundidad máxima.
MAX_RE = re.compile(r"exhaustiv|a fondo|máxim|maxim|profund[oa]|sin atajos")
# Tareas mecánicas: resumir, renombrar, formatear, comprobar.
LIGHT_RE = re.compile(r"resum|renombr|formate|ordena|lista|traduc|typo|ortograf|comprueba|check")


def choose_effort(message: str, domain: str) -> str:
    """Elige el esfuerzo de razonamiento según la consulta (heurística local, sin LLM)."""
    text = message.lower()
    words = len(text.split())
    level = 1  # medium por defecto (índice en EFFORT_LEVELS)

    if LIGHT_RE.search(text) and words <= 25 and not HIGH_STAKES_RE.search(text):
        level = 0  # low
    if DEEP_RE.search(text):
        level = max(level, 2)  # high
    # Las consecuencias económicas o de datos solo elevan el esfuerzo en dominios donde importan.
    stakes_domains = {"strategy-finance-backend", "cloud-data-engineering"}
    if domain in stakes_domains and HIGH_STAKES_RE.search(text):
        level = max(level, 3)  # xhigh
    if MAX_RE.search(text):
        level = 4  # max
    return EFFORT_LEVELS[level]


# Cómo transmitir el esfuerzo a cada worker. Solo se usan formas verificadas en esta PC:
# - claude: `claude --effort <level>` (verificado en la ayuda del CLI).
# - codex: `-c model_reasoning_effort=<level>` (clave aceptada por el CLI; codex no tiene 'max').
# - antigravity: `agy --model <id> --effort <level>` (verificado con `agy --help` y `agy models` el 2026-11-01).
EFFORT_HINTS = {
    "claude": "Aplícalo con `claude --effort {level}` si lanzas la sesión a mano. {model_hint}",
    "codex": "Aplícalo con `codex -c model_reasoning_effort={level_codex}` si el modelo lo admite. {model_hint}",
    "antigravity": "Aplícalo con `agy --effort {level}`. {model_hint}",
}

# Sugerencias orientativas revisadas 2026-11-17 con documentación oficial.
# Nunca equivalen a acceso real ni comparativas de calidad; confirmar modelos con el CLI.
# Fuente y matriz: docs/operations/MULTI-AI-CAPABILITY-ROUTING.md.
MODEL_HINTS = {
    "codex": {
        "low": "Candidato: GPT-6 Luna para tareas repetitivas; comprueba /model y acceso real.",
        "medium": "Candidato: GPT-6.2 Sol para trabajo diario; si no aparece, elige uno disponible y ajusta el esfuerzo.",
        "default": "Candidato: GPT-6.2 Astra para problemas difíciles, solo si está habilitado. Consulta /model.",
    },
    "claude": {
        "low": "Candidato: alias haiku, si está disponible; comprueba /model.",
        "medium": "Candidato: alias sonnet; no asumas qué versión resuelve el alias.",
        "default": "Considera alias opus para problemas exigentes, pero verifica disponibilidad y el esfuerzo admitido.",
    },
    "antigravity": {
        "low": "Candidato: Gemini 3.8 Flash; confirma el identificador con agy models.",
        "medium": "Candidato: Gemini 4 Hydrogen o Gemini 3.8 Flash; confirma disponibilidad.",
        "default": "Considera Gemini 4 Argon/Carbon o Orchestrator si está habilitado. Orchestrator tiene esfuerzo fijo. Confirma con agy models.",
    },
}

def model_hint(ai: str, effort: str) -> str:
    hints = MODEL_HINTS.get(ai)
    if not hints:
        return ""
    return hints.get(effort, hints["default"])

# Cadena de respaldo cuando una IA se queda sin créditos o cuota. Antigravity (Gemini) va al
# final para codex y claude: razona caro y sus fortalezas son 3D/visual, no el resto de dominios.
FALLBACK_CHAIN = {
    "codex": ["claude", "antigravity"],
    "claude": ["codex", "antigravity"],
    "antigravity": ["claude", "codex"],
}

# Frases que Codex, Claude y Antigravity muestran al agotar créditos o cuota (ampliable).
EXHAUSTED_RE = re.compile(
    r"you'?ve hit your usage limit|hit your usage limit|rate limit reached|"
    r"insufficient (credits|quota|funds)|quota (exceeded|exhausted)|out of credits|"
    r"cuota agotada|sin cr[eé]ditos disponibles",
    re.IGNORECASE,
)
# Ventana de bloqueo por defecto cuando el mensaje no trae fecha de reinicio.
DEFAULT_BLOCK_HOURS = 24


def load_ai_availability() -> dict[str, Any]:
    """Lee el estado de cuota por IA guardado en orchestration.json (ai_status)."""
    state = load_orchestration_state()
    return state.get("ai_status", {})


def is_available(ai: str, availability: dict[str, Any]) -> bool:
    info = availability.get(ai, {})
    until = info.get("exhausted_until")
    if not until:
        return True
    try:
        blocked_until = datetime.fromisoformat(until.replace("Z", "+00:00"))
    except ValueError:
        return True
    return datetime.now(timezone.utc) >= blocked_until


def apply_availability(stream: dict[str, Any], availability: dict[str, Any]) -> None:
    """Si la IA preferida está agotada, reasigna el flujo a la primera alternativa disponible."""
    preferred = stream["preferred_ai"]
    if is_available(preferred, availability):
        return
    for alt in FALLBACK_CHAIN.get(preferred, []):
        if is_available(alt, availability):
            stream["rerouted_from"] = preferred
            stream["preferred_ai"] = alt
            stream["orca_worker_agent"] = alt
            stream["reroute_reason"] = f"{preferred} no disponible ({availability.get(preferred, {}).get('reason', 'motivo no registrado')})"
            return
    stream["blocked"] = True
    stream["reroute_reason"] = "ninguna IA disponible; el flujo queda pendiente y no se lanza"


def mark_exhausted(ai: str, reason: str) -> None:
    """Registra en orchestration.json que una IA está sin créditos y hasta cuándo."""
    state = load_orchestration_state()
    if not state:
        return
    until = datetime.now(timezone.utc).timestamp() + DEFAULT_BLOCK_HOURS * 3600
    until_iso = datetime.fromtimestamp(until, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state.setdefault("ai_status", {})[ai] = {
        "exhausted_until": until_iso,
        "reason": reason,
        "detected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    ORCHESTRATION_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def watch_worker_for_exhaustion(handle: str, ai: str, seconds: int = 60) -> str | None:
    """Vigila la terminal del worker; si aparece un aviso de cuota, marca la IA como agotada."""
    import time

    deadline = time.time() + seconds
    while time.time() < deadline:
        res = run_orca(["terminal", "read", "--terminal", handle, "--limit", "200"], timeout=20)
        text = json.dumps(res, ensure_ascii=False)
        match = EXHAUSTED_RE.search(text)
        if match:
            mark_exhausted(ai, f"aviso detectado en la terminal: '{match.group(0)}'")
            return match.group(0)
        time.sleep(10)
    return None


def load_orchestration_state() -> dict[str, Any]:
    if ORCHESTRATION_PATH.exists():
        try:
            return json.loads(ORCHESTRATION_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def terminal_alive(handle: str | None) -> bool:
    # Un Run cuyo coordinador es una terminal cerrada rechaza task-create con consumer_fenced.
    return bool(handle) and bool(run_orca(["terminal", "show", "--terminal", handle]).get("ok"))


def ensure_orca_run(state: dict[str, Any], objective: str) -> tuple[str | None, str | None]:
    orca_cfg = state.get("orca", {})
    existing_run_id = orca_cfg.get("orca_run_id")
    existing_coord = orca_cfg.get("coordinator_handle")

    if existing_run_id:
        show_res = run_orca(["orchestration", "run-show", "--id", existing_run_id])
        if show_res.get("ok"):
            run_obj = show_res.get("result", {}).get("run", {})
            coord = run_obj.get("coordinator_handle") or existing_coord
            if run_obj.get("id") and terminal_alive(coord):
                return run_obj.get("id"), coord

    list_res = run_orca(["orchestration", "run-list"])
    if list_res.get("ok"):
        for run in list_res.get("result", {}).get("runs", []):
            if not run.get("legacy") and terminal_alive(run.get("coordinator_handle")):
                return run.get("id"), run.get("coordinator_handle")

    term_res = run_orca(["terminal", "list", "--worktree", "active"])
    if term_res.get("ok"):
        terms = [
            t for t in term_res.get("result", {}).get("terminals", [])
            if t.get("connected") and not t.get("orphaned")
        ]
        if terms:
            first_handle = terms[0].get("handle")
            if first_handle:
                create_res = run_orca(
                    [
                        "orchestration",
                        "run-create",
                        "--objective",
                        objective[:180],
                        "--from",
                        first_handle,
                    ]
                )
                if create_res.get("ok"):
                    new_run = create_res.get("result", {}).get("run", {})
                    return new_run.get("id"), new_run.get("coordinator_handle") or first_handle

    return None, None


def launch_worker(agent_id: str, stream: dict[str, Any]) -> dict[str, Any]:
    """Lanza un worker de Orca con el encargo; indica si es un reenvío por falta de cuota."""
    prompt_text = f"{stream['spec']}\n\nEjecuta tu flujo asignado y reporta hallazgos o cambios verificados."
    if stream.get("rerouted_from") or stream.get("reroute_reason"):
        prompt_text += f"\nNota: este encargo fue reasignado a {agent_id} por disponibilidad de la IA original."
    return run_orca(
        ["agent", "launch", "--agent", agent_id, "--surface", "terminal", "--prompt", prompt_text],
        timeout=30,
    )


def dispatch_to_orca(
    message: str,
    streams: list[dict[str, Any]],
    launch_workers: bool = False,
    watch_seconds: int = 60,
) -> dict[str, Any]:
    state = load_orchestration_state()
    run_id, coord_handle = ensure_orca_run(state, message)

    dispatched_tasks: list[dict[str, Any]] = []
    launched_terminals: list[dict[str, Any]] = []

    for stream in streams:
        task_record: dict[str, Any] = {
            "stream_index": stream["stream_index"],
            "preferred_ai": stream["preferred_ai"],
            "orca_worker_agent": stream["orca_worker_agent"],
            "worktree_strategy": stream["worktree_strategy"],
            "title": stream["task_title"],
            "skills": stream["skills"],
        }

        if run_id and coord_handle:
            create_cmd = [
                "orchestration",
                "task-create",
                "--task-title",
                stream["task_title"],
                "--spec",
                stream["spec"],
                "--run",
                run_id,
                "--from",
                coord_handle,
            ]
            create_res = run_orca(create_cmd)
            if create_res.get("ok"):
                task_obj = create_res.get("result", {}).get("task", {})
                task_id = task_obj.get("id")
                task_record["orca_task_id"] = task_id
                task_record["status"] = task_obj.get("status", "todo")
            else:
                task_record["orca_task_error"] = create_res

        if launch_workers and stream.get("blocked"):
            task_record["blocked"] = stream["reroute_reason"]
        elif launch_workers and stream.get("depends_on"):
            # No se lanza hasta que terminen sus dependencias; se relanza con un nuevo dispatch.
            task_record["waiting_on"] = stream["depends_on"]
            task_record["objective"] = stream.get("objective", "")
        elif launch_workers:
            agent_id = stream["orca_worker_agent"]
            launch_res = launch_worker(agent_id, stream)
            if launch_res.get("ok"):
                handle = launch_res.get("result", {}).get("outcome", {}).get("handle")
                task_record["worker_terminal_handle"] = handle
                launched_terminals.append(
                    {"agent": agent_id, "handle": handle, "domain": stream["domain"]}
                )
                # Vigila la cuota; si el worker se queda sin créditos, reenvía a otra IA.
                exhausted = watch_worker_for_exhaustion(handle, agent_id, watch_seconds)
                if exhausted:
                    task_record["failover"] = {"from": agent_id, "signal": exhausted}
                    availability = load_ai_availability()
                    apply_availability(stream, availability)
                    if stream.get("blocked") or stream["orca_worker_agent"] == agent_id:
                        task_record["failover_result"] = "sin alternativa disponible"
                    else:
                        relaunch = launch_worker(stream["orca_worker_agent"], stream)
                        new_handle = relaunch.get("result", {}).get("outcome", {}).get("handle")
                        task_record["failover_terminal_handle"] = new_handle
                        task_record["failover_agent"] = stream["orca_worker_agent"]
                        launched_terminals.append(
                            {
                                "agent": stream["orca_worker_agent"],
                                "handle": new_handle,
                                "domain": stream["domain"],
                            }
                        )
            else:
                task_record["worker_launch_error"] = launch_res

        dispatched_tasks.append(task_record)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if state:
        state["updated_at"] = now_iso
        state.setdefault("orca", {})
        if run_id:
            state["orca"]["orca_run_id"] = run_id
        if coord_handle:
            state["orca"]["coordinator_handle"] = coord_handle
        state["orca"]["last_auto_routing"] = {
            "timestamp": now_iso,
            "message": message,
            "streams": dispatched_tasks,
        }
        ORCHESTRATION_PATH.write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return {
        "orca_run_id": run_id,
        "coordinator_handle": coord_handle,
        "dispatched_tasks": dispatched_tasks,
        "launched_terminals": launched_terminals,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enrutador y despachador automático Multi-IA de Altiora sobre Orca."
    )
    parser.add_argument(
        "message",
        nargs="+",
        help="Mensaje único del usuario a analizar, dividir y despachar.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Registra automáticamente las tareas divididas en el Run activo de Orca.",
    )
    parser.add_argument(
        "--launch-workers",
        action="store_true",
        help="Además de crear las tareas, lanza las terminales de los agentes (codex/claude) en Orca.",
    )
    parser.add_argument(
        "--router",
        choices=["model", "heuristic"],
        default="heuristic",
        help="Heurística sin costo por defecto; `model` solicita una decisión explícita al LLM.",
    )
    parser.add_argument(
        "--entrypoint", choices=["current", "chatgpt", "codex", "claude", "antigravity"],
        default="current", help="IA desde la que se originó el encargo (metadata, no sesión autenticada).",
    )
    parser.add_argument(
        "--unavailable",
        action="append",
        default=[],
        help=(
            "IA no disponible (pausada, sin cuota o sin login); repetible o separada por comas. "
            "Se suma a PREAMBRA_UNAVAILABLE_AIS. El router no observa cuotas: solo respeta esta lista."
        ),
    )
    parser.add_argument(
        "--router-model",
        default="sonnet",
        help="Modelo del enrutador para `claude -p` (alias o id completo). Por defecto: sonnet.",
    )
    parser.add_argument(
        "--router-effort",
        default="medium",
        choices=["low", "medium", "high", "xhigh", "max"],
        help="Esfuerzo de razonamiento del propio enrutador. Por defecto: medium.",
    )
    parser.add_argument(
        "--watch-seconds",
        type=int,
        default=60,
        help="Segundos que se vigila cada worker lanzado para detectar falta de créditos y reenviar a otra IA.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime el resultado completo en formato JSON.",
    )
    args = parser.parse_args()

    # Modo solo plan (decisión del 01/11/2026): registrar o lanzar exige ALTIORA_DISPATCH_EXECUTE=1.
    if (args.execute or args.launch_workers) and os.environ.get("ALTIORA_DISPATCH_EXECUTE") != "1":
        print(
            "Modo solo plan: --execute y --launch-workers están desactivados. "
            "Delega desde Orca eligiendo la IA (orca worktree create --agent ...). "
            "Para reactivarlos en una ejecución: ALTIORA_DISPATCH_EXECUTE=1.",
            file=sys.stderr,
        )
        return 2

    full_message = " ".join(args.message).strip()
    router_meta: dict[str, Any] = {"router": "heuristic"}
    streams = None
    if args.router == "model":
        streams, router_meta = classify_with_model(full_message, args.router_model, args.router_effort)
        if streams is None:
            router_meta["fallback"] = "heuristic"
    if streams is None:
        streams = classify_message(full_message)

    result: dict[str, Any] = {
        "ok": True,
        "router": router_meta,
        "message": full_message,
        "stream_count": len(streams),
        "parallel_worktrees": False,
        "streams": streams,
    }
    unavailable = [
        name.strip()
        for raw in [os.environ.get("PREAMBRA_UNAVAILABLE_AIS", ""), *args.unavailable]
        for name in raw.split(",")
        if name.strip()
    ]
    try:
        decision = decide_mode(full_message, streams, entrypoint=args.entrypoint, unavailable=unavailable)
    except ValueError as error:
        print(f"V2: {error}", file=sys.stderr)
        return 2
    result["policy_v2"] = decision
    result["handoffs"] = make_handoffs(full_message, streams, decision)
    # V2 only recommends parallelism when independent tasks and paths are safe.
    result["parallel_worktrees"] = decision["mode"] == "C"

    # Orca cannot infer real worktree isolation from a planning flag.
    # Fail closed instead of launching multiple workers onto the same checkout.
    if args.launch_workers and (
        decision["mode"] in ("A", "D")
        or any(st.get("worktree_strategy") == "new-child" for st in streams)
    ):
        print("V2: lanzamiento bloqueado. Esta modalidad requiere fases o worktrees reales y verificados; solo planificar.", file=sys.stderr)
        return 2

    if args.execute or args.launch_workers:
        dispatch_info = dispatch_to_orca(
            full_message,
            streams,
            launch_workers=args.launch_workers,
            watch_seconds=args.watch_seconds,
        )
        result["orca_dispatch"] = dispatch_info

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print("=== PREAMBRA OS V2 | ALTIORA ORCA ROUTER ===")
    print(f"Modalidad propuesta: {decision['mode']} | Riesgo: {decision['risk']} | Orca: {decision['orca_policy']}")
    for warning in decision["warnings"]:
        print(f"  AVISO: {warning}")
    print(f"Mensaje: {full_message}")
    if router_meta.get("router") == "model" and not router_meta.get("fallback"):
        print(f"Enrutador: {router_meta.get('model_used') or router_meta.get('model')} "
              f"(esfuerzo {router_meta.get('router_effort')}, coste US${router_meta.get('cost_usd')})")
        print(f"Análisis: {router_meta.get('analysis')}")
    elif router_meta.get("fallback"):
        print(f"Enrutador: heurística (el modelo falló: {router_meta.get('error')})")
    else:
        print("Enrutador: heurística por palabras clave")
    print(
        f"Flujos detectados: {len(streams)} "
        f"({'Paralelo en worktrees separados' if len(streams) > 1 else 'Ejecución directa focalizada'})"
    )
    print("-" * 60)
    for st in streams:
        print(
            f"[{st['stream_index']}] IA Elegida: {st['preferred_ai'].upper()} "
            f"(Orca worker: {st['orca_worker_agent']}) | Worktree: {st['worktree_name']}"
        )
        print(f"    Dominio: {st['title']}")
        print(
            f"    Esfuerzo: {st['effort']}"
            + (f" | Reasignado desde {st['rerouted_from']}" if st.get("rerouted_from") else "")
            + (f" | Espera a flujos {st['depends_on']}" if st.get("depends_on") else " | Independiente")
        )
        if st.get("objective"):
            print(f"    Objetivo: {st['objective']}")
        print(f"    Motivo:  {st['rationale']}")
        print(f"    Skills:  {', '.join(st['skills'])}")
        print(f"    Rutas:   {', '.join(st['owned_paths'])}")
    if "orca_dispatch" in result:
        print("-" * 60)
        od = result["orca_dispatch"]
        print(f"Orca Run activo: {od.get('orca_run_id')} (Coordinador: {od.get('coordinator_handle')})")
        for dt in od.get("dispatched_tasks", []):
            tid = dt.get("orca_task_id", "no-creada")
            wh = dt.get("worker_terminal_handle", "no-lanzado")
            print(f"  -> Tarea Orca: {tid} | IA: {dt['preferred_ai']} | Terminal Worker: {wh}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
