BEGIN;
SELECT taxonomy.classification, taxonomy.effective_date 
from taxonomy where taxonomy.effective_date NOT BETWEEN '2004-02-01' AND '1989-06-04';
END;
