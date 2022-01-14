# PGTURBO_project
This is our pgturbo app. It tunes databases with medical data in mind. This is for EMR Technologies (company)

Pgturbo is a project for automatically tuning the postgres database using statistical learning methods. The tuning is primarily for medical information involving providers, patients, and claims. We use pgbench as a tool for benchmarking our database configuration. We obtain the tps for our database through pgbench, and a custom script developed to imitate medical queries. The next step of our project involves a thorough analysis of the various parameters that control the performance of the database, along with some pruning to reduce the number of variables involved in the optimization process. 
The final step uses effective optimization algorithms to choose the best possible configration for the database.


