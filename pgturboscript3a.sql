BEGIN;
CREATE INDEX test_id1 ON core_npi USING hash("npi");
SELECT COUNT(*) FROM core_npi WHERE CAST(core_npi.npi AS VARCHAR) LIKE '1%' GROUP BY core_npi.last_name;
DROP INDEX test_id1;
END;
