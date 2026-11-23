-- TUBETU: отзывы родителей с проверкой (модерацией)
-- Запустить один раз в Supabase → SQL Editor.
-- Новый отзыв приходит со статусом approved = false и на сайте не виден.
-- Чтобы показать отзыв: Table Editor → reviews → поставить approved = true.

create table if not exists public.reviews (
  id bigint generated always as identity primary key,
  name text not null check (char_length(name) between 2 and 40),
  city text not null default '' check (char_length(city) <= 40),
  text text not null check (char_length(text) between 10 and 600),
  approved boolean not null default false,
  created_at timestamptz not null default now()
);

alter table public.reviews enable row level security;

drop policy if exists "Anyone can read approved reviews" on public.reviews;
create policy "Anyone can read approved reviews"
  on public.reviews for select
  to anon, authenticated
  using (approved = true);

drop policy if exists "Anyone can send a review for moderation" on public.reviews;
create policy "Anyone can send a review for moderation"
  on public.reviews for insert
  to anon, authenticated
  with check (approved = false);

grant select (id, name, city, text, created_at) on public.reviews to anon, authenticated;
grant insert (name, city, text) on public.reviews to anon, authenticated;
