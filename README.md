# Cálculo Integral · Plataforma colaborativa (Fase 1)

Plataforma web interactiva para estudiar cálculo integral. Proyecto semestral de la asignatura Cálculo Integral, Tecnología en Desarrollo de Software, Universidad Tecnológica de Pereira (2026-II).

- **Sitio publicado:** `https://TU-USUARIO.github.io/calculo-integral-utp/`  *(reemplazar)*
- **Autor:** NOMBRE APELLIDO · código 000000  *(reemplazar)*

## Estado por fase

| Fase | Módulos | Estado |
|------|---------|--------|
| 1 (Parcial 1) | 1 Riemann · 2 Trapecio · 3 Punto medio · 4 Simpson · 5 Integral definida y área · 6 Integración directa | Completa |
| 2 (Parcial 2) | 7 Sustitución · 8 Exponenciales · 9 Logarítmicas · 10 Trigonométricas | Placeholder |
| 3 (Final) | 11 Trig. inversas · 12 Hiperbólicas inversas · 13 Trinomio · 14 Partes | Placeholder |

## Arquitectura

Sitio estático: HTML, CSS y JavaScript sin paso de compilación. Se despliega tal cual en GitHub Pages.

```
index.html                    Inicio con navegación a los 14 módulos
shared/style.css              Estilos (responsive, modo claro/oscuro)
shared/app.js                 Motor común: intérprete de f(x), reglas numéricas y gráficas
modules/NN-nombre/index.html  Un módulo por carpeta (teoría, visualizador, ejemplos)
tools/build.py                Generador opcional de todas las páginas
```

**Librerías (por CDN):** KaTeX (fórmulas) y Plotly.js (gráficas).

**Motor de visualizadores.** Cada módulo declara un `<div class="viz" data-mode="..." data-f="..." data-a="..." data-b="..." data-n="...">`. `app.js` lo convierte en controles (función, límites, $n$), gráfica y resultado. Modos disponibles: `riemann`, `trap`, `mid`, `simpson`, `area`, `direct`.

- El "valor de referencia" se calcula con Simpson y $n=2000$.
- Simpson fuerza $n$ par.
- En `direct`, la antiderivada $F$ se integra numéricamente con $F(a)=0$.
- Las funciones se escriben como `x^2`, `sin(x)`, `e^x`, `ln(x)`, `sqrt(x)`, `pi`. Se acepta multiplicación implícita (`2x`).

## Ejecutar localmente

```bash
python3 -m http.server 8000     # abrir http://localhost:8000
```

## Cómo contribuir

1. Cree una rama: `git checkout -b fase2-exponenciales`.
2. Abra la carpeta del módulo en `modules/` (ej. `08-exponenciales/index.html`) y reemplace el mensaje "Próximamente" con: teoría (fórmulas en `$...$` / `$$...$$`), un `<div class="viz">` si aplica y ejemplos con `<div class="ex">`.
3. Verifique cada ejemplo derivando el resultado.
4. Si añade un modo nuevo de visualización, hágalo en `shared/app.js`.
5. Abra un Pull Request con una descripción breve.

> Si edita `tools/build.py` y vuelve a ejecutarlo, **se sobrescriben** las páginas. Edite o el generador o las páginas, no ambos.

## Despliegue

Repositorio en GitHub → Settings → Pages → Branch `main`, carpeta `/ (root)`.

## Uso de IA (documentación exigida por el curso)

Según las reglas del parcial, la IA solo se permitió en la parte de software.

- **Herramienta:** Claude (Anthropic), en conversación de chat.
- **Qué generó:** estructura del sitio, `shared/app.js`, `shared/style.css`, `tools/build.py`, textos de teoría y ejemplos de los módulos 1-6, este README.
- **Qué hice yo:** *(completar: revisión, pruebas, ajustes, verificación de ejemplos, despliegue)*.
- **El taller manual (Parte I) se resolvió sin IA.**
