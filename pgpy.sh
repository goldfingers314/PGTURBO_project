#!bin/bash

#ensures connection
pg_isready
a=$?
while [ $a -ne 0 ]
do
brew services restart postgresql &
pg_isready 
a=$?
done

#calculates our y-vector

sudo -u postgres -H -- psql -d provider_lookup -c "CREATE TABLE dupli AS SELECT * FROM npi WHERE npi.addr_practce_state="Oklahoma""

a=$(pgbench -c 1 -t 1 -f pgturboscript4.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')
b=$(pgbench -c 1 -t 1 -f pgturboscript4a.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')
c=$(pgbench -c 1 -t 1 -f pgturboscript4b.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
d=$(pgbench -c 1 -t 1 -f pgturboscript4c.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*') 

sudo -u postgres -H -- psql -d provider_lookup -c "DROP TABLE dupli"

z=$(pgbench -c 1 -t 1 -f pgturboscript1.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
y=$(pgbench -c 1 -t 1 -f pgturboscript1a.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')  
x=$(pgbench -c 1 -t 1 -f pgturboscript1b.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
w=$(pgbench -c 1 -t 1 -f pgturboscript1c.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
v=$(pgbench -c 1 -t 1 -f pgturboscript1d.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
u=$(pgbench -c 1 -t 1 -f pgturboscript1e.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
t=$(pgbench -c 1 -t 1 -f pgturboscript2.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
s=$(pgbench -c 1 -t 1 -f pgturboscript2a.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')  
r=$(pgbench -c 1 -t 1 -f pgturboscript2b.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
q=$(pgbench -c 1 -t 1 -f pgturboscript3.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')   
p=$(pgbench -c 1 -t 1 -f pgturboscript3a.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*')
final=$(bc <<< "scale=7; ($z+$y+x+$w+v+$u+$t+$s+$r+$q+$p+$a+$b+$c+$d)/11")


#updates csv
sudo chmod -R 777 sample.csv
echo $final,"shared_buffers","temp_buffers","work_mem","hash_mem_multiplier","maintenance_work_mem",\
"autovacuum_work_mem","logical_decoding_work_mem","max_stack_depth","temp_file_limit"\
,"backend_flush_after","effective_io_concurrency","maintenance_io_concurrency","max_worker_processes",\
"max_parallel_workers_per_gather","max_parallel_maintenance_workers",\
"max_parallel_workers","parallel_leader_participation","checkpoint_completion_target","checkpoint_flush_after",\
"cpu_index_tuple_cost","cpu_operator_cost","min_parallel_table_scan_size",\
"min_parallel_index_scan_size","effective_cache_size","jit_above_cost","jit_inline_above_cost",\
"jit_optimize_above_cost","geqo_threshold","geqo_effort","geqo_pool_size","geqo_generations",\
"geqo_selection_bias","geqo_seed","default_statistics_target","constraint_exclusion","cursor_tuple_fraction",\
"from_collapse_limit","join_collapse_limit","plan_cache_mode",\
"autovacuum_max_workers","autovacuum_vacuum_threshold","autovacuum_vacuum_insert_threshold",\
"autovacuum_analyze_threshold","autovacuum_vacuum_scale_factor","autovacuum_vacuum_insert_scale_factor",\
"autovacuum_analyze_scale_factor","autovacuum_freeze_max_age","autovacuum_multixact_freeze_max_age",\
"autovacuum_vacuum_cost_delay","autovacuum_vacuum_cost_limit","deadlock_timeout",\
"max_locks_per_transaction","max_pred_locks_per_transaction","max_pred_locks_per_relation","max_pred_locks_per_page" >> sample.csv



