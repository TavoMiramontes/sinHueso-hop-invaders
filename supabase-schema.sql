-- ============================================================
--  HOP INVADERS: Defiende Sin Hueso — esquema de Supabase
--  Pegar TODO este archivo en: SQL Editor → New query → Run
-- ============================================================

-- Tabla de puntajes del Salón de la Fama
create table if not exists public.scores (
  id bigint generated always as identity primary key,
  name text not null check (char_length(name) between 1 and 10),
  -- validación anti-trampa: rangos imposibles se rechazan en el servidor
  score integer not null check (score between 0 and 30000),
  accuracy integer not null default 0 check (accuracy between 0 and 100),
  kills integer not null default 0 check (kills between 0 and 500),
  stars smallint not null default 1 check (stars between 1 and 3),
  created_at timestamptz not null default now()
);

create index if not exists scores_score_idx on public.scores (score desc);
create index if not exists scores_created_idx on public.scores (created_at desc);

alter table public.scores enable row level security;

-- cualquiera puede leer el ranking y registrar su puntaje;
-- solo el dueño (autenticado en admin.html) puede borrar
create policy "lectura publica" on public.scores
  for select using (true);
create policy "insercion publica" on public.scores
  for insert with check (true);
create policy "borrado solo dueno" on public.scores
  for delete to authenticated using (true);

-- Configuración del juego (eventos especiales, Etapa 6)
-- 'auto' = el juego elige el tema según su calendario anual;
-- cualquier otro valor fuerza ese tema (los nombres viven en el JS,
-- así que agregar eventos nuevos no requiere tocar la base de datos)
create table if not exists public.config (
  id smallint primary key check (id = 1),
  active_event text not null default 'auto'
);

insert into public.config (id, active_event) values (1, 'auto')
  on conflict (id) do nothing;

alter table public.config enable row level security;

create policy "config lectura publica" on public.config
  for select using (true);
create policy "config escritura solo dueno" on public.config
  for update to authenticated using (true) with check (true);
