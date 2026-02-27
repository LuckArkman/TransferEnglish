-- Row-Level Security (RLS) Configuration Script
-- Note: This is a template. Final implementation will be handled via Alembic migrations.

-- Enable RLS for each tenant-isolated table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create a policy that restricts access based on the 'app.current_tenant' session variable
-- This ensures that users can only see/modify data belonging to their own tenant
CREATE POLICY tenant_isolation_policy ON users
    USING (tenant_id = current_setting('app.current_tenant'))
    WITH CHECK (tenant_id = current_setting('app.current_tenant'));

-- Supersu (Admin) bypass policy (Optional, for platform management)
-- CREATE POLICY superuser_bypass ON users 
--     USING (current_setting('app.is_superuser', true) = 'true');
