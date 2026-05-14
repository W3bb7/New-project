# Arquitectura escalable de Khaba Core

Khaba Core queda organizado como un sistema cognitivo jerarquico con contratos
explicitos entre capas. La regla central no cambia: el ego reacciona, el
subconsciente modula desde memoria y el maestro interior decide con autoridad final.

## Componentes

- `DecisionContext`: entrada canonica para todas las capas. Evita que cada modulo
  normalice texto o gestione metadata por su cuenta.
- `CognitiveProfile`: configuracion del sistema. Permite cambiar senales, patrones
  y umbrales sin tocar el orquestador.
- `Ego`: produce una recomendacion reactiva con urgencia, beneficio, riesgo e influencia.
- `Subconsciente`: compara la situacion con patrones aprendidos y devuelve sesgo,
  confianza, modulacion y razones.
- `ConflictDetector`: detecta tensiones entre capas antes de entregar la decision
  al maestro interior.
- `MaestroInterior`: evalua coherencia, verdad y direccion. Puede integrar senales
  del ego y del subconsciente, pero no queda subordinado a ellas.
- `TraceEvent`: bitacora auditable de cada paso del flujo.

## Flujo

```text
situation
  -> DecisionContext.from_situation()
  -> Ego.response(context)
  -> Subconsciente.evaluate(context, ego_output)
  -> ConflictDetector.detect(ego_output, subconscious_output)
  -> MaestroInterior.decide(context, ego_output, subconscious_output, conflicts)
  -> FinalDecision
```

## Puntos de extension

1. Nuevos dominios
   Crea un `CognitiveProfile` con palabras clave y patrones propios del dominio.

2. Memoria persistente
   Sustituye la lista de `MemoryPattern` por patrones cargados desde base de datos,
   vector store o fichero versionado. La capa `Subconsciente` no necesita cambiar.

3. Politicas de conflicto
   Inyecta otro `ConflictDetector` si el dominio requiere conflictos mas finos,
   por ejemplo `lealtad_vs_ambicion` o `energia_vs_compromiso`.

4. Criterio superior
   Extiende `MaestroInterior` para anadir criterios como impacto sistemico,
   alineacion con principios o coste reversible/irreversible.

## Contrato de trazabilidad

Toda decision final debe conservar:

- salida del ego
- salida del subconsciente
- criterios del maestro interior
- conflictos detectados
- contexto original
- `execution_log` paso a paso

Esto permite depurar por que se decidio algo, que capa influyo y donde aparecio
el conflicto.
