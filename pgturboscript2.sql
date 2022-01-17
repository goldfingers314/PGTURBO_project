BEGIN;
SELECT npi.entity_type,addresses.line1,addresses.line2 
FROM npi INNER JOIN addresses ON CAST(npi.npi AS VARCHAR) LIKE '2%';
END;





ubunutu