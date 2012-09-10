#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: hogelog
'''
import sys
import kestrel
import argparse
import shlex
import json
import pprint
import fnmatch


class CommandParser:
    class ArgumentParser(argparse.ArgumentParser):
        class ParseExit(Exception):
            pass

        def parse_args(self, args=None, namespace=None):
            try:
                args = argparse.ArgumentParser.parse_args(
                    self, args, namespace)
                self.parse_exit = False
                return args
            except self.ParseExit:
                self.parse_exit = True

        def exit(self, status=0, message=None):
            if message:
                self._print_message(message, sys.stderr)
            raise self.ParseExit

    def __init__(self, argv, hostname=None, port=None):
        self.hostname = hostname
        self.port = port
        progname = argv.pop(0)
        command_parser = self.parser_command(progname)
        self.args = command_parser.parse_args(argv)
        self.parse_exit = command_parser.parse_exit
        if not self.parse_exit:
            if hostname:
                self.args.hostname = hostname
            if port:
                self.args.port

    def parser_command(self, progname):
        parser = self.ArgumentParser(
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

        set_parser = self.add_subcommand_parser(
            subparsers, "set", "add an item to a queue")
        self.add_arguments_set(set_parser)

        self.add_subcommand_parser(subparsers, "delete", "drop a queue")

        self.add_patterncommand_parser(subparsers,
                "delete_all", "delete all queues")

        self.add_patterncommand_parser(subparsers, "list", "queue list")

        self.add_subparser(subparsers, "stats", "queue status")

        self.add_subparser(subparsers, "shell", "interactive shell")

    def add_argument_help(self, parser):
        parser.add_argument(
            "--help",
            help="show this help message",
            action="help")

    def add_subparser(self, subparsers, cmdname, cmdhelp):
        subparser = subparsers.add_parser(
            cmdname, help=cmdhelp, add_help=False)
        self.add_argument_help(subparser)
        self.add_arguments_hostport(subparser)
        return subparser

    def add_patterncommand_parser(self, subparsers, cmdname, cmdhelp):
        subparser = self.add_subparser(subparsers, cmdname, cmdhelp)
        subparser.add_argument(
            "pattern",
            metavar="<pattern>",
            nargs="?",
            help="queue name pattern")
        return subparser

    def add_subcommand_parser(self, subparsers, cmdname, cmdhelp):
        subparser = self.add_subparser(subparsers, cmdname, cmdhelp)
        subparser.add_argument(
            "queue",
            metavar="<queue-name>",
            help="target queue")
        return subparser

    def add_arguments_hostport(self, parser):
        if self.hostname:
            parser.add_argument(
                action="store_const",
                dest="hostname",
                const=self.hostname)
        else:
            parser.add_argument(
                "-h",
                metavar="<hostname>",
                default="127.0.0.1",
                dest="hostname",
                help="server hostname (default: 127.0.0.1)")
        if self.port:
            parser.add_argument(
                action="store_const",
                dest="port",
                const=self.port)
        else:
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
    def execute(args, client_class=kestrel.Client):
        cli = CommandLine(args, client_class)
        cmdname = "cmd_" + args.command
        if hasattr(cli, cmdname):
            getattr(cli, cmdname)()
        else:
            print("Invalid Command: %s" % args.command)

    def __init__(self, args, client_class=kestrel.Client):
        self.args = args
        servers = ["%s:%s" % (args.hostname, args.port)]
        self.client = client_class(servers)

    def cmd_get(self):
        data = self.client.get(self.args.queue)
        if data:
            self.args.outfile.write(str(data))

    def cmd_peek(self):
        data = self.client.peek(self.args.queue)
        if data:
            self.args.outfile.write(str(data))

    def cmd_set(self):
        if self.args.data:
            data = self.args.data
        else:
            data = self.args.infile.read()
        self.client.add(self.args.queue, data)

    def cmd_delete(self):
        if self.client.delete(self.args.queue):
            print("deleted: %s" % self.args.queue)

    def cmd_delete_all(self):
        server, stats = self.client.stats()
        queues = self.filter(stats["queues"].keys(), self.args.pattern)
        for queue in queues:
            self.client.delete(queue)
            print("deleted: %s" % queue)

    def cmd_stats(self):
        server, stats = self.client.stats()
        print("server: %s" % server)
        pprint.pprint(stats)

    def cmd_list(self):
        server, stats = self.client.stats()
        queues = self.filter(stats["queues"].keys(), self.args.pattern)

        for queue in queues:
            print(queue)

    def filter(self, queues, pattern):
        if pattern:
            return fnmatch.filter(queues, pattern)
        else:
            return queues

    def cmd_shell(self):
        hostname = self.args.hostname
        port = self.args.port
        while True:
            try:
                import readline
            except ImportError:
                print("warning: cannot import 'readline'")
            try:
                cmdline = raw_input("> ")
                argv = [""] + shlex.split(cmdline)
                parser = CommandParser(argv, hostname, port)
                if not parser.parse_exit:
                    CommandLine.execute(parser.args)
            except EOFError:
                exit()


def main(argv=sys.argv, client_class=kestrel.Client):
    if len(argv) == 1:
        argv.append("--help")
    parser = CommandParser(argv)
    if not parser.parse_exit:
        CommandLine.execute(parser.args, client_class)

if __name__ == '__main__':
    main()
