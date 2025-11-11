-- backend/migrations/versions/116186a328fb49cdbdd923248dad1a54_admin_functions.sql
-- SECURITY DEFINER helper functions for admin operations (skeleton)
BEGIN;
CREATE OR REPLACE FUNCTION public.admin_delete_org(p_org uuid, p_reason text, p_actor uuid)
RETURNS void AS $$
BEGIN
  -- example: log and remove tenant metadata; actual data wipe handled by admin worker
  INSERT INTO public.admin_audit (actor_id, action, target_type, target_id, details)
  VALUES (p_actor, 'admin_delete_org', 'org', p_org, json_build_object('reason', p_reason));
  -- perform limited metadata cleanup
  DELETE FROM public.org_subscriptions WHERE org_id = p_org;
  -- DO NOT DROP DATA TABLES HERE; call controlled worker for full wipe
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
COMMIT;
