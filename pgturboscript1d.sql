BEGIN;
SELECT npi.org_name 
FROM npi WHERE npi.org_name NOT LIKE '2%';
END;
