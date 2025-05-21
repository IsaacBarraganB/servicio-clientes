CREATE OR REPLACE VIEW view_suppliers_options
as
SELECT id,
id as value,
company_name as label,
account_id
FROM ctg_suppliers;