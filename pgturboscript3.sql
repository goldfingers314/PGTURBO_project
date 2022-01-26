BEGIN;
CREATE INDEX test_id2 ON taxonomy USING BRIN("specialization");
DROP INDEX test_id2;
END;
