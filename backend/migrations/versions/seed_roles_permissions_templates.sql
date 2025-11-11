-- Seed common roles and permissions
INSERT INTO public.permissions (codename, description)
VALUES
('admin.view', 'View admin sections'),
('admin.manage', 'Create/update admin settings'),
('users.invite', 'Invite new users'),
('roles.manage', 'Create/update roles and permissions'),
('llm.manage', 'Manage LLM provider mappings')
ON CONFLICT (codename) DO NOTHING;

-- Create roles: admin, analyst, viewer
INSERT INTO public.roles (name, description) VALUES
('admin', 'Administrator with full privileges'),
('analyst', 'Can view and analyze data'),
('viewer', 'Read-only access') ON CONFLICT (name) DO NOTHING;

-- Map permissions to roles
-- admin -> all permissions
INSERT INTO public.role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM public.roles r CROSS JOIN public.permissions p WHERE r.name='admin'
ON CONFLICT DO NOTHING;

-- analyst -> view, llm.manage (example)
INSERT INTO public.role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM public.roles r JOIN public.permissions p ON p.codename IN ('admin.view','llm.manage') WHERE r.name='analyst'
ON CONFLICT DO NOTHING;

-- viewer -> view only
INSERT INTO public.role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM public.roles r JOIN public.permissions p ON p.codename = 'admin.view' WHERE r.name='viewer'
ON CONFLICT DO NOTHING;
