-- TUBETU B2B company storefront profiles
-- Apply this migration in the Supabase SQL Editor before using cloud persistence.

create table if not exists public.company_profiles (
  owner_id uuid primary key references auth.users(id) on delete cascade,
  company_name text not null default '',
  visibility text not null default 'Публичный'
    check (visibility in ('Закрытый', 'Частично открытый', 'Публичный')),
  about text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.company_profiles enable row level security;

drop policy if exists "Users can view own company profile" on public.company_profiles;
create policy "Users can view own company profile"
  on public.company_profiles for select
  to authenticated
  using (auth.uid() = owner_id);

drop policy if exists "Users can insert own company profile" on public.company_profiles;
create policy "Users can insert own company profile"
  on public.company_profiles for insert
  to authenticated
  with check (auth.uid() = owner_id);

drop policy if exists "Users can update own company profile" on public.company_profiles;
create policy "Users can update own company profile"
  on public.company_profiles for update
  to authenticated
  using (auth.uid() = owner_id)
  with check (auth.uid() = owner_id);

grant select, insert, update on public.company_profiles to authenticated;
