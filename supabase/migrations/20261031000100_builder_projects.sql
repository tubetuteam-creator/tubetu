-- TUBETU website builder projects and public publishing
create table if not exists public.builder_projects (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  slug text not null unique,
  title text not null default 'Новый сайт',
  template text not null default 'pitstop',
  data jsonb not null default '{}'::jsonb,
  is_published boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  published_at timestamptz
);
alter table public.builder_projects enable row level security;
drop policy if exists "Owners can read own builder projects" on public.builder_projects;
create policy "Owners can read own builder projects" on public.builder_projects
for select to authenticated using (auth.uid() = owner_id);
drop policy if exists "Anyone can read published builder projects" on public.builder_projects;
create policy "Anyone can read published builder projects" on public.builder_projects
for select to anon, authenticated using (is_published = true);
drop policy if exists "Owners can create builder projects" on public.builder_projects;
create policy "Owners can create builder projects" on public.builder_projects
for insert to authenticated with check (auth.uid() = owner_id);
drop policy if exists "Owners can update builder projects" on public.builder_projects;
create policy "Owners can update builder projects" on public.builder_projects
for update to authenticated using (auth.uid() = owner_id) with check (auth.uid() = owner_id);
drop policy if exists "Owners can delete builder projects" on public.builder_projects;
create policy "Owners can delete builder projects" on public.builder_projects
for delete to authenticated using (auth.uid() = owner_id);
grant select, insert, update, delete on public.builder_projects to authenticated;
grant select on public.builder_projects to anon;
create index if not exists builder_projects_owner_updated_idx on public.builder_projects(owner_id, updated_at desc);
