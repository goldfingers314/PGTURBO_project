BEGIN;
SELECT npi_taxonomy.npi, npi_taxonomy.license_num, addresses.id 
FROM addresses LEFT JOIN npi_taxonomy ON npi_taxonomy.license_num IS NOT NULL;
END;