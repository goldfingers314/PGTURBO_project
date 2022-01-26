#! bin/bash
pgbench -i provider_lookup
if [ ! -f "sample.csv" ]; then
sudo touch sample.csv
echo "tsp_avg","shared_buffers","temp_buffers","work_mem","hash_mem_multiplier","maintenance_work_mem","autovacuum_work_mem","logical_decoding_work_mem","max_stack_depth","temp_file_limit"\
,"backend_flush_after","effective_io_concurrency","maintenance_io_concurrency","max_worker_processes","max_parallel_workers_per_gather","max_parallel_maintenance_workers",\
"max_parallel_workers","parallel_leader_participation","checkpoint_completion_target","checkpoint_flush_after","cpu_index_tuple_cost","cpu_operator_cost","min_parallel_table_scan_size",\
"min_parallel_index_scan_size","effective_cache_size","jit_above_cost","jit_inline_above_cost","jit_optimize_above_cost","geqo_threshold","geqo_effort","geqo_pool_size","geqo_generations",\
"geqo_selection_bias","geqo_seed","default_statistics_target","constraint_exclusion","cursor_tuple_fraction","from_collapse_limit","join_collapse_limit","plan_cache_mode",\
"autovacuum_max_workers","autovacuum_vacuum_threshold","autovacuum_vacuum_insert_threshold","autovacuum_analyze_threshold","autovacuum_vacuum_scale_factor","autovacuum_vacuum_insert_scale_factor",\
"autovacuum_analyze_scale_factor","autovacuum_freeze_max_age","autovacuum_multixact_freeze_max_age","autovacuum_vacuum_cost_delay","autovacuum_vacuum_cost_limit","deadlock_timeout",\
"max_locks_per_transaction","max_pred_locks_per_transaction","max_pred_locks_per_relation","max_pred_locks_per_page" >> sample.csv
fi

