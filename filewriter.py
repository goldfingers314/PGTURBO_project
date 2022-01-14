import os
import sys
import fileinput
import itertools
import pprint


#will cap total memory at 1024 * 4 MB = memory_cap. (this is in MB!!) (for later)
#you can specify units. For now, I'm dealing with everything using mb, but you can switch to kb and bytes later.


with open('test.txt', 'r') as file:
    # read a list of lines into data
    data = file.readlines()
# print data

# print data[0]

##################### Resource Parameters (mostly memory based) ##################### 

int allotted_ram_mem = 1024*6

#!! change requires restart
shared_buffers_memory_cap = int(allotted_ram_mem*0.5)#this is in MB
shared_buffers_refineparam = 32
shared_buffers_list = [16*8+x*shared_buffers_refineparam for x in range(int(max((shared_buffers_memory_cap-16*8)/(shared_buffers_refineparam)+1,1)))]
#settings significantly higher than the minimum is needed for good performance
#reasonable starting value for shared_buggers is 25% of the memory in my system (for later optimizing)
#unlikely a value of more than 40% of memory will work better than a smaller amount
#larger settings for shared_buffers usually require a corresponding increase in max_wal_size
data[126] = 'shared_buffers = 256MB			# min 128kB\n'

#huge pages settings are all only supported on linux/windows (not macos friendly)

#!!change does not require restart
max_num_temp_buffers = int(allotted_ram_mem*0.1) #this is in MB
temp_buffers_refineparam = 4
temp_buffers_list = [1+x*temp_buffers_refineparam for x in range(int(max((max_num_temp_buffers-1)/(temp_buffers_refineparam)+1,1)))]
#min is 800KB. These are session-local buffers used only for access to temporary tables
#A session will allocate temporary buffers up to the limit given by temp_buffers
#if no temp buffers are used, then only buffer descriptor (64 bytes) is used
# if a buffer is actually used, 8 KB is used per byte.
data[132] = '#temp_buffers = 8MB			# min 800kB\n'

#we're not going to care about prepared transactions for now.

#!!change does not require restart
work_mem_memory_cap = int(allotted_ram_mem*0.02) #this is in MB
work_mem_refineparam = 1
work_mem_list = [1+x*work_mem_refineparam for x in range(int(max((work_mem_memory_cap-1)/(work_mem_refineparam)+1,1)))]
#this sets the base max amount of memory to be used by a query opteration (like sort, or hashtable)
#for a complex query, several sort or hash operations might run in parallel, so workmem is multiplied possibly by many times
#hash based operations are the usually the most memory sensitive, and mem available for hash tables = work_mem * hash_mem_multiplier
data[137] = '#work_mem = 4MB				# min 64kB\n'

#!!change does not require restart
max_num_hash_mem_multiplier = 10
hash_mem_multiplier_refineparam = 1
hash_mem_multiplier_list = [1+x*hash_mem_multiplier_refineparam for x in range(int(max((max_num_hash_mem_multiplier-1)/(hash_mem_multiplier_refineparam)+1,1)))]
#setting of 1.5 to 2.0 is good for mixes workloads
#setting 2-8 is good for environments where work_mem is at 40MB or more
#for a complex query, several sort or hash operations might run in parallel, so workmem is multiplied possibly by many times
#hash based operations are the usually the most memory sensitive, and mem available for hash tables = work_mem * hash_mem_multiplier
data[138] = '#hash_mem_multiplier = 1.0		# 1-1000.0 multiplier on hash table work_mem\n'

#!!change does not require restart
maintenance_work_mem_memory_cap = int(allotted_ram_mem*0.2) #this is in MB
maintenance_work_mem_refineparam = 32
maintenance_work_mem_list = [1+x*maintenance_work_mem_refineparam for x in range(int(max((maintenance_work_mem_memory_cap-1)/(maintenance_work_mem_refineparam)+1,1)))]
#Sets max memory amount of memory to be used by maintenance operations
#Only one of these operations can be executed at a time, so you can set it much larger than work_mem
#When autovacuum runs, up to autovacuum_max_workers*maintenance_work_mem may be allocated
data[139] = '#maintenance_work_mem = 64MB		# min 1MB\n'

#!!change does not require restart
autovacuum_work_mem_memory_cap = int(allotted_ram_mem*0.1) #this is in MB
autovacuum_work_mem_refineparam = 32
autovacuum_work_mem_list = [-1+x*autovacuum_work_mem_refineparam for x in range(int(max((autovacuum_work_mem_memory_cap)/(autovacuum_work_mem_refineparam)+1,1)))]
#Collects dead tuple identifiers, it's only able to use up to a maximum of 1GB of memory
#It defaults to -1 if maintenance work mem is being used instead
#seems useful though.
data[140] = '#autovacuum_work_mem = -1		# min 1MB, or -1 to use maintenance_work_mem\n'

#!!change does not require restart
logical_decoding_work_mem_memory_cap = int(allotted_ram_mem*0.1) #this is in MB
logical_decoding_work_mem_refineparam = 32
logical_decoding_work_mem_list = [1+x*logical_decoding_work_mem_refineparam for x in range(int(max((logical_decoding_work_mem_memory_cap-1)/(logical_decoding_work_mem_refineparam)+1,1)))]
#Each replication uses only a single buffer of this size
#Number of concurrent processes is limited by max_wal_senders
data[141] = '#logical_decoding_work_mem = 64MB	# min 64kB\n'

#!!change does not require restart
max_stack_depth_memory_cap = int(allotted_ram_mem*0.1) #this is in MB
max_stack_depth_refineparam = 2
max_stack_depth_list = [1+x*max_stack_depth_refineparam for x in range(int(max((max_stack_depth_memory_cap-1)/(max_stack_depth_refineparam)+1,1)))]
#Setting this higher than the actual kernel limit will mean that a runaway recursive function can crash an individual backend process
#Ideal setting of this parameter is the actual stack size limit enforced by the kernel
data[142] = '#max_stack_depth = 2MB			# min 100kB\n'


#!! change requires restart
#the notes said you should probably just stick with these ones.
#The last one is affected by the huge_pages setting on os where that's supported
data[143] = '#shared_memory_type = mmap		# the default is the first option\n'
data[149] = 'dynamic_shared_memory_type = posix	# the default is the first option\n'
data[156] = '#min_dynamic_shared_memory = 0MB	# (change requires restart)\n'


#!!change does not require restart
max_num_temp_file_limit = 100
temp_file_limit_refineparam = 1
temp_file_limit_list = [-1+x*temp_file_limit_refineparam for x in range(int(max((max_num_temp_file_limit)/(temp_file_limit_refineparam)+1,1)))]
#Says max number of disk space a process can use for temporary files, like sort and hash or storage for a cursor (At any instant)
#A transaction attempting to exceed this limit will be cancelled (throw an exception)
#Temp files are used for behind the scenes in query execution (disk space is used for explicit temporary tables, not this!)
data[160] = '#temp_file_limit = -1			# limits per-process temp file space\n'

#!! change does not require restart
#you care about these parameters if you will vacuuming. I guess we'll just autovacuum?
data[170] = '#vacuum_cost_delay = 0			# 0-100 milliseconds (0 disables)\n'
data[171] = '#vacuum_cost_page_hit = 1		# 0-10000 credits\n'
data[172] = '#vacuum_cost_page_miss = 2		# 0-10000 credits\n'
data[173] = '#vacuum_cost_page_dirty = 20		# 0-10000 credits\n'
data[174] = '#vacuum_cost_limit = 200		# 1-10000 credits\n'

#bgwriter autotunes itself. Only modify these if you have a demonstrated issue shown 
#by checkpoint spikes and monitoring pg_stat_bgwritter
#laptop postgresql users should set this to 60s?
data[178] = '#bgwriter_delay = 60s			# 10-10000ms between rounds\n'
data[179] = '#bgwriter_lru_maxpages = 100		# max buffers written/round, 0 disables\n'
data[180] = '#bgwriter_lru_multiplier = 2.0		# 0-10.0 multiplier on buffers scanned/round\n'
data[181] = '#bgwriter_flush_after = 0		# measured in pages, 0 disables\n'

#!! change does not require restart
max_num_backend_flush_after = 256
backend_flush_after_refineparam = 1
backend_flush_after_list = [x*backend_flush_after_refineparam for x in range(int(max((max_num_backend_flush_after)/(backend_flush_after_refineparam)+1,1)))]
#After you overload data in a single backend, then you flush some stuff to disks?
#They said number of pages after which previously perfomed writes are flushed to disk
#Range is from 0 to 256
data[185] = '#backend_flush_after = 0		# measured in pages, 0 disables\n'


#!! change does not require restart
max_num_effective_io_concurrency = 1000
effective_io_concurrency_refineparam = 1
effective_io_concurrency_list = [x*effective_io_concurrency_refineparam for x in range(int(max((max_num_effective_io_concurrency)/(effective_io_concurrency_refineparam)+1,1)))]
#Number of simultaneous requests that can be handled efficiently by the disk subsystem
#Currently, this setting only affects bitmap heap scans.
#Something about a good starting point for magnetic drives: 
#https://postgresqlco.nf/doc/en/param/effective_io_concurrency/
data[186] = '#effective_io_concurrency = 0		# 1-1000; 0 disables prefetching\n'

#!! change does not require restart
max_num_maintenance_io_concurrency = 1000
maintenance_io_concurrency_refineparam = 1
maintenance_io_concurrency_list = [x*maintenance_io_concurrency_refineparam for x in range(int(max((max_num_maintenance_io_concurrency)/(maintenance_io_concurrency_refineparam)+1,1)))]
#A variant of effective_io_concurrency that is used for maintenance work
data[187] = '#maintenance_io_concurrency = 10	# 1-1000; 0 disables prefetching\n'

#!! change requires restart
max_num_max_worker_processes = 200
max_worker_processes_refineparam = 2
max_worker_processes_list = [x*max_worker_processes_refineparam for x in range(int(max((max_num_max_worker_processes)/(max_worker_processes_refineparam)+1,1)))]
#Maximum number of background processes that the system can support
data[188] = '#max_worker_processes = 8		# (change requires restart)\n'

#!! change does not require restart
max_num_max_parallel_workers_per_gather = 1024
max_parallel_workers_per_gather_refineparam = 2
max_parallel_workers_per_gather_list = [x*max_parallel_workers_per_gather_refineparam for x in range(int(max((max_num_max_parallel_workers_per_gather)/(max_parallel_workers_per_gather_refineparam)+1,1)))]
#Maximum number of workers that can be started by a single gather or gather merge node
#Parallle queries may consume substantially more resources than nonparallel queries
#Each separate process has roughly the same impact on the system as an a additional user session
#So a parallel query using 4 workers may use up to 5 times as much CPU time, memory, I/O bandwidth, as a query with no workers at all
data[189] = '#max_parallel_workers_per_gather = 2	# taken from max_parallel_workers\n'

#!! change does not require restart
max_num_max_parallel_maintenance_workers = 1024
max_parallel_maintenance_workers_refineparam = 2
max_parallel_maintenance_workers_list = [x*max_parallel_maintenance_workers_refineparam for x in range(int(max((max_num_max_parallel_maintenance_workers)/(max_parallel_maintenance_workers_refineparam)+1,1)))]
#Sets the max number of parallel workers that can be started by a single utility command
#Parallel utility commands that support the use of parallel workers are only create index when building a B-tree index, and Vacuum without FULL option
#Parallel utility commands don't consume substantially more memory than equivalent non-parallel operations
#Resource limit for parallel utilitycommands is maintenance_work_mem (for the entire utility command, regardless the number of parallel worker processes)
#Parallel utilitu commands may still consume substantially more CPU resources and I/O bandwidth
data[190] = '#max_parallel_maintenance_workers = 2	# taken from max_parallel_workers\n'

#!! change does not require restart
max_num_max_parallel_workers = 1024
max_parallel_workers_refineparam = 2
max_parallel_workers_list = [x*max_parallel_workers_refineparam for x in range(int(max((max_num_max_parallel_workers)/(max_parallel_workers_refineparam)+1,1)))]
#Sets the max number of workers that the system can support for parallel operations
data[191] = '#max_parallel_workers = 8		# maximum number of max_worker_processes that\n'


#!! change does not require restart
parallel_leader_participation_list = ["on", "off"]
#Allows leader process to execute query plan under gather and gather merge nodes instead of waiting for worker processes
#Setting to off reduces likelihood that workers will become blocked because leader isn't reading tuples fast enough
#Off also requires leader processes to wait for worker processes to start up before the first tuples can be produced
data[193] = '#parallel_leader_participation = on\n'


#!! change requires restart
data[194] = '#old_snapshot_threshold = -1		# 1min-60d; -1 disables; 0 is immediate\n'
#This parameter tells garbage collector to get rid of data that hasn't been touched for this amount of time period
#We won't touch this

#Changes to database are first recorded to log, which is written to stable stoage before changes are made to database
#This is to ensure integrity of database
#We basically don't care about this right now since our data can be entirely scrapped and replaced if the system malfunctions?

#!! change requires restart
data[204] = '#wal_level = minimal			# minimal, replica, or logical\n'
data[219] = '#wal_log_hints = off			# also do full page writes of non-critical updates\n'
data[224] = '#wal_buffers = 4			# min 32kB, -1 sets based on shared_buffers\n'
#Let's just care about the read-only database clone, so we don't care too much about backups
#For the alternative scenario, you'd want either replica or logical.

#!! change does not require restart
data[206] = '#fsync = off				# flush data to disk for crash safety\n'
data[209] = '#synchronous_commit = off		# synchronization level;\n'
data[211] = '#wal_sync_method = fsync		# the default is the first option\n'
data[218] = '#full_page_writes = off			# recover from partial page writes\n'
data[221] = '#wal_compression = off			# enable compression of full-page writes\n'
data[222] = '#wal_init_zero = off			# zero-fill new WAL files\n'
data[223] = '#wal_recycle = on			# recycle WAL files\n'
data[226] = '#wal_writer_delay = 1ms		# 1-10000 milliseconds\n'
data[227] = '#wal_writer_flush_after = 0		# measured in pages, 0 disables\n'
data[230] = '#commit_delay = 0			# range 0-100000, in microseconds\n'
data[231] = '#commit_siblings = 5			# range 1-1000\n' #This doesn't matter since commit_delay is 0?
data[235] = '#checkpoint_timeout = 5min		# range 30s-1d\n'
#Let us just care about the read only database, so we don't care about clones
#For the alternative scenario, you'd want to keep this on at a loss of performance
#Never turn off unless your data is entirely disposable. Setting fsync=off is the equivalent of saying "I do not care about my data, I can recreate the database from scratch if I have to."
data[228] = '#wal_skip_threshold = 2MB\n' #I think changing this won't do anything since we set fsync to off



#!! change does not require restart
max_num_checkpoint_completion_target = 1
checkpoint_completion_target_refineparam = 0.1
checkpoint_completion_target_list = [x*checkpoint_completion_target_refineparam for x in range(int(max((max_num_checkpoint_completion_target)/(checkpoint_completion_target_refineparam)+1,1)))]
#Deals with I/O processing https://postgresqlco.nf/doc/en/param/checkpoint_completion_target/
data[236] = '#checkpoint_completion_target = 0.9	# checkpoint target duration, 0.0 - 1.0\n'

#!! change does not require restart
max_num_checkpoint_flush_after = 256
checkpoint_flush_after_refineparam = 1
checkpoint_flush_after_list = [x*checkpoint_flush_after_refineparam for x in range(int(max((max_num_checkpoint_flush_after)/(checkpoint_flush_after_refineparam)+1,1)))]
#Number of pages after which previously performed writes are flushed to disk
data[237] = '#checkpoint_flush_after = 0		# measured in pages, 0 disables\n'


#!! change does not require restart
data[238] = '#checkpoint_warning = 0		# 0 disables\n'

#!! change does not require restart
data[239] = 'max_wal_size = 2\n' #MB
data[240] = 'min_wal_size = 2\n' #MB
#I'm setting this to small as possible values to preserve as much memory as possible
#If some errors happen, it's probably from here.

##################### Some Archiving and Recovery Parameters we might potentially care about ##################### 

#!! change requires restart
data[297] = '#max_wal_senders = 0		# max number of walsender processes\n'
#We might need to set this to one if we're going to use another server for updates/ keeping data safe and updated

#!! change requires restart
data[299] = '#max_replication_slots = 0	# max number of replication slots\n'
#We might need to set this to one if we're going to use another server for updates/ keeping data safe and updated

#!! change does not require restart
data[301] = '#wal_keep_size = 0		# in megabytes; 0 disables\n'
#We might need to set this to nonzero if we're going to use another server for updates/ keeping data safe and updated

#!! change does not require restart
data[302] = '#max_slot_wal_keep_size = -1	# in megabytes; -1 disables\n'
#We might need to set this to nonzero if we're going to use another server for updates/ keeping data safe and updated

##################### Query Specific Parameters ##################### 

data[360] = '#enable_async_append = on\n'
data[361] = '#enable_bitmapscan = on\n'
data[362] = '#enable_gathermerge = on\n'
data[363] = '#enable_hashagg = on\n'
data[364] = '#enable_hashjoin = on\n'
data[365] = '#enable_incremental_sort = on\n'
data[366] = '#enable_indexscan = on\n'
data[367] = '#enable_indexonlyscan = on\n'
data[368] = '#enable_material = on\n'
data[369] = '#enable_memoize = on\n'
data[370] = '#enable_mergejoin = on\n'
data[371] = '#enable_nestloop = on\n'
data[372] = '#enable_parallel_append = on\n'
data[373] = '#enable_parallel_hash = on\n'
data[374] = '#enable_partition_pruning = on\n'
data[375] = '#enable_partitionwise_join = off\n'
#Because partitionwise join planning can use significantly more CPU time and memory during planning, the default is off
data[376] = '#enable_partitionwise_aggregate = off\n'
#Because partitionwise grouping or aggregation can use significantly more CPU time and memory during planning, the default is off
data[377] = '#enable_seqscan = on\n'
data[378] = '#enable_sort = on\n'
data[379] = '#enable_tidscan = on\n'


#!! change does not require restart
data[383] = '#seq_page_cost = 1.0			# measured on an arbitrary scale\n'
#The main reason to modify seq_page_cost is to try to get planner costs 
#to more-or-less indicate execution times in milleseconds. 
#All other costs change relative to this cost automatically.
#I don't think we care about this

#!! change does not require restart
data[384] = '#random_page_cost = 4.0			# same scale as above\n'
#Sets the ratio of seek to scan time for your database storage. 
#Should not be altered unless you're using special storage (SSDs, high end SANs, etc.) 
#where seek/scan ratios are actually different. If you need the database to favor indexes more, 
#tune effective_cache_size and some of the cpu_* costs instead.

#!! change does not require restart
data[385] = '#cpu_tuple_cost = 0.01			# same scale as above\n'
#Sets the planner's estimate of the cost of processing each row during a query. 
#The default is 0.01.

#!! change does not require restart
max_num_cpu_index_tuple_cost = 0.010
cpu_index_tuple_cost_refineparam = 0.001
cpu_index_tuple_cost_list = [x*cpu_index_tuple_cost_refineparam for x in range(int(max((max_num_cpu_index_tuple_cost)/(cpu_index_tuple_cost_refineparam)+1,1)))]
#Decrease this slightly to make your database favor indexes slightly more.
data[386] = '#cpu_index_tuple_cost = 0.005		# same scale as above\n'


#!! change does not require restart
max_num_cpu_operator_cost = 0.0035
cpu_operator_cost_refineparam = 0.0001
cpu_operator_cost_list = [0.0015+x*cpu_operator_cost_refineparam for x in range(int(max((max_num_cpu_operator_cost-0.0015)/(cpu_operator_cost_refineparam)+1,1)))]
#Decrease this slightly to make your database favor indexes slightly more.
data[387] = '#cpu_operator_cost = 0.0025		# same scale as above\n'



data[388] = '#parallel_setup_cost = 1000.0	# same scale as above\n'
data[389] = '#parallel_tuple_cost = 0.1		# same scale as above\n'




#!! change does not require restart
min_parallel_table_scan_size_memory_cap = int(allotted_ram_mem*0.1) #this is in MB
min_parallel_table_scan_size_refineparam = 8
min_parallel_table_scan_size_list = [x*min_parallel_table_scan_size_refineparam for x in range(int(max((min_parallel_table_scan_size_memory_cap)/(min_parallel_table_scan_size_refineparam)+1,1)))]
#Sets the minimum amount of table data that must be scanned in order for a parallel scan to be considered. 
#For a parallel sequential scan, the amount of table data scanned 
#is always equal to the size of the table, 
#but when indexes are used the amount of table data scanned will normally be less.
data[390] = '#min_parallel_table_scan_size = 8MB\n'


#!! change does not require restart
min_parallel_index_scan_size_memory_cap = int(allotted_ram_mem*0.05) #this is in MB
min_parallel_index_scan_size_refineparam = 4
min_parallel_index_scan_size_list = [x*min_parallel_index_scan_size_refineparam for x in range(int(max((min_parallel_index_scan_size_memory_cap)/(min_parallel_index_scan_size_refineparam)+1,1)))]
#Sets the minimum amount of index data that must be scanned in order for a parallel scan to be considered. 
#Note that a parallel index scan typically won't touch the entire index; 
#it is the number of pages which the planner believes 
#will actually be touched by the scan which is relevant. 
#This parameter is also used to decide whether a particular index 
#can participate in a parallel vacuum.
data[391] = '#min_parallel_index_scan_size = 512kB\n'


#!! change does not require restart
effective_cache_size_memory_cap = int(allotted_ram_mem*0.7)#this is in MB
effective_cache_size_refineparam = 64
effective_cache_size_list = [1+x*effective_cache_size_refineparam for x in range(int(max((effective_cache_size_memory_cap-1)/(effective_cache_size_refineparam)+1,1)))]
#Sets the planner's assumption about the total size of the data caches
#This is factored into estimates of the cost of using an index; 
#a higher value makes it more likely index scans will be used, 
#a lower value makes it more likely sequential scans will be used
#This setting just helps the planner make good cost estimates; 
#it does not actually allocate the memory.
data[392] = '#effective_cache_size = 4096MB\n'

#!! change does not require restart
max_num_jit_above_cost = 200000
jit_above_cost_refineparam = 10000
jit_above_cost_list = [x*jit_above_cost_refineparam for x in range(int(max((max_num_jit_above_cost)/(jit_above_cost_refineparam)+1,1)))]
#Sets the query cost above which JIT compilation is activated, 
#if enabled (see jit). Performing JIT costs planning time but can accelerate query execution.
data[394] = '#jit_above_cost = 100000		# perform JIT compilation if available\n'


#!! change does not require restart
max_num_jit_inline_above_cost = 1000000
jit_inline_above_cost_refineparam = 100000
jit_inline_above_cost_list = [x*jit_inline_above_cost_refineparam for x in range(int(max((max_num_jit_inline_above_cost)/(jit_inline_above_cost_refineparam)+1,1)))]
#Sets the query cost above which JIT compilation attempts to inline functions and operators. 
#Inlining adds planning time, but can improve execution speed. 
#It is not meaningful to set this to less than jit_above_cost (CONSTRAINT)
data[397] = '#jit_inline_above_cost = 500000		# inline small functions if query is\n'

#!! change does not require restart
max_num_jit_optimize_above_cost = 1000000
jit_optimize_above_cost_refineparam = 100001
jit_optimize_above_cost_list = [-1+x*jit_optimize_above_cost_refineparam for x in range(int(max((max_num_jit_optimize_above_cost)/(jit_optimize_above_cost_refineparam)+1,1)))]
#Sets the query cost above which JIT compilation applies expensive optimizations. 
#Such optimization adds planning time, but can improve execution speed.
#It is not meaningful to set this to less than jit_above_cost (CONSTRAINT)
#it is unlikely to be beneficial to set it to more than jit_inline_above_cost (CONSTRAINT)
data[399] = '#jit_optimize_above_cost = 500000	# use expensive JIT optimizations if\n'


data[405] = '#geqo = on\n'

#!! change does not require restart

#!!!!START HERE!!!#

#With new, faster processors it's tempting to raise the geqo_threshold a little, 
#such as to 16 or 18. Increasing more than that is unwise as query planning time 
#goes up geometrically.
max_num_geqo_threshold = 20
geqo_threshold_refineparam = 1
geqo_threshold_list = [x*geqo_threshold_refineparam for x in range (int(max((max_num_geqo_threshold)/(geqo_threshold_refineparam)+1,1)))]
data[406] = '#geqo_threshold = 12\n'
#sets threshold of FROMs in queries beyond which GEQO is used
max_num_geqo_effort = 10
geqo_effort_list = range(11)
data[407] = '#geqo_effort = 5			# range 1-10\n'
#controls effort between query planning time and quality, with larger numbers focussing more on quaity 
max_num_geqo_pool_size = 1000
geqo_pool_size_refineparam = 10
geqo_pool_size_list = [2 + x*geqo_pool_size_refineparam for x in range(int(max((max_num_geqo_pool_size)/(geqo_pool_size_refineparam)+1,1)))]
data[408] = '#geqo_pool_size = 0			# selects default based on effort\n'
#decides number of individuals for gene pool of geco's genetic algorithm
max_num_geqo_generations = 2000
geqo_generations_refineparam = 10
geqo_generations_list = [1 + x*geqo_generations_refineparam for x in range(int(max((max_num_geqo_generations)/(geqo_generations_refineparam)+1,1 )))]
data[409] = '#geqo_generations = 0			# selects default based on effort\n'
#number of iterations for the genetic algorithm
max_num_geqo_selection_bias = 2.0
geqo_selection_bias_refineparam = 0.01
geqo_selection_bias_list = [1.5 + x*geqo_selection_bias_refineparam for x in range(int(max((max_num_geqo_selection_bias)/(geqo_selection_bias_refineparam)+1,1 ))) ]
data[410] = '#geqo_selection_bias = 2.0		# range 1.5-2.0\n'
#controls selective pressure of GA
max_num_geqo_seed = 1.0
geqo_seed_refineparam = 0.01
geqo_seed_list = [x*geqo_seed_refineparam for x in range(int(max((max_num_geqo_seed)/(geqo_seed_refineparam)+1,1)))]
data[411] = '#geqo_seed = 0.0			# range 0.0-1.0\n'
#controls rng for random paths in join-order search space
max_num_default_statistics_target = 1000
default_statistics_target_refineparam = 10
default_statistics_target_list = [1 + x*default_statistics_target_refineparam for x in range(int(max((max_num_default_statistics_target)/(default_statistics_target_refineparam)+1,1)))]
data[415] = '#default_statistics_target = 100	# range 1-10000\n'
#For very small/simple databases, decrease to 10 or 50. 
#Data warehousing applications generally need to use 500 to 1000.
#Otherwise, increase statistics targets on a per-column basis.
#Larger values increase time required but also planner's quality in analysing tables
constraint_exclusion_list = ['partition','on','off']
data[416] = '#constraint_exclusion = partition	# on, off, or partition\n'
#Controls the query planner's use of table constraints to optimize queries.
#on- examines all constraints
#off - none
#partitions - only for inheritance tables and UNION ALL queries
max_num_cursor_tuple_fraction = 1.0
cursor_tuple_fraction_refineparam = 0.1
cursor_tuple_fraction_list = [x*cursor_tuple_fraction_refineparam for x in range(int(max((max_num_cursor_tuple_fraction)/(cursor_tuple_fraction_refineparam)+1,1)))]
data[417] = '#cursor_tuple_fraction = 0.1		# range 0.0-1.0\n'
#gives estimate of fraction of cursor's rows that will be recieved
#smaller values give the first few rows quickly and struggle with the rest
#larger values maintain consistency
max_num_from_collapse_limit = 1400
from_collapse_limit_refineparam = 7
from_collapse_limit_list = [1 + x*from_collapse_limit_refineparam for x in range(int(max_num_from_collapse_limit/from_collapse_limit_refineparam))]
data[418] = '#from_collapse_limit = 8\n'
#setting to value above geqo threshold triggers its use
#FROM queries are not collapsed beyond this limit i.e. sub-queries arent
#grouped to form upper queries

data[419] = '#jit = on				# allow JIT compilation\n'
#is always on, no reason to turn it off
max_num_join_collapse_limit = 1400
join_collapse_limit_refineparam = 7
join_collapse_limit_list = [1 + x*join_collapse_limit_refineparam for x in range(int(max_num_join_collapse_limit/join_collapse_limit_refineparam))]
data[420] = '#join_collapse_limit = 8		# 1 disables collapsing of explicit\n'
#similar to from_collapse_limit, except the JOIN queries are flattened into FROM lists 
#beyond this threshold 
plan_cache_mode_list = ['auto','force_generic_plan','force_custom_plan']
data[422] = '#plan_cache_mode = auto			# auto, force_generic_plan or\n'
#
##################### Autovacuum (some parameters) ##################### 
data[619] = '#autovacuum = on			# Enable autovacuum subprocess?  \'on\'\n'
#track_counts must be enabled for auto_vaccum to work
num_max_autovacuum_max_workers = 20
autovacuum_max_workers_refineparam = 1
autovacuum_max_workers_list = [1 + x*autovacuum_max_workers_refineparam for x in range(int(num_max_autovacuum_max_workers/autovacuum_max_workers_refineparam ))] 
data[621] = '#autovacuum_max_workers = 3		# max number of autovacuum subprocesses\n'
#max number of autovacuum processes that can occur at once

#Don't know if I want to deal with time related stuff yet
data[623] = '#autovacuum_naptime = 1min		# time between autovacuum runs\n'
#minimum delay between 2 consecutive autovacuum runs

max_num_autovacuum_vacuum_threshold = 1000
autovacuum_vacuum_threshold_refineparam = 10
autovacuum_vacuum_threshold_list = [x*autovacuum_vacuum_threshold_refineparam for x in range(int(max_num_autovacuum_vacuum_threshold/autovacuum_vacuum_threshold_refineparam))]
data[624] = '#autovacuum_vacuum_threshold = 50	# min number of row updates before\n'
#Minimum number of tuple updates or deletes prior to vacuum
max_num_autovacuum_vacuum_insert_threshold = 4000
autovacuum_vacuum_insert_threshold_refineparam = 200
autovacuum_vacuum_insert_threshold_list = [-1 + x*autovacuum_vacuum_insert_threshold_refineparam for x in range(int(max_num_autovacuum_vacuum_insert_threshold/autovacuum_vacuum_insert_threshold_refineparam)+1)]
data[626] = '#autovacuum_vacuum_insert_threshold = 1000	# min number of row inserts\n'
#Specifies the number of inserted tuples needed to trigger a VACUUM in any one table. The default is 1000 tuples.
#If -1 is specified, autovacuum will not trigger a VACUUM operation on any tables based on the number of inserts.
max_num_autovacuum_analyze_threshold = 1000
autovacuum_analyze_threshold_refineparam = 10
autovacuum_analyze_threshold_list = [x*autovacuum_analyze_threshold_refineparam for x in range(int(max_num_autovacuum_analyze_threshold/autovacuum_analyze_threshold_refineparam))]
data[629] = '#autovacuum_analyze_threshold = 50	# min number of row updates before\n'
#Specifies the minimum number of inserted, updated or deleted tuples needed to trigger an ANALYZE in any one table
max_num_autovacuum_vacuum_scale_factor = 10.0
autovacuum_vacuum_scale_factor_refineparam = 0.1
autovacuum_vacuum_scale_factor_list = [x*autovacuum_vacuum_scale_factor_refineparam for x in range(int(max_num_autovacuum_vacuum_scale_factor/autovacuum_vacuum_scale_factor_refineparam))]
data[631] = '#autovacuum_vacuum_scale_factor = 0.2	# fraction of table size before vacuum\n'
#Specifies a fraction of the table size to add to autovacuum_vacuum_threshold when deciding whether to trigger a VACUUM.
max_num_autovacuum_vacuum_insert_scale_factor = 10.0
autovacuum_vacuum_insert_scale_factor_refineparam = 0.1
autovacuum_vacuum_insert_scale_factor_list = [x*autovacuum_vacuum_insert_scale_factor_refineparam for x in range(int(max_num_autovacuum_vacuum_insert_scale_factor/autovacuum_vacuum_insert_scale_factor_refineparam))]

data[632] = '#autovacuum_vacuum_insert_scale_factor = 0.2	# fraction of inserts over table\n'

max_num_autovacuum_analyze_scale_factor = 10.0
autovacuum_analyze_scale_factor_refineparam = 0.1
autovacuum_analyze_scale_factor_list = [x*autovacuum_analyze_scale_factor_refineparam for x in range(int(max_num_autovacuum_analyze_scale_factor/autovacuum_analyze_scale_factor_refineparam))]
data[634] = '#autovacuum_analyze_scale_factor = 0.1	# fraction of table size before analyze\n'

max_num_autovacuum_freeze_max_age = 2000000000
autovacuum_freeze_max_age_refineparam = 100000000
autovacuum_freeze_max_age_list = [100000+x*autovacuum_freeze_max_age_refineparam for x in range(int(max_num_autovacuum_freeze_max_age/autovacuum_freeze_max_age_refineparam))]
data[635] = '#autovacuum_freeze_max_age = 200000000	# maximum XID age before forced vacuum\n'

max_num_autovacuum_multixact_freeze_max_age = 2000000000
autovacuum_multixact_freeze_max_age_refineparam = 100000000
autovacuum_multixact_freeze_max_age_list = [10000+x*autovacuum_multixact_freeze_max_age_refineparam for x in range(int(max_num_autovacuum_multixact_freeze_max_age/autovacuum_multixact_freeze_max_age_refineparam))]

data[637] = '#autovacuum_multixact_freeze_max_age = 400000000	# maximum multixact age\n'

#Don't know if I want to deal with time related stuff yet
autovacuum_vacuum_cost_delay_list = [-1+x for x in range(102)]
data[640] = '#autovacuum_vacuum_cost_delay = 2ms	# default vacuum cost delay for\n'


autovacuum_vacuum_cost_limit_list = [-1+x*100 for x in range(100)]
data[643] = '#autovacuum_vacuum_cost_limit = -1	# default vacuum cost limit for\n'

##################### Lock Management (some parameters) ##################### 

#In a database, a deadlock is an unwanted situation in 
#which two or more transactions are waiting indefinitely for one another to give up locks
max_num_deadlock_timeout = 1000
deadlock_timeout_list = [1,10,100,200,500,1000]
data[735] = '#deadlock_timeout = 1s\n'
#max time the system will wait for a deadlock

max_num_max_locks_per_transaction = 1024
max_locks_per_transaction_refineparam = 16
max_locks_per_transaction_list = [10 + x*max_locks_per_transaction_refineparam for x in range(int(max_num_max_locks_per_transaction/max_locks_per_transaction_refineparam))]
data[736] = '#max_locks_per_transaction = 64		# min 10\n'


max_num_max_pred_locks_per_transaction = 1024
max_pred_locks_per_transaction_refineparam = 16
max_pred_locks_per_transaction_list = [10 + x*max_pred_locks_per_transaction_refineparam for x in range(int(max_num_max_pred_locks_per_transaction/max_pred_locks_per_transaction_refineparam))]
data[738] = '#max_pred_locks_per_transaction = 64	# min 10\n'

max_num_max_pred_locks_per_relation = 64
max_pred_locks_per_relation_refineparam = 1
max_pred_locks_per_relation_list = [-64 + x*max_pred_locks_per_relation_refineparam for x in range(int(2*max_num_max_pred_locks_per_relation/max_pred_locks_per_relation_refineparam))]
data[740] = '#max_pred_locks_per_relation = -2	# negative values mean\n'

max_num_max_pred_locks_per_page = 100
max_pred_locks_per_page_refineparam = 1
max_pred_locks_per_page_list = [x*max_pred_locks_per_page_refineparam for x in range(int(max_num_max_pred_locks_per_page/max_pred_locks_per_page_refineparam))]
data[743] = '#max_pred_locks_per_page = 2            # min 0\n'


#configslist = itertools.product(shared_buffers_list, temp_buffers_list, , max_pred_locks_per_relation_list, max_pred_locks_per_page_list)
#for congifuration in configslist:
#	print(configuration)

# and write everything back
with open('test.txt', 'w') as file:
    file.writelines( data )