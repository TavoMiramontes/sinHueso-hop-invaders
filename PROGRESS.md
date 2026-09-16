# Hop Invaders: Defiende Sin Hueso — Avance del proyecto

Juego arcade retro 2D para la nanocervecería **Sin Hueso!**, pensado para jugarse en el taproom vía tag NFC. Shooter tipo Space Invaders con partidas de 60 segundos.

> *"Las cervezas sin sabor han invadido Sin Hueso. Tu misión es defender el último lote de cerveza artesanal."*

## Estado actual: Etapas 1-8 completas — juego publicado 🚀 (falta 6.3: NFC)

### Etapa 8 hecha (huida a velocidad luz: bonus tras vencer al Rey Hueso)
- 8.1 ✅ Idea del usuario. Antes, vencer al Rey con tiempo de sobra dejaba la pantalla vacía hasta el 0:00 (30 pts/s por esperar). Ahora la singularidad colapsa y la nave escapa a velocidad luz esquivando los restos de la batalla (rocas, huesos, cráneos, latas, botellas), SIN disparar. Estado `warp` en `index.html`: succión 1.3 s → escombros que caen girando con estela, la mayoría apuntados al tarro → "¡ESCAPASTE!" 1.4 s → pantalla final. Entra sólo con ≥3 s de sobra (`warpMinTime`); los 30 pts/s se siguen pagando y encima suma 10 pts por escombro esquivado, racha x2 a los 5 seguidos y x3 a los 10; chocar rompe la racha pero **nunca quita pinta ni partida** (ya está ganada). Línea nueva en el desglose final: "HUIDA A VELOCIDAD LUZ +N". Música propia (arpegios a 168 bpm). Atajo de prueba `?warp=1` (entra directo con 12 s).
- 8.2 ✅ Afinado con el usuario en celular: primera vuelta "lentos y muy fácil" → 780 px/s, escombros cada 0.30→0.17 s, 75% apuntados. Marcador `ESQUIVADOS n · RACHA xK` a tamaño 2 (a tamaño 1 no se leía). Simulación sin navegador (`smoke.js` en scratchpad, stub de canvas, 60 fps): el que esquiva saca ~1080 en 12 s, el quieto ~130. Dos fugas cazadas sólo por simular: con x al azar el quieto esquivaba el 95%, y los escombros que atravesaban al tarro durante el parpadeo contaban como esquivados. Una huida perfecta de 12 s vale ~1300 (> Rey Hueso 750); si pesa de más, bajar `warpDodgePts`.
- Ranking: la pestaña MES ahora es mes calendario (arranca el día 1) y cada pestaña muestra su periodo debajo ("SEPTIEMBRE 2026"). El usuario decidió NO borrar puntajes viejos (251 en dos meses contra 500 MB del plan Free); `supabase-limpieza-mensual.sql` (pg_cron, conserva top 10 + mes) queda escrito pero sin activar.
- QR de marca para el juego y para Instagram en `qr/` (SVG + PNG), generados y verificados por `tools/qr_gen.py`.

### Etapa 7 hecha (calendario de eventos, 3 temas nuevos y ráfaga de puntos dobles)
- 7.1 ✅ Calendario automático `EVENT_CALENDAR`: con `active_event='auto'` (el modo normal) el juego elige el tema por fecha, incluso sin conexión. Ventanas: 💘 San Valentín 10–14 feb · 🎂 Aniversario todo junio · 🇲🇽 Fiesta Mexicana 1–16 sep y 15–20 nov · 🍺 Oktoberfest 20 sep–5 oct · 👻 Halloween 24–31 oct · 💀 Día de Muertos 1–2 nov · 🎄 Navidad 1 dic–6 ene. El admin puede forzar cualquier tema o apagarlos ('none'). "Independencia" se renombró a "Fiesta Mexicana" (alias del valor viejo incluido). Power-ups bajados a 8% de drop (pedido del usuario).
- 7.2 ✅ Temas nuevos: San Valentín (corazones/rosas/pétalos, red ale fija), Día de Muertos (cempasúchil/velas/papel picado, separado de Halloween a propósito), Aniversario (gorritos/globos/confeti, Las Mañanitas en chiptune, banner "★ N AÑOS DE SIN HUESO ★" calculado desde junio 2023, tarro aleatorio con `mug: null`). Motor: `ambientColors` por tema y `banner` para personalizar el letrero del título.
- 7.3 ✅ Evento ráfaga ⚡ PUNTOS DOBLES: interruptor manual en admin.html (columna `double_points` en `config`, NO va en el calendario por decisión del dueño). Duplica todo (enemigos, racha, jefe +1500, bonos finales); avisos en título (parpadeante), HUD y arranque. Previsualización con `?doble=1`. Tope anti-trampa de 30k sigue holgado (~8k por partida doble). Verificado por el usuario contra su Supabase real.
- Tests en scratchpad: calendar_test.js (25 casos de fechas), themes_test.js (arranque con los 7 temas + alias + auto), doble_test.js (duplicación unitaria + partida completa).

### Etapa 6 (casi cerrada)
- 6.1 ✅ Temas de eventos como paquetes de datos en `THEMES` (fondo, sombreros pixel, decoración parallax, clima nieve/papel picado, tarro fijo, música). Previsualización con `?evento=X`; producción vía admin.html→Supabase. Para un evento nuevo: entrada en THEMES + ventana en EVENT_CALENDAR (opcional) + option en admin.html + push. La BD ya no valida nombres de eventos (constraint eliminado por el usuario).
- 6.2 ✅ Publicado en GitHub Pages: repo público `TavoMiramontes/sinHueso-hop-invaders` (rama master), URL https://tavomiramontes.github.io/sinHueso-hop-invaders/ — esta es la URL para el tag NFC. GitHub Action `keepalive.yml` hace ping al ranking lunes y jueves para que Supabase Free no se pause. Nota: git en esta máquina requirió `http.sslBackend schannel`; curl requiere `--ssl-no-revoke`.
- 6.3 pendiente: prueba de punta a punta con NFC/QR y cierre.

### Etapa 5 hecha (Supabase conectado y verificado con el proyecto real del usuario)
- Proyecto Supabase `hop-invaders` creado por el usuario; llaves en `config.js` (anon, pública por diseño).
- `supabase-schema.sql`: tabla `scores` (RLS: lectura/inserción públicas, borrado solo autenticado; CHECKs anti-trampa verificados: score ≤30000 rechazado en vivo) y tabla `config` (`active_event`).
- Juego: guarda en la nube ("GUARDANDO..."), pestañas consultan Supabase (top 50), fila propia resaltada por id remoto, fallback offline a localStorage con aviso "SIN CONEXIÓN". `ACTIVE_EVENT` se lee al cargar (re-skins en Etapa 6).
- `admin.html`: login del dueño (usuario creado en Authentication), selector de evento, borrado individual y total de puntajes.
- `?reset` en la URL limpia datos locales del dispositivo (récord personal 'sh_best', ranking local, nombre).
- Free tier: ojo con la pausa tras 7 días sin actividad → en Etapa 6 agregar ping automático (GitHub Action).

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

### Etapa 3 hecha (validada por el usuario: "casi imposible ganarle, genial")
- 👹 Rey Hueso = la mano de la etiqueta (`IMG_4624.png`) con corona y ojo en la palma; emerge de la singularidad al seg 40 (erupción + fondo rojizo de tensión). 52 HP, ráfagas dirigidas, abanicos de orbes y ataque en picada. +750 al derrotarlo.
- Fondo parallax: nebulosas, singularidad animada (disco de acreción), elementos de la etiqueta (máscara/flores/hongos), insumos (lúpulo/trigo/barril/olla/botella) y el borracho flotante con hipo.
- Power-ups: 🍃 doble, 🔥 triple, 🍺 barril limpia-pantalla, ⚡ nitro (+80%, estela), ❤️ +1 pinta (13%). 11% de drop; durante el jefe caen del cielo cada ~5s.
- CAOS FINAL (últimos 10s con jefe vivo): todo más rápido, lluvia de orbes, huesos kamikaze, el borracho lanza botellazos.
- REGLA: solo ganas si derrotas al Rey Hueso; si el tiempo acaba con él vivo → cataclismo (todo explota, "EL REY HUESO GANÓ").
- Balas cambian de color: por oleada (teal→cian→verde→amarillo→ámbar→rojo) y por arma (verde=hop, fuego=IPA).
- Bonos: +100 por 15s sin daño (racha), +500 por sobrevivir (solo al ganar).
- Ajustes post-prueba: jefe a 42 HP (calibrado con el usuario), al vencerlo la onda barre a los enemigos restantes y ya no aparece nada más.
- 5 estilos de cerveza aleatorios por partida para el tarro (IPA/Pilsner/Red/Brown/Stout, aviso "HOY SIRVES: X", iconos de vida a juego); `EVENT_MUG` fija el estilo durante eventos (Etapa 6).
- Troleo del borracho: 30% de las victorias, botellazo al letrero a los 3s → "¡LOTE NO DEFENDIDO! EL BORRACHO TENÍA OTROS PLANES JAJA" (cosmético, los puntos cuentan).

### Etapa 4 hecha (validada por el usuario en PC y celular)
- Flujo final: RESULTADO (rango ⭐-⭐⭐⭐: 3=vencer al jefe, 2=1200+ pts o 40s+) → captura de nombre (overlay HTML, ≤10 chars, filtro de groserías con normalización de acentos/leet) → Salón de la Fama local (localStorage `sh_scores`, máx 500) con pestañas HOY/SEMANA/MES/TOTAL tocables, top 10, entrada propia resaltada, "TU MEJOR/PUESTO #N" → JUGAR DE NUEVO.
- Audio Web Audio API: ~16 SFX + secuenciador chiptune con 4 pistas (main 108bpm, boss 150bpm con tritono y +18% en caos, victory loop, defeat loop; el loop final suena hasta la próxima partida; el troleo cambia a defeat). Botón mute (esquina inf. der., tecla M), preferencia en `sh_mute`.
- Desbloqueo de audio: 1er toque en título despierta la música (patrón insert-coin), 2º juega; en móvil el desbloqueo real ocurre en pointerup/touchend (regla de los navegadores). Si no hay AudioContext, el 1er toque juega directo.
- Power-up nuevo: 🛡️ Escudo de Espuma (8% el más raro, 5s, absorbe todo el daño, burbuja pixelada que parpadea al acabarse).
- Troleo del borracho reducido a 8% de las victorias.
- Logo `sh_logo.jpeg` pixelizado en el título (56x56, blanco→transparente; requiere http, con file:// se omite sin error).
- Pruebas en Node (scratchpad): smoke.js (partida completa/inmortal) y fame_test.js (flujo nombre→filtro→ranking→pestañas→reinicio).

### Siguiente paso: Etapa 5 — Salón de la Fama real (Supabase)

### Etapas restantes
- **Etapa 5:** Supabase — tabla `scores` con RLS y CHECK anti-trampa, tabla `config`, ranking compartido con fallback offline a localStorage, `admin.html` con login del dueño, `supabase-schema.sql`, README.
- **Etapa 6:** eventos re-skin activables desde admin (Oktoberfest, Halloween, Navidad, Independencia 🇲🇽) y deploy a GitHub Pages (URL para el tag NFC).

## Notas técnicas
- Resolución lógica 480×720 escalada con `image-rendering: pixelated`.
- Todo lo calibrable está en el objeto `CFG` al inicio del script; colores en `PAL`; tipos de enemigo en `ETYPES`.
- Prueba de humo: existe un script que simula 70s de partida con DOM stub en Node (en el scratchpad de la sesión; recrearlo es trivial si hace falta).
- La precisión cuenta *impactos* por bala (pegarle 3 veces a una calavera = 3 impactos).
