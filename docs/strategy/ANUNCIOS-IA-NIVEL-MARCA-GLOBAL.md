# Anuncios con IA a nivel de marca global: casos, pipeline, QA, stack y brecha de Altiora

Fecha: 2026-11-11 · Autor: `claude/creative-ads-director` (investigación; sin producción) · Estado: **DISEÑADO** (borrador para revisión).
Ubicación: `docs/strategy/ANUNCIOS-IA-NIVEL-MARCA-GLOBAL.md` (rama `claude/anuncios-ia-nivel-global`, aprobada por el usuario el 2026-11-11).
Leyenda: **VERIFICADO** = con fuente enlazada o comando ejecutado · **OPINIÓN** = criterio de dirección · **SUPUESTO** = cifra o dato sin comprobar en esta sesión · **NO SÉ** = no encontrado.

> **¿Aporta valor o entorpece?** Aporta valor **solo si** se convierte en una pieza piloto para un cliente real (El Tilichero o La Central del Queso) que sirva de venta y portafolio. Entorpece si se traduce en suscripciones, hardware o más infraestructura antes de tener un cliente que pague: Altiora tiene 0 clientes de pago (`docs/altiora-business/FINANZAS.md`).

---

## 0. Resumen ejecutivo (5 líneas)

1. Las marcas grandes **no** hacen «un prompt y listo»: Coca-Cola necesitó estudios especializados, 5 especialistas y unos **70.000 clips** para un spot, y aun así recibió críticas por inconsistencias (camiones que cambian de forma). VERIFICADO (§1).
2. El nivel «marca global» no depende del modelo de video, sino de **dirección + selección + postproducción + QA**. Un spot de Kalshi costó unos **US$2.000** con Veo 3, con una tasa de aprovechamiento de 15 clips útiles de 300–400 generaciones (≈4–5 %). VERIFICADO.
3. La PC actual de Altiora (AMD 3020e, 2 núcleos, Radeon Vega 3 integrada, 13,9 GB) **no** cumple el mínimo de DaVinci Resolve (GPU dedicada de 4 GB, 16 GB de RAM). Generación en la nube y montaje ligero, sí; color y VFX pesados en local, no. VERIFICADO (comando, §4).
4. Altiora ya tiene la parte que más escasea: roles, skills, SOP de postproducción, Blender comprobado y una dirección de pieza diseñada (`projects/tilicheros/ads/vfx-captacion`). Le faltan **cuentas de generación con licencia comercial, un editor/colorista utilizable, una biblioteca de consistencia (personajes/producto/LUT) y un caso producido y medido**.
5. Recomendación (OPINIÓN): producir **una** pieza piloto de 15 s, la ruta «Adentro de la caja» de El Tilichero, en nivel Mínimo viable (unos US$60–150 en créditos, SUPUESTO), y medirla por consultas de WhatsApp con código, no por vistas.

---

## 1. Casos reales

### 1.1 Coca-Cola — «Holidays Are Coming» con IA (2024 y 2025)

| Aspecto | 2024 | 2025 |
|---|---|---|
| Estudios | Secret Level, Silverside AI y Wild Card; cada uno hizo su versión. VERIFICADO ([PetaPixel](https://petapixel.com/2024/11/18/coca-cola-uses-ai-video-to-reimagine-its-classic-christmas-ad), [Marketing Brew](https://www.marketingbrew.com/stories/2024/11/21/inside-the-making-of-one-of-coca-cola-s-controversial-holiday-commercials)) | Silverside y Secret Level. VERIFICADO ([Tom's Guide](https://tomsguide.com/ai/ai-image-video/coca-cola-turns-to-ai-for-its-christmas-ad-in-2025-sparking-mixed-reactions)) |
| Herramientas | Leonardo (imagen) → Luma y Runway (animación); Kling se sumó a mitad de la producción y Secret Level lo usó para personas. Sora y MiniMax citados por algunas fuentes (incierto). VERIFICADO parcial ([Marketing Brew](https://www.marketingbrew.com/stories/2024/11/21/inside-the-making-of-one-of-coca-cola-s-controversial-holiday-commercials)) | Sora, Veo 3 y Luma según el *making of* de la marca; otra fuente cita Runway, Kling y Luma. VERIFICADO con discrepancia ([eWeek](https://www.eweek.com/news/coca-cola-ai-ads/), [Dataconomy](https://dataconomy.com/2025/11/04/coca-colas-new-ai-generated-christmas-ad-shows-why-generative-video-still-struggles-with-realism)) |
| Escala | — | 5 especialistas y unos 70.000 clips; plazo de 30 días según la marca y 2 meses según Silverside (frente a ~1 año en CGI tradicional). VERIFICADO con discrepancia |
| Qué funcionó | Velocidad, volumen de versiones y alcance global; la marca lo considera un éxito; System1 reportó una respuesta positiva del público general. VERIFICADO según fuentes secundarias ([Marketing-Interactive](https://www.marketing-interactive.com/coca-cola-s-2025-ai-driven-holiday-ad-draws-mixed-reactions)) | Idem; animales en lugar de personas para esquivar el «valle inquietante» de 2024. VERIFICADO ([Implicator](https://www.implicator.ai/coca-cola-debuts-ai-holiday-ads-animals-replace-actors-after-2024-backlash/)) |
| Críticas | Personas poco creíbles y una sensación de «falta de alma». VERIFICADO ([The Decoder](https://the-decoder.com/ai-generated-holidays-are-coming-coca-cola-ad-looks-festive-but-feels-artificial-critics-say/)) | Camiones que cambian de forma y número de ruedas, animales que se mueven como recortes, mezcla de estilos realista y caricaturesco, y comentarios negativos (CARMA: 32 % negativo frente a 10,2 % positivo). VERIFICADO ([Tom's Guide](https://tomsguide.com/ai/ai-image-video/coca-cola-turns-to-ai-for-its-christmas-ad-in-2025-sparking-mixed-reactions), [ContentGrip](https://www.contentgrip.com/coca-cola-ai-holiday-ad-backlash/)) |

**Lección para Altiora (OPINIÓN):** el fallo visible de Coca-Cola fue de **continuidad del objeto de marca** (el camión), justo lo que un cliente pequeño menos perdona en su producto. Regla derivada: el producto real **nunca** se genera; se fotografía, se filma o se modela en 3D desde referencias reales (coincide con `DIRECCION_CREATIVA.md` de El Tilichero).

### 1.2 Puma

- **Imagen de catálogo con Google Cloud:** Puma usa Imagen en Vertex AI para generar imágenes de producto personalizadas por mercado. VERIFICADO ([PR Newswire / Google Cloud](https://www.prnewswire.com/news-releases/puma-transforms-product-campaign-development-with-google-clouds-generative-ai-302256616.html)). Es IA aplicada a fondos y contexto, no a reinventar el producto.
- **Spot «sin intervención humana»:** una fuente lo atribuye a Monks + NVIDIA + agentes de Meta (Llama como orquestador, NVIDIA Cosmos para metraje y Runway + Flux para fijas), hecho en 5 semanas. VERIFICADO solo por fuentes secundarias de calidad desigual ([SmashingApps](https://www.smashingapps.com/puma-and-ai-agent-ad-generative-ai/), [Mercado Negro](https://mercadonegro.pe/medios/digital/creatividad-o-automatizacion-el-anuncio-de-puma-generado-por-ia-desata-polemica)). La fecha y la autoría exacta están en conflicto: **NO SÉ** cuál es la versión oficial.
- **Críticas:** debate entre «creatividad o automatización». VERIFICADO (Mercado Negro).

### 1.3 Adidas

- **«Floral by adidas»** es un **spec ad** independiente (no un encargo oficial) de Blair Vermette (RabbitHole), hecho con Runway, Midjourney, Adobe y Topaz para el escalado. Recepción dividida. VERIFICADO ([Marketing-Interactive](https://www.marketing-interactive.com/why-creatives-are-rooting-for-this-adidas-floral-spec-ad-crafted-entirely-by-ai), [Brandsynario](https://www.brandsynario.com/technology/adidas-drops-its-first-ever-100-ai-made-campaign/)).
- **Uso oficial:** creatividad automatizada para rendimiento (Ad-Lib.io, +12 % de conversiones según el proveedor; no verificado de forma independiente) ([caso](https://www.casestudies.com/company/ad-libio/case-study/adidas-achieved12-uplift-in-conversionswith-ad-libios-automated-creative-tools)) y VFX generativo para rejuvenecer jugadores en «Backyard Legends» (2026) ([Pulse](https://www.pulse.bot/digital-marketing/news/adidas-backyard-legends-a-true-40-yard-screamer-51c2f29b-960c-4521-b032-9190e39fa2a8/)).
- **NO SÉ:** no encontré qué agencia ni qué herramientas usa Adidas internamente para un spot 100 % IA oficial.

**Lección (OPINIÓN):** muchos de los «anuncios IA de Adidas/Nike» que circulan son **spec ads**. Son el camino legítimo para que Altiora construya portafolio, pero **nunca** se presentan como trabajo para esa marca ni se usa su logo en material comercial de Altiora.

### 1.4 Kalshi — el caso más útil para Altiora

Spot emitido en la final de la NBA 2025: PJ Accetturo, Veo 3, unos **US$2.000 y 2 días**. Flujo: guion con Gemini/ChatGPT → lista de planos y prompts con Gemini (5 a la vez) → **300–400 generaciones para 15 clips útiles** → montaje en CapCut. VERIFICADO ([NPR](https://www.npr.org/2025/06/23/nx-s1-5432712/ai-video-ad-kalshi-advertising-nba-finals)).
**Lección (OPINIÓN):** el rendimiento real ronda el **4–5 %** y es la base de cualquier presupuesto de créditos. Funcionó porque el **concepto** (humor absurdo y caótico) convierte los artefactos de la IA en parte del estilo.

### 1.5 Patrón común (OPINIÓN, derivada de 1.1–1.4)

| Funciona | Falla |
|---|---|
| Conceptos donde la estética IA es parte de la idea (surreal, miniatura, animales, absurdo) | Rostros humanos realistas en primer plano y diálogo con sincronía labial |
| Planos cortos (2–5 s) y mucho montaje | Objetos de marca que deben mantener la forma exacta entre planos (camión, logo, empaque) |
| Producto real compuesto sobre el mundo generado | Producto generado por IA |
| Diseño sonoro y música hechos por personas | Sustituir la idea por espectáculo («sin alma») |

---

## 2. Pipeline de la preproducción al máster

Encaja con lo existente: `creative-ads-os/WORK_ROUTER.md` → `creative-ads-director` + `visual-producer` + `motion-designer` + `qa-reviewer`; skills `advertising-concept`, `storyboarding`, `cinematic-direction`, `ai-video-direction` (+ `references/postproduction-playbook.md`), `audio-production`, `creative-quality-assurance`. **No hace falta crear agentes nuevos.** Lo que sigue amplía el playbook con la capa generativa.

| Fase | Qué se hace | Herramientas (nube/local) | Entregable y gate |
|---|---|---|---|
| **P0 Brief** | Objetivo comercial, métrica (consultas con código), claims permitidos, presupuesto de créditos | Repo (`advertising-concept`) | Brief aprobado por una persona. **Gate:** ¿la idea necesita IA o se filma más barato con celular? |
| **P1 Guion y storyboard** | 3 rutas (humor, emoción, demostración), guion por segundos, beats de 2–5 s | LLM + `storyboarding`; boceto con imagen IA (Midjourney/Nano Banana/Flux) o a mano | Animatic de fijas con tiempos (puede hacerse en DaVinci/CapCut con imágenes) |
| **P2 Biblia visual** | Paleta, lentes, luz, estilo, **hoja de personaje** (frente/perfil/¾) y **hoja de producto** (fotos reales en 6 ángulos) | Imagen IA + fotos reales; Higgsfield Soul ID o referencias de personaje de Runway/Kling para consistencia | `style-bible.md` + carpeta de referencias con licencia |
| **P3 Layout y previz en Blender** | Set de baja poligonización, cámara con lente real (mm), recorrido de cámara, luz clave; render de **fotogramas clave** (primer y último cuadro de cada plano) | Blender 5.2.2 (VERIFICADO local en CPU, lento); EEVEE para previz | Fotogramas clave 1080×1920 por plano. **Gate:** composición y continuidad aprobadas *antes* de gastar créditos de video |
| **P4 Generación de video** | Imagen→video con primer/último cuadro; control de cámara; 1 plano = 1 acción; lotes de 4–8 variantes; registrar prompt, semilla, modelo y coste | Veo 3.1 (calidad y audio), Kling 3.0 (relación calidad/precio y personas), Runway Gen-4.5 (control y edición de video), Higgsfield (presets de cámara y Soul ID, agregador de modelos), Seedance (barato). Sora 2: **descontinuado** según fuentes secundarias ([Shattered](https://shattered.io/best-ai-video-generators-kling-4-veo-3-1-sora-shutdown-2026/)) | `generation-log.csv`; selects con criterio QA (§3) |
| **P5 Producto real** | Producto filmado/fotografiado con luz que imite la del plano IA; o modelo 3D de Blender hecho con fotos reales (fidelidad comprobada) | Celular + luz continua barata; Blender | Placas del producto con fondo limpio para componer |
| **P6 Composición y VFX** | Integrar producto real y logo vectorial (nunca el logo generado), limpiar artefactos, rotoscopia, *paint-out* | After Effects / DaVinci Fusion (no viable con la PC actual) / Photoshop para fotogramas | Planos «limpios» con logo y producto exactos |
| **P7 Montaje** | Ritmo, *whip* y cortes ocultos, subtítulos | DaVinci Resolve / Premiere / CapCut; FFmpeg + Remotion (ya en el SOP del repo) | Timeline + EDL |
| **P8 Upscaling y limpieza** | Escalar a 1080×1920 o 4K **solo al final** y sobre selects; reducir parpadeo | Topaz Video, escalado de Runway/Higgsfield, Resolve Super Scale (Studio) | Comparación A/B antes y después del escalado |
| **P9 Color** | Igualar planos de modelos distintos (gran fuente de incoherencia), LUT de marca, protección de tonos de piel y del color de marca | DaVinci Resolve (estándar de la industria) | LUT de marca + *stills* de referencia |
| **P10 Sonido y voz** | Diseño sonoro propio (foley real), música con licencia, voz humana o sintética **con consentimiento**; mezcla a −14 LUFS para redes (orientativo) | `audio-production` + `audio-specialist`; ElevenLabs u otra (SUPUESTO: precios por verificar); Fairlight en Resolve | Mezcla estéreo + stems |
| **P11 Máster y versiones** | H.264/AAC, yuv420p, 9:16 / 4:5 / 16:9, versión sin texto, subtítulos .srt | FFmpeg (SOP del repo) | Másteres + manifiesto de derechos + reporte QA |

**Regla de presupuesto de créditos (OPINIÓN basada en Kalshi):** planos útiles × 20–25 generaciones × duración × precio por segundo, más un 30 % de margen.

---

## 3. Control de calidad

### 3.1 Checklist técnico (bloquea `SUCCESS` si falla un ítem marcado ★)

- ★ **Resolución y formato:** 1080×1920 como mínimo, fps constante, H.264/AAC, sin bandas negras accidentales (`ffprobe` + visionado).
- ★ **Producto y logo:** forma, color, texto y proporciones idénticos a la referencia real en **todos** los planos (comparación cuadro a cuadro con la hoja de producto).
- ★ **Manos y anatomía:** recuento de dedos y articulaciones; nada de dedos que se funden con objetos.
- ★ **Texto en pantalla:** todo texto legible se añade en postproducción; ningún texto generado (salen letras falsas).
- ★ **Coherencia entre planos:** vestuario, peinado, luz y dirección de la mirada; regla de los 180°; objeto de marca estable (lección Coca-Cola).
- **Física y cámara:** sin *morphing*, sin pies que patinan, sin parpadeo de texturas; movimiento de cámara motivado y no aleatorio.
- **Color:** planos igualados en blancos, contraste y saturación; color de marca medido (p. ej., `#c4161c` de El Tilichero, dato de `vfx-captacion/CONCEPTO.md`).
- **Audio:** sin clipping, voz inteligible, sincronía, sonoridad final adecuada al canal, sin música sin licencia.
- **Zonas seguras** de Reels/TikTok: CTA y texto fuera de la interfaz de la app.
- ★ **Visionado humano completo** en un móvil real. Sin esto, QA visual = `NOT_RUN` (regla ya vigente en el playbook).

### 3.2 Checklist legal y de licencias

| Riesgo | Regla | Estado de la evidencia |
|---|---|---|
| **Uso comercial por herramienta** | Solo planes de pago. Los planes gratuitos de Higgsfield y Kling **excluyen** uso comercial | VERIFICADO según fuentes secundarias ([Higgsfield, blog oficial](https://higgsfield.ai/blog/higgsfield-pricing-explained); [teamday](https://www.teamday.ai/blog/best-ai-video-models-2026)). Leer los TOS vigentes antes de cada contratación: **pendiente de revisión cruzada** |
| **Indemnización** | Adobe Firefly ofrece indemnización de PI en planes de pago, pero **no** cubre modelos de socios dentro de Firefly | VERIFICADO según fuentes secundarias ([Adobe News](https://news.adobe.com/news/2025/02/firefly-web-app-commercially-safe), [Fluxnote](https://fluxnote.io/guides/adobe-firefly-ai-video-generator-review)). NO SÉ si Veo, Kling o Higgsfield indemnizan a clientes pequeños |
| **Derechos de autor del resultado** | En EE. UU., un prompt por sí solo no da autoría; sí se protegen la selección, el arreglo y el material humano integrado | VERIFICADO ([Copyright Alliance — informe USCO parte 2](https://copyrightalliance.org/ai-report-part-2-copyrightability/)). Costa Rica: NO SÉ; consultar abogado. Consecuencia contractual: no prometer al cliente «exclusividad» del material generado; ceder lo que sí es de Altiora (guion, montaje, composición) |
| **Derecho de imagen** | Consentimiento escrito para rostro **y voz** de cualquier persona real, incluido su uso para entrenar o clonar | Art. 47 del Código Civil de Costa Rica exige consentimiento para publicar o vender la imagen, con excepciones. VERIFICADO según fuentes secundarias ([CIJUL-UCR](https://cijulenlinea.ucr.ac.cr/blog/category/derecho-a-la-imagen/)). Texto literal y jurisprudencia: **pendiente de abogado** |
| **Parecidos y marcas ajenas** | No generar celebridades, personajes, logos ni diseños de producto de terceros; revisar cada plano por marcas «coladas» | OPINIÓN, coherente con `WORK_ROUTER.md` §Checkpoint |
| **Divulgación de IA** | Meta aplica la etiqueta «AI info» con sus herramientas o al detectar metadatos C2PA; TikTok exige divulgación del contenido AIGC en anuncios | VERIFICADO solo con blogs ([ContentGrip](https://www.contentgrip.com/meta-ai-ad-labels/), [Billo](https://billo.app/blog/ai-labeling/)); leer las políticas oficiales antes de pautar. **No borrar metadatos C2PA** |
| **UE (si un cliente pauta allí)** | AI Act art. 50: obligación de divulgar *deepfakes* desde el 2-ago-2026, más ligera en obras evidentemente creativas | VERIFICADO según fuentes secundarias ([artificialintelligenceact.eu](https://artificialintelligenceact.eu/?p=6131)). Hoy no aplica a clientes de Costa Rica (OPINIÓN) |
| **Claims** | Nada de prestaciones, precios ni «original» sin ficha vigente (regla de El Tilichero) | Vigente en el repo |

Plantilla mínima por pieza: `rights-manifest.json` con herramienta, plan, fecha, TOS consultado, prompt/semilla, consentimientos, música/licencia y etiqueta de IA aplicada.

---

## 4. Stack recomendado por niveles

### 4.1 Hardware local — VERIFICADO (PowerShell, 2026-11-11)

`AMD 3020e` (2 núcleos) · `Radeon Vega 3` integrada (2 GB compartidos) · `13,9 GB` de RAM · `Resolve.exe` **no encontrado** en la ruta estándar · en `C:\Program Files\Adobe` solo aparece `Acrobat DC` (no se buscó en otras rutas). Blender 5.2.2 sí está (doc `BLENDER-LOCAL.md`, prueba del 2026-10-31).
Requisito mínimo de Resolve: GPU dedicada de 4 GB y 16 GB de RAM (32 GB con Fusion). VERIFICADO ([Blackmagic readme](https://www.blackmagicdesign.com/support/content/readme/d8c4a8297ebb4d94b14a045ba7eda2eb), [VRLA Tech](https://vrlatech.com/davinci-resolve-gpu-buyers-guide-for-2026-which-card-is-actually-right-for-you/)).
**Conclusión:** la generación es 100 % en la nube (no depende del PC). Montaje ligero, sí (CapCut/FFmpeg/Remotion). Color serio en Resolve, After Effects, Topaz y render de Blender en Cycles: **no viables** o muy lentos en esta máquina.

### 4.2 Niveles (precios en US$ aproximados; **verificar en la página oficial antes de pagar**)

| Nivel | Generación | 3D / previz | Post | Audio | Coste mensual aprox. | Curva | Hardware |
|---|---|---|---|---|---|---|---|
| **Mínimo viable** (piloto) | **Un solo** proveedor: Higgsfield Starter/Plus (US$15–49, [blog oficial](https://higgsfield.ai/blog/higgsfield-pricing-explained)) *o* Kling por créditos (~US$0,10/s) *o* Google AI Pro (US$19,99, [teamday](https://www.teamday.ai/blog/best-ai-video-models-2026)) | Blender en CPU solo para fijas de layout (ya comprobado) | CapCut + FFmpeg/Remotion (SOP existente) | Foley con celular + biblioteca con licencia; voz humana | **US$20–60** + créditos de la pieza | 2–3 semanas | PC actual suficiente |
| **Profesional** | Higgsfield Plus/Ultra (US$49–129) **+** Veo 3.1 por API (US$0,10–0,40/s) para planos estrella; Midjourney (SUPUESTO ~US$30/mes) | Blender con GPU (render de producto y cámara) | DaVinci Resolve gratuito → Studio (SUPUESTO ~US$295 pago único); Photoshop | ElevenLabs u otra con licencia comercial (SUPUESTO ~US$22/mes); música de stock | **US$150–350** | 2–3 meses | **Requiere PC nueva**: GPU NVIDIA de ≥8–12 GB, 32 GB RAM (SUPUESTO: US$1.200–1.800) o estación en la nube por horas |
| **Top** | Varios modelos por plano (Veo, Kling, Runway Gen-4.5 con edición de video), Adobe Firefly para lo «comercialmente seguro» con indemnización | Blender + escaneo o fotogrametría del producto | Resolve Studio + After Effects/Premiere (SUPUESTO ~US$70/mes Creative Cloud Pro) + Topaz | Diseñador de sonido humano + música original | **US$400–1.000+** y talento externo por proyecto | 6–12 meses | Estación de trabajo + almacenamiento NAS |

**OPINIÓN:** para el modelo de Altiora (proyecto de US$10.000 con E/P ≥ 25 %, `FINANZAS.md`), el nivel Profesional se justifica **después** del primer cliente que pague, como coste del proyecto y no como estructura fija. Antes, Mínimo viable.

---

## 5. Brecha y plan

### 5.1 Qué hay hoy (VERIFICADO en el repo canónico)

- Router y roles de anuncios (`creative-ads-os/WORK_ROUTER.md`, `.claude/agents/creative-ads-director.md`, `audiovisual-experience-director.md`, `audio-specialist.md`, `visual-producer.md`).
- Skills: `ai-video-direction` con playbook de postproducción FFmpeg/Remotion, `storyboarding`, `cinematic-direction`, `creative-quality-assurance` y `audio-production`.
- Workflow multi-IA (`docs/workflows/visual-production-multi-ai.md`) y repos de video seleccionados (`docs/research/video-production-repositories-2026-10-30.md`: Remotion, Whisper, auto-editor; **documentados, no instalados**).
- Blender 5.2.2 comprobado en CPU (`docs/operations/BLENDER-LOCAL.md`) y script `projects/tilicheros/ads/vfx-captacion/produccion/blender/caja_tilichero.py` con fotograma `kf_B6`.
- Pieza diseñada: `vfx-captacion/CONCEPTO.md` «Adentro de la caja», 24 s/15 s, estado DESIGNED, con medición por código «CAJA».

### 5.2 Qué falta

| # | Brecha | Impacto | Cierre más corto |
|---|---|---|---|
| B1 | Ninguna cuenta de generación de video con licencia comercial comprobada (no encontrada en `REGISTRO-HERRAMIENTAS.md` ni en `ALTIORA-REAL-INTEGRATION-STATUS.md`) | Bloquea producir | 1 suscripción mensual cancelable, aprobada por el usuario |
| B2 | Hardware no apto para color, VFX ni render GPU | Limita el nivel Profesional | Montaje ligero local; color básico en CapCut; aplazar la compra hasta tener cliente |
| B3 | Sin «biblia» de consistencia (personaje, producto, LUT) ni plantilla `rights-manifest` / `generation-log` | Incoherencia entre planos (error Coca-Cola) | Añadir 2 plantillas al playbook (sin agentes nuevos) |
| B4 | Sin caso producido y medido | No hay prueba de venta para Altiora | Pieza piloto (§5.3) |
| B5 | Datos del negocio de El Tilichero pendientes (SKU, fichas) | Bloquea piezas de producto, **no** la ruta «Adentro de la caja» (usa objetos genéricos) | Producir primero la ruta genérica |
| B6 | Contrato de cliente sin cláusulas de IA (autoría, divulgación, consentimientos) | Riesgo legal | Revisión de abogado antes del primer cobro |

### 5.3 Plan por pasos con pieza piloto medible

**Pieza:** `ALT-VIS-TIL-VFX-01`, corte de 15 s «Adentro de la caja» (beats B1, B2, B3, B5, B6 y B7 de `CONCEPTO.md`).

1. **Aprobación (usuario):** concepto, presupuesto máximo de créditos (propuesta: US$100, tope US$150) y un único proveedor. *Nada se gasta sin este sí.*
2. **Biblia y fotogramas clave (0 US$):** completar los 6 fotogramas de inicio y fin en Blender (CPU, 1080×1920, EEVEE para pruebas) y la paleta. Gate de composición.
3. **Generación (créditos):** 6 planos × ~20 generaciones × 3–5 s. Registrar cada intento en `generation-log.csv`.
4. **Post:** montaje con FFmpeg/Remotion o CapCut según el SOP; logo y CTA vectoriales; foley propio; igualación de color.
5. **QA independiente:** checklist §3 por `qa-reviewer` (otra IA o secuencial declarado) + visionado en móvil.
6. **Publicación (usuario y cliente):** solo con aprobación del dueño de El Tilichero, con la etiqueta de IA aplicada.
7. **Medición (14 días):** comparar con el Reel tipográfico anterior.

**Métricas de aceptación (propuestas):**

| Métrica | Objetivo del piloto | Tipo |
|---|---|---|
| Checklist técnico ★ | 100 % aprobado | Calidad |
| Coste por segundo útil | ≤ US$10/s final (SUPUESTO de partida; se ajusta con el log) | Eficiencia |
| Rendimiento de generación | ≥ 5 % (referencia Kalshi ≈ 4–5 %) | Eficiencia |
| Horas totales | ≤ 20 h | Margen |
| Consultas de WhatsApp con código «CAJA» | Superar la línea base del Reel anterior en la misma ventana | Negocio (principal) |
| Vistas | Solo informativo; **no** es criterio de éxito | — |

**Siguiente paso concreto:** que el usuario apruebe (o rechace) el presupuesto de créditos y el proveedor del paso 1.

---

## 6. Formato de entrega (ROUTING §5)

1. **Resultado:** investigación de casos, pipeline, QA, stack por niveles y plan piloto, conectada con los roles, skills y piezas que ya existen en Altiora.
2. **Evidencia:** lectura de `team/ROUTING.md`, `creative-ads-os/WORK_ROUTER.md`, los agentes `creative-ads-director` y `audiovisual-experience-director`, `skills/ai-video-direction` (+ playbook), `INDEX.md`, `docs/operations/REGISTRO-HERRAMIENTAS.md`, `BLENDER-LOCAL.md`, `docs/research/video-production-repositories-2026-10-30.md`, `docs/workflows/visual-production-multi-ai.md`, `projects/tilicheros/DIRECCION_CREATIVA.md`, `vfx-captacion/CONCEPTO.md` y `FINANZAS.md`; 15 búsquedas web (fuentes enlazadas arriba); un comando PowerShell de hardware (`Win32_VideoController`, `Win32_Processor`, RAM, rutas de Resolve y Adobe).
3. **Verificado / supuesto:** marcado en cada fila. Precios de Midjourney, Resolve Studio, Adobe CC, ElevenLabs, Topaz y hardware = SUPUESTO. Términos de licencia leídos en fuentes secundarias, no en los TOS oficiales. `npm run check`: ver PR. Revisión de `qa-reviewer` = `NOT_RUN`.
4. **Pendiente y bloqueos:** aprobación de gasto (paso 1); lectura de los TOS oficiales del proveedor elegido (**pendiente de revisión cruzada**); abogado para el art. 47 y las cláusulas de IA; datos del negocio de El Tilichero (no bloquean el piloto genérico).
5. **Siguiente paso:** el usuario decide proveedor y tope de créditos del piloto.
