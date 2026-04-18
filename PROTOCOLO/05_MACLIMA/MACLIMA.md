# MACLIMA — MÓDULO DE ANÁLISIS CLIMÁTICO INTEGRADO

## Naturaleza

MACLIMA es un módulo transversal del RMD 2.0.

No constituye un tipo de conflicto.

No reemplaza variables del modelo.

Opera como forzante sistémico post-medición.

---

## Función

1. Medir el estado climático objetivo del territorio
2. Sintetizarlo en un índice climático compuesto
3. Ajustar variables RMD mediante coeficientes (MACC)

---

## Ubicación en el flujo

Se aplica:

DESPUÉS de:
- MiE completo
- Cálculo de variables base

ANTES de:
- Escenarios (VDA)
- Cosmosemiótica final

---

## Componentes

### Variables MACLIMA

- ZBG — Zona Biogeográfica
- EstCicMacClim — Estado macro-climático
- ANTermic — Anomalía térmica
- ANPrecip — Anomalía de precipitación
- EstHidric — Estrés hídrico
- InEvExtre — Eventos extremos
- RIncFor — Riesgo de incendio
- PrCost — Presión costera

---

### Índice compuesto

- InClimCo — Índice climático compuesto

---

### Ajuste

- MACC — Matriz de coeficientes climáticos

---

## Regla de aplicación

MACC:

- Ajusta variables existentes
- Nunca crea variables nuevas
- Nunca reemplaza variables base

---

## Lista blanca de variables ajustables

(Definida en Hoja MACLIMA)

Incluye:

- Bloque Social (ICS, IPS, IAH, TMS)
- Bloque Económico (IIEC, IPE, IVP, IDE)
- Bloque Territorial (MICR, IVT, IRT)
- Bloque Seguridad (IOC, IVD, IPT)
- Bloque METECO (con cautela)
- Bloque Cosmosemiótico (ICR, IRDE indirectamente)

---

## Exclusiones explícitas

No ajustar:

- ANA
- VDA
- IGRMD

---

## Condiciones de aplicación

Debe existir:

- Justificación explícita
- Variable MACLIMA activa
- Trazabilidad del ajuste

---

## Propósito

Calibrar:

- umbrales
- sensibilidades
- persistencias

según el entorno climático real.

---

## Restricciones

- No duplicar mediciones
- No generar doble conteo
- No interpretar el conflicto como climático

---

## Resultado

Variables RMD ajustadas por condición climática.

Base para escenarios.
