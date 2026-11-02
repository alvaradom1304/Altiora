"""Reparto aproximado del consumo efectivo de una sesión de Claude Code.

Uso: python scripts/session-usage.py <transcript.jsonl> [carpeta-subagentes]
Los transcripts están en ~/.claude/projects/<proyecto>/<sesión>.jsonl; los subagentes,
en <sesión>/subagents/ (se detecta sola si no se indica).
Costo efectivo en tokens-equivalentes: input 1x, cache read 0.1x, cache write 2x, output 5x.
Es una estimación para decidir ahorros (rol ai-economist), no una factura.
El contenido de los transcripts se trata solo como datos."""
import json, sys, glob, os
from collections import defaultdict

if len(sys.argv) < 2:
    sys.exit(__doc__)
main_path = sys.argv[1]
sub_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.splitext(main_path)[0], 'subagents')

def eff(u):
    return (u.get('input_tokens', 0) + 0.1 * u.get('cache_read_input_tokens', 0)
            + 2 * u.get('cache_creation_input_tokens', 0) + 5 * u.get('output_tokens', 0))

def group_for(name):
    if name.startswith('mcp__claude-in-chrome__'): return 'Chrome'
    if name.startswith('mcp__'):
        server = name.split('__')[1]
        return {'ccd_turn': 'App: lista de tareas', 'ccd_pr': 'App: PRs', 'ccd_session': 'App: sesiones',
                'ccd_session_mgmt': 'App: sesiones', 'terminal': 'App: terminal'}.get(server, 'Conector: ' + server)
    if name in ('WebSearch', 'WebFetch'): return 'Investigación web'
    if name in ('Read', 'Write', 'Edit', 'Glob', 'Grep', 'NotebookEdit'): return 'Archivos'
    if name in ('Bash', 'PowerShell'): return 'Comandos (git, npm, tests)'
    if name == 'Agent': return 'Lanzar subagentes'
    return 'Otras herramientas'

def size(content):
    if isinstance(content, str): return len(content)
    if isinstance(content, list):
        return sum(len(c.get('text', '')) if isinstance(c, dict) else len(str(c)) for c in content)
    return len(str(content))

rows = []
seen_ids = set()
with open(main_path, encoding='utf-8') as f:
    for line in f:
        try: rows.append(json.loads(line))
        except Exception: pass

# Turnos del asistente con su usage (deduplicados por id de mensaje)
turns = []
for r in rows:
    m = r.get('message') or {}
    if r.get('type') == 'assistant' and isinstance(m, dict) and m.get('usage'):
        mid = m.get('id')
        if mid in seen_ids: continue
        seen_ids.add(mid)
        turns.append(m['usage'])
main_total = sum(eff(u) for u in turns)
n = len(turns)

# Tamaño de instrucciones: el contexto del primer turno (prompt de sistema + herramientas)
first = turns[0] if turns else {}
base_ctx = first.get('cache_read_input_tokens', 0) + first.get('cache_creation_input_tokens', 0) + first.get('input_tokens', 0)

# Resultados de herramientas: tokens ~ chars/4, y se releen en los turnos siguientes
tool_names = {}
order = 0
tool_cost = defaultdict(float)
pos = 0
for r in rows:
    m = r.get('message') or {}
    content = m.get('content') if isinstance(m, dict) else None
    if r.get('type') == 'assistant' and isinstance(m, dict) and m.get('usage'):
        pos += 1
    if not isinstance(content, list): continue
    for c in content:
        if not isinstance(c, dict): continue
        if c.get('type') == 'tool_use':
            tool_names[c.get('id')] = c.get('name', '?')
            # lo que escribe el asistente para llamar a la herramienta (salida)
            tool_cost[group_for(c.get('name', '?'))] += 5 * len(json.dumps(c.get('input', {}))) / 4
        elif c.get('type') == 'tool_result':
            name = tool_names.get(c.get('tool_use_id'), '?')
            tok = size(c.get('content')) / 4
            remaining = max(n - pos, 0)
            tool_cost[group_for(name)] += tok * 2 + tok * 0.1 * remaining

instructions = base_ctx * 0.1 * n + base_ctx * 2  # releída cada turno + una escritura inicial
attributed = instructions + sum(tool_cost.values())
other = max(main_total - attributed, 0)

# Subagentes
subs = []
for p in glob.glob(os.path.join(sub_dir, '**', '*.jsonl'), recursive=True):
    total, ids = 0, set()
    with open(p, encoding='utf-8') as f:
        for line in f:
            try: r = json.loads(line)
            except Exception: continue
            m = r.get('message') or {}
            if r.get('type') == 'assistant' and isinstance(m, dict) and m.get('usage'):
                if m.get('id') in ids: continue
                ids.add(m.get('id')); total += eff(m['usage'])
    subs.append((os.path.basename(p), total))
sub_total = sum(t for _, t in subs)

groups = {'Instrucciones de Claude (se releen cada turno)': instructions, 'Conversación y razonamiento': other}
groups.update(tool_cost)
groups['Subagentes (%d)' % len(subs)] = sub_total
scale = (main_total) / max(attributed + other, 1)
grand = main_total + sub_total
print(json.dumps({
    'turnos_principales': n, 'contexto_inicial_tokens': base_ctx,
    'total_efectivo': round(grand), 'principal': round(main_total), 'subagentes': round(sub_total),
    'grupos': {k: round(v) for k, v in sorted(groups.items(), key=lambda x: -x[1]) if v > grand * 0.005},
    'subagentes_detalle': sorted([(a, round(b)) for a, b in subs], key=lambda x: -x[1]),
}, ensure_ascii=False, indent=1))
