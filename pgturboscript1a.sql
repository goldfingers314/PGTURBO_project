BEGIN;
SELECT core_npi.last_name, core_npi.first_name, core_npi.phone
FROM core_npi WHERE core_npi.phone IS NOT NULL;
END;
