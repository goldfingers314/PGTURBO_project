BEGIN;
SELECT taxonomy.specialization, addresses.phone 
FROM taxonomy,addresses WHERE addresses.id = taxonomy.id ;
END;
BEGIN;
CREATE INDEX test_id1 ON core_npi USING hash("npi");
SELECT COUNT(*) FROM core_npi WHERE core_npi.npi LIKE "1%" GROUP BY core_npi.last_name;
DROP INDEX test_id1;
END;
BEGIN;
SELECT addresses.city,addresses.phone 
FROM addresses WHERE addresses.state = 'California' ;
END;
BEGIN;
SELECT core_npi.last_name, core_npi.first_name, core_npi.phone
FROM core_npi WHERE core_npi.phone IS NOT NULL;
END;
BEGIN;
SELECT count(npi.entity_type) 
FROM npi GROUP BY npi.entity_type;
END;
BEGIN;
SELECT taxonomy.classification, taxonomy.effective_date 
from taxonomy where taxonomy.effective_date NOT BETWEEN '2004-02-01' AND '1989-06-04';
END;
BEGIN;
SELECT npi.org_name 
FROM npi WHERE npi.org_name NOT LIKE '2%';
END;
BEGIN;
SELECT count(npi_taxonomy.taxonomy)
FROM npi_taxonomy GROUP BY npi_taxonomy.taxonomy HAVING npi_taxonomy.taxonomy IS NOT NULL;
END;
BEGIN;
SELECT shortened_npi.entity_type,addresses.line_1,addresses.line_2 
FROM (SELECT * FROM npi WHERE npi.addr_mail_phone LIKE '510%') AS shortened_npi INNER JOIN addresses ON CAST(shortened_npi.npi AS VARCHAR) LIKE '2%';
END;
BEGIN;
SELECT npi_taxonomy.npi, npi_taxonomy.license_num, temp_table.id 
FROM (SELECT * FROM addresses WHERE addresses.state = 'Kentucky') AS temp_table LEFT JOIN npi_taxonomy ON npi_taxonomy.license_num IS NOT NULL;
END;
BEGIN;
CREATE INDEX test_id2 ON addresses using gin(city);
DROP INDEX test_id2;
END;
BEGIN;
CREATE INDEX test_id3
ON taxonomy USING gist(specialization);
SELECT * FROM taxonomy WHERE taxonomy.specialization = "ENT";
DROP INDEX test_id3
END;


  
