#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
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

        get_parser = self.add_subcommand_parser(
            subparsers, "get", "get and remove an item from a queue")
        self.add_arguments_get(get_parser)

        peek_parser = self.add_subcommand_parser(
            subparsers, "peek", "get an item from a queue")
        self.add_arguments_get(peek_parser)

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

    def add_arguments_get(self, parser):
        parser.add_argument(
            "-f",
            type=argparse.FileType("w"),
            default=sys.stdout,
            metavar="<file>",
            dest="outfile",
            help="output data file (default: STDOUT)")

    def add_arguments_set(self, parser):
        parser.add_argument(
            "expiration",
            type=int,
            default=0,
            nargs="?",
            metavar="<expiration>",
            help="expiration time (default: 0)")
        input_group = parser.add_mutually_exclusive_group()
        input_group.add_argument(
            "-f",
            type=argparse.FileType("r"),
            default=sys.stdin,
            metavar="<file>",
            dest="infile",
            help="input data file (default: STDIN)")
        input_group.add_argument(
            "-d",
            metavar="<data>",
            dest="data",
            help="input string data")


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
        self.client = kestrel.Client(servers)
        self.queue = args.queue

    def get(self):
        data = str(self.client.get(self.queue))
        self.args.outfile.write(data)

    def peek(self):
        data = str(self.client.peek(self.queue))
        self.args.outfile.write(data)

    def set(self): #@ReservedAssignment @IgnorePep8
        if self.args.data:
            data = self.args.data
        else:
            data = self.args.infile.read()
        self.client.add(self.queue, data)

    def delete(self):
        self.client.delete(self.queue)


def main(argv=sys.argv):
    parser = CommandParser(argv)
    CommandLine.execute(parser.args)

if __name__ == '__main__':
    main()
