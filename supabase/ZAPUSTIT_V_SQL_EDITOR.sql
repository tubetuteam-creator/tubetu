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
-- TUBETU: конкурс рисунков с голосованием + подписка на новости
-- Запустить один раз в Supabase → SQL Editor (после 20261123000100_reviews.sql).
-- Рисунок появляется в галерее только после проверки: Table Editor → drawings → status = 'approved'.

-- 1) Хранилище картинок
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('drawings', 'drawings', true, 5242880, array['image/jpeg','image/png','image/webp'])
on conflict (id) do nothing;

drop policy if exists "Parents upload drawings to own folder" on storage.objects;
create policy "Parents upload drawings to own folder"
  on storage.objects for insert to authenticated
  with check (bucket_id = 'drawings' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "Anyone can view drawings" on storage.objects;
create policy "Anyone can view drawings"
  on storage.objects for select to anon, authenticated
  using (bucket_id = 'drawings');

-- 2) Рисунки
create table if not exists public.drawings (
  id bigint generated always as identity primary key,
  owner_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  child_name text not null check (char_length(child_name) between 2 and 20),
  child_age smallint check (child_age between 1 and 17),
  hero text not null default '' check (char_length(hero) <= 20),
  image_path text not null check (char_length(image_path) <= 200),
  status text not null default 'pending' check (status in ('pending','approved','rejected')),
  votes integer not null default 0,
  created_at timestamptz not null default now()
);
alter table public.drawings enable row level security;

drop policy if exists "Approved drawings are public" on public.drawings;
create policy "Approved drawings are public" on public.drawings for select
  to anon, authenticated using (status = 'approved' or owner_id = auth.uid());

drop policy if exists "Parents add own drawings" on public.drawings;
create policy "Parents add own drawings" on public.drawings for insert
  to authenticated with check (owner_id = auth.uid() and status = 'pending' and votes = 0);

grant select on public.drawings to anon, authenticated;
grant insert (child_name, child_age, hero, image_path) on public.drawings to authenticated;

-- 3) Голоса: один голос от одного взрослого за один рисунок
create table if not exists public.drawing_votes (
  drawing_id bigint not null references public.drawings(id) on delete cascade,
  voter_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (drawing_id, voter_id)
);
alter table public.drawing_votes enable row level security;

drop policy if exists "Voters see own votes" on public.drawing_votes;
create policy "Voters see own votes" on public.drawing_votes for select
  to authenticated using (voter_id = auth.uid());

drop policy if exists "Parents vote once" on public.drawing_votes;
create policy "Parents vote once" on public.drawing_votes for insert
  to authenticated with check (voter_id = auth.uid()
    and exists (select 1 from public.drawings d where d.id = drawing_id and d.status = 'approved'));

grant select, insert (drawing_id) on public.drawing_votes to authenticated;

create or replace function public.tubetu_count_vote() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  update public.drawings set votes = votes + 1 where id = new.drawing_id;
  return new;
end $$;

drop trigger if exists tubetu_vote_added on public.drawing_votes;
create trigger tubetu_vote_added after insert on public.drawing_votes
  for each row execute function public.tubetu_count_vote();

-- 4) Подписка на новости
create table if not exists public.subscribers (
  id bigint generated always as identity primary key,
  email text not null unique check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$' and char_length(email) <= 120),
  created_at timestamptz not null default now()
);
alter table public.subscribers enable row level security;

drop policy if exists "Anyone can subscribe" on public.subscribers;
create policy "Anyone can subscribe" on public.subscribers for insert
  to anon, authenticated with check (true);

grant insert (email) on public.subscribers to anon, authenticated;
