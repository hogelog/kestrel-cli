'''
Created on 2012/04/09

@author: hogelog
'''
import sys
import kestrel
import argparse


class CommandParser:
    def __init__(self, argv):
        progname = argv.pop(0)
        command_parser = self.parser_command(progname)
        self.args = command_parser.parse_args(argv)

    def parser_command(self, progname):
        parser = argparse.ArgumentParser(
            prog=progname,
            description="Kestrel CommandLine Interface",
            add_help=False)
        self.add_argument_help(parser)
        self.add_sub_parsers(parser)
        return parser

    def add_sub_parsers(self, parser):
        subparsers = parser.add_subparsers(
           description="kestrel commands", dest="command")

        self.add_subcommand_parser(
            subparsers, "get", "get and remove an item from a queue")
        self.add_subcommand_parser(
            subparsers, "peek", "get an item from a queue")

        add_parser = self.add_subcommand_parser(
            subparsers, "set", "add an item to a queue")
        self.add_arguments_set(add_parser)

        self.add_subcommand_parser(subparsers, "delete", "drop a queue")

    def add_argument_help(self, parser):
        parser.add_argument(
            "--help",
            help="show this help message and exit",
            action="help")

    def add_subcommand_parser(self, subparsers, cmdname, cmdhelp):
        subparser = subparsers.add_parser(
            cmdname, help=cmdhelp, add_help=False)
        self.add_argument_help(subparser)
        self.add_arguments_hostport(subparser)
        subparser.add_argument(
            "queue",
            metavar="<queue-name>",
            help="target queue")
        return subparser

    def add_arguments_hostport(self, parser):
        parser.add_argument(
            "-h",
            metavar="<hostname>",
            default="127.0.0.1",
            dest="hostname",
            help="server hostname (default: 127.0.0.1)")
        parser.add_argument(
            "-p",
            default=22133,
            metavar="<port>",
            type=int,
            dest="port",
            help="server port (default: 22133)")

    def add_arguments_set(self, parser):
        parser.add_argument(
            "expiration",
            type=int,
            default=0,
            nargs="?",
            metavar="<expiration>",
            help="expiration time (default 0)")


class CommandLine:
    @staticmethod
    def execute(args):
        cli = CommandLine(args)
        cmdname = args.command
        if hasattr(cli, cmdname):
            getattr(cli, cmdname)()
        else:
            print("Invalid Command: %s" % cmdname)

    def __init__(self, args):
        self.args = args
        servers = ["%s:%s" % (args.hostname, args.port)]
        self.client = kestrel.Client(servers, args.queue)

    def get(self):
        print(self.client.get())

    def peek(self):
        print(self.client.peek())

    def set(self): #@ReservedAssignment @IgnorePep8
        data = sys.stdin.read()
        self.client.add(data)

if __name__ == '__main__':
    parser = CommandParser(sys.argv)
    CommandLine.execute(parser.args)
