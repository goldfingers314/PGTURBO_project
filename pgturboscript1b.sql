BEGIN;
SELECT count(npi.entity_type) 
FROM npi GROUP BY npi.entity_type;
END;
