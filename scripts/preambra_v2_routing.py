"""PREAMBRA OS V2: deterministic, plan-only mode selection and handoff contracts.

Designed to augment the established Altiora dispatcher without importing or running
any provider CLI. No network, no worker launch, no file writes.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import PurePosixPath
from typing import Any

MODES = ("A", "B", "C", "D")
OWNERS = ("codex", "claude", "antigravity")
STATUSES = ("PLANNED", "READY", "IN_PROGRESS", "REVIEW", "APPROVED", "DONE",
            "BLOCKED", "FAILED", "CANCELED")

# Signal-based, conservative policy. This does not constitute an AI quality score.
CRITICAL = re.compile(
    r"\b(?:seguridad|owasp|vulnerabilid\w*|contrato\w*|legal(?:es)?|"
    r"impuest\w*|pago\w*|cobro\w*|finanz\w*|datos personales|"
    r"producci[oó]n|publicar|publicaci[oó]n|borrar|eliminar)\b",
    re.IGNORECASE,
)
SUBSTANTIAL = re.compile(
    r"\b(?:crear|desarrollar|implementar|integrar|auditar|investigar|"
    r"refactorizar|dise[nñ]ar|redise[nñ]ar|desplegar|revisar|"
    r"arquitectura|automatizar|estrategia|construir|evaluar)\b",
    re.IGNORECASE,
)
INDEPENDENT = re.compile(
    r"(?:\ben paralelo\b|\bparaleliz\w*\b|\bindependient\w*\b|"
    r"\bsimult[aá]ne\w*\b|\bsin dependencias\b)",
    re.IGNORECASE,
)
INTEGRAL = re.compile(
    r"(?:\bproyecto integral\b|\bproyecto completo\b|"
    r"\bde principio a fin\b|\bextremo a extremo\b|"
    r"\bdesde el diagn[oó]stico hasta\b|\bdel diagn[oó]stico al lanzamiento\b)",
    re.IGNORECASE,
)


def _path(raw: str) -> str:
    """Canonicalize relative paths conservatively for overlap checks."""
    raw = raw.replace("\\", "/").strip()
    if not raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise ValueError("owned_path must be a nonempty, relative repository path")
    parts = PurePosixPath(raw).parts
    if any(p in ("..", "~") for p in parts):
        raise ValueError("owned_path must not traverse outside the repository")
    return "/".join(p for p in parts if p != ".")


def overlapping_paths(streams: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Find writer collisions, including parent/child directory ownership."""
    claims: list[tuple[int, str]] = []
    for index, stream in enumerate(streams, start=1):
        for raw in stream.get("owned_paths", []):
            claims.append((index, _path(str(raw))))
    collisions: list[dict[str, Any]] = []
    for i, (ai, a) in enumerate(claims):
        for bi, b in claims[i + 1:]:
            if ai == bi:
                continue
            if a == b or a.startswith(b.rstrip("/") + "/") or b.startswith(a.rstrip("/") + "/"):
                collisions.append({"stream_a": ai, "stream_b": bi, "path_a": a, "path_b": b})
    return collisions


def _has_dependencies(streams: list[dict[str, Any]]) -> bool:
    return any(bool(s.get("depends_on")) for s in streams)


def _lead(streams: list[dict[str, Any]], entrypoint: str) -> str:
    preferred = streams[0].get("preferred_ai") if streams else ""
    if preferred in OWNERS:
        return str(preferred)
    return entrypoint if entrypoint in OWNERS else "codex"


def decide_mode(message: str, streams: list[dict[str, Any]], entrypoint: str = "current") -> dict[str, Any]:
    """Select mode conservatively. C is permitted only with explicit independence."""
    if not message.strip():
        raise ValueError("The job description cannot be empty")
    collisions = overlapping_paths(streams)
    dependent = _has_dependencies(streams)
    critical = bool(CRITICAL.search(message))
    high_scope = bool(INTEGRAL.search(message))
    parallel_request = bool(INDEPENDENT.search(message))
    separate = len(streams) > 1 and not collisions and not dependent
    lead = _lead(streams, entrypoint)
    reviewer = "codex" if lead != "codex" else "claude"

    if high_scope:
        mode, reason = "D", "Multi-phase business engagement requires phase gates."
    elif parallel_request and separate and not critical:
        mode, reason = "C", "Independent tasks and non-overlapping write paths explicitly requested."
    elif critical or len(streams) > 1 or bool(SUBSTANTIAL.search(message)):
        mode, reason = "B", "Substantial or high-impact work needs construction and independent review."
    else:
        mode, reason = "A", "Small, narrow task: avoid unnecessary delegation."

    warnings: list[str] = []
    if parallel_request and mode != "C":
        if collisions:
            warnings.append("Parallel execution rejected: overlapping owned_paths.")
        if dependent:
            warnings.append("Parallel execution rejected: dependency order must be respected.")
        if critical:
            warnings.append("Parallel execution requires additional authorization for critical risk.")
    if len(streams) > 1 and not parallel_request:
        warnings.append("Multiple domains detected; execution is sequential unless independence is proved.")

    return {
        "mode": mode,
        "reason": reason,
        "entrypoint": entrypoint,
        "lead_candidate": lead,
        "reviewer_candidate": reviewer if mode in ("B", "C", "D") else None,
        "risk": "critical" if critical else ("elevated" if high_scope else "standard"),
        "parallel_requested": parallel_request,
        "parallel_safe": bool(separate and not critical),
        "has_dependencies": dependent,
        "path_collisions": collisions,
        "orca_policy": "OPTIONAL_AFTER_RUNTIME_VERIFICATION" if mode in ("C", "D") else "NOT_REQUIRED",
        "model_observed": "UNKNOWN",
        "execution_status": "PLAN_ONLY",
        "requires_human_approval": critical or high_scope,
        "warnings": warnings,
    }


def make_handoffs(message: str, streams: list[dict[str, Any]], decision: dict[str, Any]) -> list[dict[str, Any]]:
    """Create contracts, never auto-create worktrees, workers or tasks."""
    job_id = "PRE-" + hashlib.sha256(message.encode("utf-8")).hexdigest()[:12].upper()
    contracts = []
    for i, stream in enumerate(streams, start=1):
        owner = stream.get("preferred_ai", "codex")
        contracts.append({
            "schema_version": "2.0",
            "job_id": f"{job_id}-{i:02}",
            "brand": "PREAMBRA",
            "technical_system": "Altiora",
            "goal": stream.get("objective") or stream.get("title") or message,
            "mode": decision["mode"],
            "owner": owner,
            "reviewer": decision["reviewer_candidate"] if decision["reviewer_candidate"] != owner else None,
            "model_observed": "UNKNOWN",
            "reasoning_effort_candidate": stream.get("effort", "medium"),
            "tool_access": {"orca": "UNKNOWN", "agent_session": "UNKNOWN"},
            "inputs": [],
            "owned_paths": stream.get("owned_paths", []),
            "dependencies": stream.get("depends_on", []),
            "acceptance": ["Acceptance criteria must be specified before execution",
                           "Evidence-backed QA required before DONE"],
            "max_correction_attempts": 2,
            "budget_limit": "REQUIRES_APPROVAL",
            "artifacts": [],
            "checks": [],
            "status": "PLANNED",
            "evidence": [],
            "risks": ["Execution is not authorized by the planning output"],
            "next_action": "VERIFY_RUNTIME_AND_APPROVE_SCOPE",
        })
    return contracts


def validate_contract(contract: dict[str, Any]) -> list[str]:
    """Cheap standalone integrity checks; no implicit action permissions."""
    errors: list[str] = []
    required = ("schema_version", "job_id", "brand", "goal", "mode", "owner",
                "model_observed", "reasoning_effort_candidate", "owned_paths", "acceptance",
                "status", "evidence", "budget_limit")
    for key in required:
        if key not in contract:
            errors.append(f"missing required field: {key}")
    if contract.get("mode") not in MODES:
        errors.append("invalid workflow mode")
    if contract.get("owner") not in OWNERS:
        errors.append("unknown owner")
    if contract.get("status") not in STATUSES:
        errors.append("invalid status")
    if contract.get("status") == "DONE" and not contract.get("evidence"):
        errors.append("DONE requires nonempty evidence")
    if contract.get("status") == "DONE" and not contract.get("checks"):
        errors.append("DONE requires checks")
    if not isinstance(contract.get("owned_paths"), list):
        errors.append("owned_paths must be a list")
    else:
        for path in contract["owned_paths"]:
            try:
                _path(str(path))
            except ValueError as error:
                errors.append(str(error))
    return errors
