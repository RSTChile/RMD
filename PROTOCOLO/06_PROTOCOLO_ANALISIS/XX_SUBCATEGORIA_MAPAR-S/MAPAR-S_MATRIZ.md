# MAPAR-S — MATRIZ POR ETAPA

Matriz de selección de variables existentes + derivados internos.
Trazabilidad obligatoria.

---

## Principio rector

MAPAR-S no usa todas las variables al mismo tiempo.

Opera por etapas:

- cada etapa selecciona variables pertinentes
- cada selección debe ser trazable
- toda inferencia debe estar anclada en evidencia

---

## Estructura obligatoria

Cada etapa debe registrar:

- objetivo
- variables/métricas utilizadas
- datos requeridos
- fuentes
- método
- umbrales/triggers
- salida/acción
- notas

---

# 🔷 S0 — Fase 0: verificación estructural

## Objetivo
Validar integridad del sistema antes de cualquier análisis.

## Variables / métricas
- errores Excel
- #REF!
- #DIV0!
- IDs duplicados
- variables huérfanas

## Datos requeridos
- workbook completo

## Fuentes
- revisión interna

## Método
- checklist de integridad estructural

## Umbrales / triggers
- cualquier error estructural

## Salida / acción
- bloquear análisis y corregir

## Notas
- si S0 falla, todo el análisis queda inválido

---

# 🔷 S1 — MiE F1–F10

## Objetivo
Construir base factual sin juicios.

## Variables / métricas
- MiE completo

## Datos requeridos
- corpus factual
- eventos fechados

## Fuentes
- OSINT
- HUMINT
- documentos

## Método
- registrar hechos
- validar con usuario antes de conceptualizar

## Umbrales / triggers
- vacíos críticos

## Salida / acción
- mapa factual validado

## Notas
- si faltan datos: usar "No sé" + dónde buscar
- anti-heurístico obligatorio

---

# 🔷 S2 — ANA (299)

## Objetivo
Construir base histórica y genealógica obligatoria.

## Variables / métricas
- ANA (299)
- HLC
- LIN
- CHE
- FHC

## Datos requeridos
- genealogía
- biografía
- hitos
- quiebres

## Fuentes
- documentos
- archivos
- cronologías

## Método
- triangulación
- aplicar FHC = 0.8–1.5

## Umbrales / triggers
- inconsistencias cronológicas

## Salida / acción
- línea de tiempo
- drivers históricos

## Notas
- no concluir todavía

---

# 🔷 S3 — Identidad / Autopoiesis

## Objetivo
Detectar perfil estable del sujeto.

## Variables / métricas
- IPS
- ICS
- IMR
- IDM
- IVT
- trazas cualitativas

## Datos requeridos
- rutinas
- ética
- valores
- contradicciones

## Fuentes
- entrevistas
- textos
- biografía

## Método
- extraer invariantes
- detectar autopoiesis intelectual / emocional si aplica

## Umbrales / triggers
- contradicciones fuertes

## Salida / acción
- perfil estable de identidad

## Notas
- distinguir contradicción táctica vs fractura estructural

---

# 🔷 S3a — Perfil cognitivo (circunstancial)

## Objetivo
Estimar arquitectura cognitiva sin diagnóstico clínico.

## Variables / métricas
- IExap (280)
- Mmeta (297)
- Ceff (295)
- η (296)
- Ls (298)
- IDCS (294)

## Datos requeridos
- producción sostenida
- decisiones
- transferencia de dominio

## Fuentes
- textos largos
- clases
- debates
- juegos

## Método
- reportar en intervalo
- registrar asimetrías:
  - estratégica
  - verbal
  - sistémica

## Umbrales / triggers
- IExap alto + Mmeta alto + IDCS fértil

## Salida / acción
- COG-MAPAR:
  - alto
  - medio
  - bajo
- nota de asimetrías

## Notas
- prohibido usar CI clínico

---

# 🔷 S3b — AFE / Afectividad estructural

## Objetivo
Mapear frenos y gatillos bajo estrés.

## Variables / métricas
- EMOESTRESS
- PS (289)
- CEE-Cos (286)
- IRDE (278)
- IPEM-Cos (287)
- Bext-Cos (285)

## Datos requeridos
- cárcel
- pérdidas
- quiebres
- reconocimiento
- eventos críticos fechados

## Fuentes
- documentos
- testimonios
- prensa
- biografía

## Método
- mapear frenos y gatillos
- distinguir dolor vs vector estructural

## Umbrales / triggers
- PS baja bajo estrés + CEE-Cos alta

## Salida / acción
- alerta de bifurcación
- guardrails

## Notas
- no es clínica
- es arquitectura de reacción

---

# 🔷 S4 — Cosmovisión + Conquista ideológica

## Objetivo
Clasificar doctrina, telos y estructura cosmovisional.

## Variables / métricas
- taxonomía RMD
- IRIde
- TDId
- TDI
- IGM1

## Datos requeridos
- textos doctrinales
- símbolos
- teleología

## Fuentes
- libros
- papers
- discursos

## Método
- clasificar cosmovisión sin moralizar
- identificar telos

## Umbrales / triggers
- nihilismo
- escatología crítica activa

## Salida / acción
- mapa cosmovisional
- telos

## Notas
- separar causa de medio

---

# 🔷 S5 — Escalamiento MAPAR-S

## Objetivo
Ubicar al sujeto en el árbol de escalamiento.

## Variables / métricas
- IRIde
- TRI
- TADI
- ITV
- IAAP_X
- ITP
- IRA
- IPS
- ICS

## Datos requeridos
- conductas
- decisiones
- amenazas
- precedentes

## Fuentes
- prensa
- judicial
- OSINT

## Método
- ubicar en árbol N0–N8
- distinguir discurso vs acción

## Umbrales / triggers
- Nodo ≥ N3
- IRDE > 0.30

## Salida / acción
- nivel MAPAR-S
- recomendación

## Notas
- Post-VDA obligatorio desde N3

---

# 🔷 S6 — Capacidad operacional y red

## Objetivo
Medir capacidad sin confundirla con intención.

## Variables / métricas
- TPM
- IIX
- TDM
- IMR
- Itur
- TPCO
- THI (si aplica)

## Datos requeridos
- recursos
- logística
- redes
- movilidad

## Fuentes
- OSINT
- finanzas
- medios

## Método
- separar capacidad de intención
- usar como multiplicador

## Umbrales / triggers
- capacidad alta + Nodo ≥ N3

## Salida / acción
- priorizar mitigación
- priorizar monitoreo

## Notas
- capacidad ≠ intención

---

# 🔷 S6b — Shibumi / artefactos estratégicos

## Objetivo
Detectar no linealidad, opacidad y sorpresa.

## Variables / métricas
- NIP
- SLD
- ROP
- Ls
- IDCS
- Mmeta
- IExap

## Datos requeridos
- partidas Go / ajedrez
- simulaciones
- patrones observables

## Fuentes
- SGF
- PGN
- observables conductuales

## Método

### NIP
avg(
  norm(IDCS),
  norm(Mmeta),
  norm(IExap)
)

### ROP
avg(
  norm(Ceff),
  norm(η),
  norm(Mmeta)
)

### SLD
estimado por latencia entre señales y detección

## Umbrales / triggers
- NIP > 0.70
- o ROP > 0.70 + SLD alto

## Salida / acción
- marcador de sorpresa
- elevar vigilancia analítica

## Notas
- uso defensivo
- no optimizar evasión

---

# 🔷 S7 — MACEC Sub1 / presencia mediática y digital

## Objetivo
Evaluar huella mediática y digital del sujeto.

## Variables / métricas
- ICOP
- ICM
- IIX
- TPM
- TDM
- TAS
- TDI
- TPInd

## Datos requeridos
- datos de medios y redes
- ventana 25 años si aplica

## Fuentes
- medios
- X
- YouTube
- hemeroteca

## Método
- normalizar por ventana
- separar volumen vs impacto

## Umbrales / triggers
- IIX alto + IRDE bajo

## Salida / acción
- perfil de presencia
- drivers de influencia

## Notas
- evitar sesgo por volumen

---

# 🔷 S8 — Post-VDA / red-team

## Objetivo
Romper consenso y probar escenarios alternativos.

## Variables / métricas
- VDA (103)
- VDA-Cos (288)
- IPEM-Cos
- Bext-Cos
- CEE-Cos

## Datos requeridos
- resultados previos
- supuestos

## Fuentes
- equipo mixto humano/IA

## Método
- generar 2–3 contrafactuales
- definir condiciones de disparo
- definir falsación
- definir límites éticos

## Umbrales / triggers
- IRDE > 0.30
- divergencia discurso-percepción
- Nodo ≥ N3

## Salida / acción
- escenarios alternativos
- acciones

## Notas
- obligatorio desde N3

---

# 🔷 S9 — Cosmosemiótica

## Objetivo
Cerrar la lectura semiótica del caso.

## Variables / métricas
- ICR (277)
- IRDE (278)
- IEOS (279)
- IGM-Cos (283)
- Bext-Cos (285)
- CEE-Cos (286)
- IPEM-Cos (287)

## Datos requeridos
- corpus de mensajes
- ruido contextual

## Fuentes
- transcripciones
- posts
- clips

## Método
- calcular / estimar RC e INR
- aplicar semáforos
- registrar sesgos

## Umbrales / triggers
- IRDE > 0.30
- Bext alto

## Salida / acción
- capa final de sentido, ética y riesgo

## Notas
- no inferir ICR directamente

---

# 🔷 S10 — Resumen Ejecutivo extendido

## Objetivo
Entregar salida final para humanos e IAs.

## Variables / métricas
- IGRMD (300)
- síntesis MAPAR-S

## Datos requeridos
- todo lo anterior

## Fuentes
- documento final

## Método
- explicar variables
- explicar resultados
- documentar supuestos
- documentar límites
- documentar trazabilidad

## Umbrales / triggers
- sin S0 / MiE válido = inválido

## Salida / acción
- resumen ejecutivo extendido

## Notas
- salida final integrada

---

# 🔴 REGLAS TRANSVERSALES

## 1. Trazabilidad obligatoria
Cada variable debe registrar:
- origen
- fecha
- tipo de evidencia
- modo:
  - dato
  - estimado
  - no calculado

## 2. Anti-heurístico
No saltar etapas.
No adelantar conclusiones.

## 3. No diagnóstico
MAPAR-S no diagnostica.
Describe patrones emergentes falsables.

## 4. Capacidad ≠ intención
Regla obligatoria en S5 y S6.

## 5. Post-VDA
No opcional desde N3.

---

# 🧠 PRINCIPIO CENTRAL

MAPAR-S no clasifica personas.

MAPAR-S clasifica:

patrones de riesgo, escalamiento y sorpresa.

