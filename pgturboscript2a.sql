BEGIN;
SELECT taxonomy.specialization, addresses.phone 
FROM taxonomy,addresses WHERE adresses.id = taxonomy.id ;
END;
