BEGIN;
CREATE INDEX test_id2 ON taxonomy USING BRIN("specialization");
SELECT taxonomy.id,taxonomy.code,COUNT(taxonomy.specialization) FROM taxonomy WHERE taxonomy.specialization LIKE 's%';
DROP INDEX test_id2;
END;
