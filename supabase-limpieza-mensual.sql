-- ============================================================
--  HOP INVADERS — limpieza mensual del ranking (OPCIONAL)
--
--  No hace falta por espacio: cada puntaje pesa ~150 bytes con todo e
--  índices y el plan Free da 500 MB. Esto es solo para quien quiera la
--  tabla chica. El día 1 de cada mes borra todo MENOS:
--    - el top 10 histórico (las leyendas se quedan para siempre)
--    - los puntajes del mes que acaba de empezar
--
--  Cómo activarlo:
--    1. Dashboard → Database → Extensions → buscar "pg_cron" → Enable
--    2. SQL Editor → New query → pegar este archivo → Run
--  Para desactivarlo:  select cron.unschedule('limpieza-mensual');
--  Para ver el historial:  select * from cron.job_run_details order by start_time desc limit 10;
-- ============================================================

-- Prueba en seco: cuántos puntajes borraría HOY si corriera ahora mismo.
-- Correr esto solo, antes de programar nada, para ver que el número tenga sentido.
select count(*) as se_borrarian
from public.scores
where created_at < (date_trunc('month', now() at time zone 'America/Mexico_City')
                    at time zone 'America/Mexico_City')
  and id not in (select id from public.scores order by score desc, created_at asc limit 10);

-- Programación. Supabase corre pg_cron en UTC; 06:05 UTC son las 00:05 en
-- CDMX (México ya no cambia de horario desde 2022). Volver a correr esto
-- con el mismo nombre reemplaza el job, no lo duplica.
select cron.schedule(
  'limpieza-mensual',
  '5 6 1 * *',
  $$
    delete from public.scores
    where created_at < (date_trunc('month', now() at time zone 'America/Mexico_City')
                        at time zone 'America/Mexico_City')
      and id not in (select id from public.scores order by score desc, created_at asc limit 10);
  $$
);
