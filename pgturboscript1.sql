BEGIN;
SELECT addresses.city,addresses.phone 
FROM addresses WHERE addresses.state = 'California' ;
SELECT core_npi.last_name, core_npi.first_name, core_npi.phone
FROM core_npi WHERE core_npi.phone IS NOT NULL;
SELECT count(npi.entity_type) 
FROM npi GROUP BY npi.entity_type;
-- SELECT npi.deactivate_reason, npi.last_update FROM npi where npi.addr_practice_city = "Los Angeles";
SELECT taxonomy.classification, taxonomy.effective_date 
from taxonomy where taxonomy.effective_date NOT BETWEEN '2004-02-01' AND '1989-06-04';
SELECT npi.org_name 
FROM npi WHERE npi.org_name NOT LIKE '2%';
SELECT count(npi_taxonomy.taxonomy), npi_taxonomy.tax_id 
FROM npi_taxonomy GROUP BY npi_taxonomy.taxonomy HAVING npi_taxonomy.npi LIKE '1%';
END;

  