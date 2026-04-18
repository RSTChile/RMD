#!/bin/bash

NOMBRE=$1

if [ -z "$NOMBRE" ]; then
  echo "Uso: ./generar_resumen.sh NOMBRE_DEL_CASO"
  exit 1
fi

ARCHIVO="09_RESUMEN_EJECUTIVO/${NOMBRE}.md"

cat << 'DOC' > "$ARCHIVO"
# RESUMEN EJECUTIVO — RMD 2.0

---

## 1. Contexto y objetivo

(Qué se analiza, por qué, tipo de sistema/sujeto)

---

## 2. Base factual (MiE + ANA)

- Hechos verificados:
- Vacíos de información:
- Línea temporal:
- Eventos críticos:

⚠️ Sin interpretación

---

## 3. Estructura del sistema / sujeto

- Identidad operativa (autopoiesis)
- Rasgos estructurales
- Perfil cognitivo (si aplica)
- Afectividad estructural (AFE)

---

## 4. Cosmovisión

- Interpretación de la realidad
- Telos (qué busca)
- Nivel de cierre doctrinal

---

## 5. Escalamiento (MAPAR-S)

- Nodo:
- Justificación:
- Diferenciar discurso / intención / acción

---

## 6. Capacidad operacional

- Recursos
- Red
- Alcance

⚠️ Capacidad ≠ intención

---

## 7. Riesgo de sorpresa (Shibumi)

- NIP:
- ROP:
- SLD:

Interpretación:

---

## 8. Cosmosemiótica

- ICR:
- IRDE:
- Bext-Cos:
- CEE-Cos:
- IPEM-Cos:

Interpretación obligatoria (no números sueltos)

---

## 9. Post-VDA

- Escenario 1:
- Escenario 2:
- Qué podría invalidar el análisis:

---

## 10. Conclusiones

- Qué está pasando realmente
- Nivel de riesgo
- Tipo de dinámica

---

## 11. Recomendaciones

- Qué hacer
- Qué no hacer
- Qué monitorear

---

## NOTA FINAL

No usar índices como conclusión.
No inferir sin evidencia.
Explicar todo concepto técnico.

DOC

echo "Informe creado en: $ARCHIVO"
