# Seguimiento de cambios

## Estado actual

El repositorio Git esta activo en la carpeta del proyecto y VS Code queda configurado para mostrar:

- Cambios por archivo en Source Control.
- Decoraciones de lineas modificadas.
- Diffs lado a lado.
- Historial reciente mediante tarea.
- GitLens como extension recomendada.

## Tareas disponibles en VS Code

Abre `Terminal > Run Task`:

- `Git: estado de cambios`
- `Git: diff sin stage`
- `Git: historial reciente`

## Politica de commits

Antes de cada commit:

1. Ejecutar `Khaba Core: ejecutar tests`.
2. Revisar `Git: diff sin stage`.
3. Crear un commit con mensaje concreto y en presente.

Ejemplo:

```bash
git add .
git commit -m "Configura entorno Visual Studio Code"
```
