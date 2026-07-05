# Hop Invaders: Defiende Sin Hueso — Avance del proyecto

Juego arcade retro 2D para la nanocervecería **Sin Hueso!**, pensado para jugarse en el taproom vía tag NFC. Shooter tipo Space Invaders con partidas de 60 segundos.

> *"Las cervezas sin sabor han invadido Sin Hueso. Tu misión es defender el último lote de cerveza artesanal."*

## Estado actual: Etapas 1 y 2 completas ✅

**El plan completo por etapas está al final de este archivo.** Trabajamos etapa por etapa: el usuario prueba cada una (PC + celular) y se ajusta antes de avanzar.

### Hecho hasta ahora
- `index.html` — juego completo autocontenido (canvas 2D, JS vanilla, sin dependencias). Pixel art y fuente pixel (con acentos ÁÉÍÓÚÑ) dibujados 100% por código.
- Paleta de la marca (de `sh_logo.jpeg`): azul petróleo `#0d3b4f`, ámbar `#d9971e`, espuma `#f4efe6`.
- Jugador: tarro de cerveza, disparo automático, ← →/A-D o arrastre táctil, 3 pintas de vida.
- Enemigos: 🦴 Hueso (1 vida, 10 pts, ojos rojos), 💀 Calavera (3 vidas, 25 pts, ojos púrpura), 🥫 Lata (2 vidas, 40 pts, franja roja, dispara gotas), 🍺 Cerveza industrial (1 vida, 50 pts, botella verde, zigzag rápido).
- Oleadas paramétricas que se enciman, descenso continuo, cambios de dirección aleatorios, ataques en picada estilo Galaxian, flash blanco de daño.
- Partida de 60s, HUD (score/tiempo/pintas/oleada), pantalla de título con tabla de puntos, pantalla de fin con precisión %, récord en localStorage.
- `serve.js` — servidor local para probar en el celular: `node serve.js` → abrir `http://<IP-de-la-PC>:8080` (misma WiFi; la IP la imprime el script).
- Calibración validada por el usuario: movimiento y disparo bien; dificultad "un poco fácil" aún — se espera que la Etapa 3 (jefe) la suba.

### Siguiente paso: Etapa 3 — Rey Hueso, power-ups y bonos
- 👹 Rey Hueso aparece al segundo 40: barra de vida, ráfagas, patrón de movimiento. 500 pts + 250 de bonus por derrotarlo.
- Power-ups que sueltan enemigos: 🍃 Hop Shot (doble disparo), 🔥 Triple IPA (triple), 🍺 Barril Explosivo (limpia pantalla), ⚡ Nitro (velocidad), ❤️ Vida extra.
- Bonos: +100 por 15s sin daño, +500 por sobrevivir el minuto.

### Etapas restantes
- **Etapa 4:** resultado con rango ⭐–⭐⭐⭐, captura de nombre (≤10 chars, filtro de groserías), Salón de la Fama local con pestañas Hoy/Semana/Mes/Histórico, audio chiptune (Web Audio API) + botón mute.
- **Etapa 5:** Supabase — tabla `scores` con RLS y CHECK anti-trampa, tabla `config`, ranking compartido con fallback offline a localStorage, `admin.html` con login del dueño, `supabase-schema.sql`, README.
- **Etapa 6:** eventos re-skin activables desde admin (Oktoberfest, Halloween, Navidad, Independencia 🇲🇽) y deploy a GitHub Pages (URL para el tag NFC).

## Notas técnicas
- Resolución lógica 480×720 escalada con `image-rendering: pixelated`.
- Todo lo calibrable está en el objeto `CFG` al inicio del script; colores en `PAL`; tipos de enemigo en `ETYPES`.
- Prueba de humo: existe un script que simula 70s de partida con DOM stub en Node (en el scratchpad de la sesión; recrearlo es trivial si hace falta).
- La precisión cuenta *impactos* por bala (pegarle 3 veces a una calavera = 3 impactos).
