BEGIN;
SELECT taxonomy.specialization, addresses.phone 
FROM taxonomy,addresses WHERE addresses.id = taxonomy.id ;
END;
