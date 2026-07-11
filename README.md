# 🍺 Hop Invaders: Defiende Sin Hueso

Juego arcade retro para la nanocervecería **Sin Hueso!** — shooter de 60 segundos
con Rey Hueso, power-ups y Salón de la Fama compartido.

> *"Las cervezas sin sabor han invadido Sin Hueso. Tu misión es defender el último lote de cerveza artesanal."*

## Jugar en local

- **En la PC:** abre `index.html` en el navegador (o corre `node serve.js` y entra a `http://localhost:8080`).
- **En el celular:** corre `node serve.js` en la carpeta del proyecto y abre en el
  celular la dirección que imprime (misma red WiFi). Si Windows pregunta por el
  Firewall, dale "Permitir acceso".

Sin configurar Supabase, el juego funciona completo con ranking **local**
(cada dispositivo ve solo sus puntajes).

## Configurar el Salón de la Fama compartido (Supabase)

Una sola vez, ~10 minutos:

### 1. Crear la cuenta y el proyecto
1. Entra a [supabase.com](https://supabase.com) → **Start your project** → crea tu
   cuenta (con tu correo o con GitHub).
2. **New project**: nombre `hop-invaders`, contraseña de base de datos la que
   quieras (guárdala), región `East US` o la más cercana. Plan **Free**.
3. Espera ~2 minutos a que el proyecto termine de crearse.

### 2. Crear las tablas
1. En el menú izquierdo: **SQL Editor** → **New query**.
2. Abre el archivo `supabase-schema.sql` de esta carpeta, copia TODO su
   contenido, pégalo y presiona **Run**. Debe decir "Success".

### 3. Conectar el juego
1. En el menú izquierdo: **Settings** (engrane) → **API**.
2. Copia dos cosas:
   - **Project URL** (ej. `https://abcdefgh.supabase.co`)
   - **anon public** key (la larga que empieza con `eyJ...`)
3. Pégalas en el archivo `config.js` de esta carpeta:
   ```js
   window.SH_CONFIG = {
     url: 'https://abcdefgh.supabase.co',
     key: 'eyJ...',
   };
   ```
   ⚠️ Usa la llave **anon**, nunca la `service_role`.
4. Recarga el juego. Al guardar un puntaje ya aparecerá para **todos** los
   dispositivos. Si no hay internet, el juego avisa y usa el respaldo local.

### 4. Crear tu usuario de administrador
1. En Supabase: **Authentication** → **Users** → **Add user** → **Create new user**.
2. Pon tu correo y una contraseña. Marca **Auto Confirm User**.
3. Abre `admin.html` (por http, ej. `http://localhost:8080/admin.html`) e inicia
   sesión con ese correo. Desde ahí puedes:
   - 🎃 Controlar los **eventos especiales** (ver sección siguiente).
   - ⚡ Prender/apagar la ráfaga de **PUNTOS DOBLES**.
   - 🏆 **Borrar puntajes** individuales o todo el ranking.

## Eventos especiales

El juego tiene 7 temas re-skin (fondo, sombreros de los enemigos, decoración,
clima y música propios). En el modo **⚙️ Automático** (el recomendado) se
activan solos por calendario:

| Tema | Fechas |
|---|---|
| 💘 San Valentín | 10–14 de febrero |
| 🎂 Aniversario Sin Hueso | todo junio (el "N AÑOS" se calcula solo desde 2023) |
| 🇲🇽 Fiesta Mexicana | 1–16 de septiembre y 15–20 de noviembre |
| 🍺 Oktoberfest | 20 de septiembre – 5 de octubre |
| 👻 Halloween | 24–31 de octubre |
| 💀 Día de Muertos | 1–2 de noviembre |
| 🎄 Navidad | 1 de diciembre – 6 de enero |

Desde `admin.html` puedes **forzar** cualquier tema fuera de fecha o apagarlos
todos ("Ninguno"). Aparte está la ráfaga **⚡ PUNTOS DOBLES**: un interruptor
manual (no tiene fechas) que duplica todos los puntos mientras esté encendido —
ideal para sorprender un día cualquiera en el taproom.

Previsualizar sin tocar nada: agrega `?evento=halloween` (o cualquier tema) o
`?doble=1` a la URL del juego; se pueden combinar con `&`.

Para **agregar un evento nuevo** en el futuro: entrada en `THEMES` (index.html),
ventana en `EVENT_CALENDAR` si lleva fechas, `<option>` en admin.html, y push.
No hay que tocar la base de datos.

## Seguridad (por qué esto es seguro)
- La llave `anon` es pública por diseño: lo que puede hacer está limitado por las
  **políticas RLS** del servidor — cualquiera puede leer el ranking e insertar su
  puntaje, nadie puede editar ni borrar sin tu sesión de dueño.
- **Anti-trampa:** el servidor rechaza puntajes fuera de rango (score > 30,000,
  precisión > 100%, etc.) con `CHECK` constraints; el juego además filtra
  groserías en los nombres.

## Archivos
| Archivo | Qué es |
|---|---|
| `index.html` | El juego completo (autocontenido salvo `config.js` y el cliente de Supabase) |
| `config.js` | URL y llave anon de tu proyecto Supabase |
| `supabase-schema.sql` | Se pega una vez en el SQL Editor de Supabase |
| `admin.html` | Panel del dueño: eventos y limpieza de ranking |
| `serve.js` | Servidor local para probar en el celular |
| `PROGRESS.md` | Bitácora de desarrollo por etapas |
