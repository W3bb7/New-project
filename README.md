# Khaba Core

Sistema cognitivo jerarquico con tres capas:

- `Ego`: respuesta reactiva orientada a beneficio, proteccion e impulso.
- `Subconsciente`: memoria de patrones, experiencias y sesgos aprendidos.
- `MaestroInterior`: criterio final basado en coherencia, verdad y direccion.
- `KhabaCore`: orquestador del flujo completo.

## Flujo

```text
input -> Ego.response() -> Subconsciente.evaluate() -> MaestroInterior.decide() -> output
```

Cada decision incluye trazabilidad por capa, conflictos detectados y justificacion final del
maestro interior.

## Uso en Visual Studio Code

Abre `KhabaCore.code-workspace` y usa:

- `Run and Debug > Khaba Core: ejemplo`
- `Terminal > Run Task > Khaba Core: ejecutar ejemplo`
- `Terminal > Run Task > Khaba Core: ejecutar tests`

El entorno virtual vive en `.env/` y VS Code queda configurado para usarlo como interprete Python.

## Uso por terminal

```bash
python3 -m venv .env
PYTHONPATH=src .env/bin/python examples/run_decision.py
PYTHONPATH=src .env/bin/python -m unittest discover -s tests
```

## Seguimiento de cambios

El proyecto usa Git y VS Code Source Control:

- `Terminal > Run Task > Git: estado de cambios`
- `Terminal > Run Task > Git: diff sin stage`
- `Terminal > Run Task > Git: historial reciente`

Flujo recomendado:

```bash
git status --short
git diff -- .
git add .
git commit -m "Configura Khaba Core"
```
