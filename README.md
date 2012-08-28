# Kestrel CommandLine Interface

## Install
    # pip install kestrel-cli

## Usage
    $ kestrel-cli --help
    usage: kestrelcli/cli.py [--help] {get,peek,set,delete,stats,list,shell} ...
    
    Kestrel CommandLine Interface
    
    optional arguments:
      --help                show this help message
    
    subcommands:
      kestrel commands
    
      {get,peek,set,delete,stats,list,shell}
        get                 get and remove an item from a queue
        peek                get an item from a queue
        set                 add an item to a queue
        delete              drop a queue
        stats               queue status
        list                queue list
        shell               interactive shell

### Get
    $ kestrel-cli get --help
    usage: /usr/local/bin/kestrel-cli get [--help] [-h <hostname>] [-p <port>]
                                          [-f <file>]
                                          <queue-name>
    
    positional arguments:
      <queue-name>   target queue
    
    optional arguments:
      --help         show this help message and exit
      -h <hostname>  server hostname (default: 127.0.0.1)
      -p <port>      server port (default: 22133)
      -f <file>      output data file (default: STDOUT)

### Set
    $ kestrel-cli set --help
    usage: /usr/local/bin/kestrel-cli set [--help] [-h <hostname>] [-p <port>]
                                          [-f <file> | -d <data>]
                                          <queue-name> [<expiration>]
    
    positional arguments:
      <queue-name>   target queue
      <expiration>   expiration time (default: 0)
    
    optional arguments:
      --help         show this help message and exit
      -h <hostname>  server hostname (default: 127.0.0.1)
      -p <port>      server port (default: 22133)
      -f <file>      input data file (default: STDIN)
      -d <data>      input string data

## Example
    $ kestrel-cli set foobar -d hello
    $ kestrel-cli get foobar
    hello
    $ kestrel-cli get foobar
    None
    $ kestrel-cli set foobar -f hoge.json
    $ kestrel-cli get foobar
    {"hoge": "log"}
    $ kestrel-cli stats
    server: 127.0.0.1:22133
    {'queues': {'foobar': {'age': 0L,
                           'bytes': 0L,
                           'discarded': 0L,
                           'expired_items': 0L,
                           'items': 0L,
                           'logsize': 0L,
                           'mem_bytes': 0L,
                           'mem_items': 0L,
                           'open_transactions': 0L,
                           'total_items': 2L,
                           'waiters': 0L}},
     'server': {'bytes': 0L,
                'bytes_read': 143L,
                'bytes_written': 1734L,
                'cmd_get': 3L,
                'cmd_peek': 0L,
                'cmd_set': 2L,
                'curr_connections': 1L,
                'curr_items': 0L,
                'get_hits': 2L,
                'get_misses': 1L,
                'time': 1346178187L,
                'total_connections': 8L,
                'total_items': 2L,
                'uptime': 102L,
                'version': '2.1.3'}}
    $ kestrel-cli list
    foobar
