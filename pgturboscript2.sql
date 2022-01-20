BEGIN;
SELECT shortened_npi.entity_type,addresses.line_1,addresses.line_2 
FROM (SELECT * FROM npi WHERE npi.addr_mail_phone LIKE '510%') AS shortened_npi INNER JOIN addresses ON CAST(shortened_npi.npi AS VARCHAR) LIKE '2%';
END;




ubunutu
