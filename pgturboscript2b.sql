BEGIN;
SELECT npi_taxonomy.npi, npi_taxonomy.license_num, temp_table.id 
FROM (SELECT * FROM addresses WHERE addresses.state = 'Kentucky') AS temp_table LEFT JOIN npi_taxonomy ON npi_taxonomy.license_num IS NOT NULL;
END;
