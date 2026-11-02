# Informe de calidad de skills

Generado el 2026-11-02 con `npm run skills:baseline`. 355 skills; media **98.3/100**.
Por origen: propias 259: media 100 (259 en 100); origen externo 96: media 93.9. Las de origen externo (terceros y copias de skills personales) no se reescriben a mano; mejoran con casos de evaluación propios o actualizando desde su origen.
Mide estructura y verificabilidad; no sustituye ejecutar los casos de evaluación. Proceso: [mejora continua de skills](../docs/workflows/skill-improvement.md).

## Reglas incumplidas

| Regla | Puntos | Skills que fallan |
|---|---:|---:|
| Frontmatter YAML presente (`frontmatter`) | 5 | 0 |
| name coincide con la carpeta (`name-match`) | 5 | 0 |
| description entre 60 y 1024 caracteres (`description-length`) | 5 | 0 |
| description indica cuándo usarla (`description-trigger`) | 5 | 10 |
| Un único título H1 (`single-h1`) | 5 | 21 |
| Sin secciones H2 duplicadas (`no-duplicate-sections`) | 10 | 1 |
| Sin encabezados vacíos (`no-empty-sections`) | 5 | 4 |
| Sin párrafos repetidos (`no-duplicate-paragraphs`) | 10 | 8 |
| Sin bloque SOP genérico que contradiga el contrato (`no-legacy-conflict`) | 10 | 0 |
| SKILL.md de 500 líneas o menos (`length`) | 5 | 3 |
| Al menos 3 casos de evaluación (`eval-cases`) | 15 | 2 |
| Define el entregable (`output-defined`) | 5 | 38 |
| Enlaces locales válidos (`local-links`) | 10 | 0 |
| Versión declarada (`versioned`) | 5 | 18 |

## Distribución

| Rango | Skills |
|---|---:|
| 90–100 | 344 |
| 75–89 | 10 |
| 60–74 | 1 |
| 0–59 | 0 |

## 25 skills con menor puntuación (backlog del próximo ciclo)

| Skill | Puntos | Reglas incumplidas |
|---|---:|---|
| gcp-pipeline-orchestration | 70 | description-trigger, single-h1, no-duplicate-sections, no-empty-sections, length |
| finishing-a-development-branch | 80 | single-h1, no-empty-sections, output-defined, versioned |
| n8n-error-handling-official | 80 | eval-cases, versioned |
| n8n-expressions-official | 80 | eval-cases, versioned |
| ai-seo | 85 | single-h1, length, output-defined |
| building-data-apps | 85 | no-duplicate-paragraphs, output-defined |
| cloud-databases-onboarding | 85 | no-duplicate-paragraphs, output-defined |
| gcp-managed-airflow-migrations | 85 | description-trigger, no-duplicate-paragraphs |
| orca-orchestration | 85 | description-trigger, single-h1, length |
| schema-mapping | 85 | single-h1, no-duplicate-paragraphs |
| webapp-testing | 85 | description-trigger, output-defined, versioned |
| ad-creative | 90 | single-h1, no-empty-sections |
| bigquery-graph-query | 90 | no-duplicate-paragraphs |
| brainstorming | 90 | output-defined, versioned |
| dispatching-parallel-agents | 90 | single-h1, versioned |
| frontend-design | 90 | output-defined, versioned |
| gcp-data-pipelines | 90 | description-trigger, output-defined |
| gcp-managed-airflow-dag-authoring | 90 | no-duplicate-paragraphs |
| gcp-pipeline-resource-provisioning | 90 | single-h1, output-defined |
| gcp-spark | 90 | no-duplicate-paragraphs |
| gcp-spark-troubleshooting | 90 | no-duplicate-paragraphs |
| immersive-interaction-lab | 90 | description-trigger, output-defined |
| managing-python-dependencies | 90 | single-h1, output-defined |
| requesting-code-review | 90 | output-defined, versioned |
| resolving-mcp-region-configs | 90 | description-trigger, output-defined |
