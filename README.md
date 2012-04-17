# Kestrel CommandLine Interface

## Install
    > pip install kestrel-cli

## Usage
    $ kestrel-cli --help
    usage: /usr/local/bin/kestrel-cli [--help] {get,peek,set,delete} ...
    
    Kestrel CommandLine Interface
    
    optional arguments:
      --help                show this help message and exit
    
    subcommands:
      kestrel commands
    
      {get,peek,set,delete}
        get                 get and remove an item from a queue
        peek                get an item from a queue
        set                 add an item to a queue
        delete              drop a queue

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
