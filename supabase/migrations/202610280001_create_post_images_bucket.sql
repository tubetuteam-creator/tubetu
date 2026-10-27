-- TUBETU post image storage.
-- Public reads are intentional because the current frontend uses getPublicUrl().
-- Uploads are restricted to authenticated users writing into their own UID folder.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'post-images',
  'post-images',
  true,
  8388608,
  array['image/jpeg', 'image/png', 'image/webp']::text[]
)
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "TUBETU post images upload own folder" on storage.objects;
create policy "TUBETU post images upload own folder"
on storage.objects for insert to authenticated
with check (
  bucket_id = 'post-images'
  and (storage.foldername(name))[1] = auth.uid()::text
);

drop policy if exists "TUBETU post images update own folder" on storage.objects;
create policy "TUBETU post images update own folder"
on storage.objects for update to authenticated
using (
  bucket_id = 'post-images'
  and (storage.foldername(name))[1] = auth.uid()::text
)
with check (
  bucket_id = 'post-images'
  and (storage.foldername(name))[1] = auth.uid()::text
);

drop policy if exists "TUBETU post images delete own folder" on storage.objects;
create policy "TUBETU post images delete own folder"
on storage.objects for delete to authenticated
using (
  bucket_id = 'post-images'
  and (storage.foldername(name))[1] = auth.uid()::text
);

-- Public bucket URLs can read images without a signed URL.
-- Allow authenticated object listing only within the user's own folder.
drop policy if exists "TUBETU post images list own folder" on storage.objects;
create policy "TUBETU post images list own folder"
on storage.objects for select to authenticated
using (
  bucket_id = 'post-images'
  and (storage.foldername(name))[1] = auth.uid()::text
);
