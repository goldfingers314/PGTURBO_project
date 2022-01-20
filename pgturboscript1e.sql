BEGIN;
SELECT count(npi_taxonomy.taxonomy)
FROM npi_taxonomy GROUP BY npi_taxonomy.taxonomy HAVING npi_taxonomy.taxonomy IS NOT NULL;
END;
