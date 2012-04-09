'''
Created on 2012/04/09

@author: hogelog
'''
import sys
import kestrel
from test.test_iterlen import len


class CommandLine:
    def __init__(self, argv):
        self.exe = argv.pop(0)
        try:
            self.servers = [argv.pop(0)]
            self.queue = argv.pop(0)
            self.argv = argv
            self.client = kestrel.Client(self.servers, self.queue)
        except Exception:
            self.usage()

    def execute(self):
        command = self.argv.pop(0)
        if command == "help":
            self.help()
        elif command == "get":
            self.get()
        elif command == "peek":
            self.peek()
        elif command == "set":
            self.add()
        elif command == "quit":
            self.quit()

    def shell(self):
        while True:
            command = raw_input("> ")
            self.argv = command.split(" ")
            self.execute()

    def usage(self):
        print(self.exe + " hostname:port queue-name [get|peek|set filename]")
        sys.exit(0)

    def help(self):
        print("  get")
        print("  peek")
        print("  set filepath")

    def get(self):
        print(self.client.get())

    def peek(self):
        print(self.client.peek())

    def add(self):
        with open(self.argv.pop(0)) as datafile:
            data = datafile.read()
            if len(self.argv) == 0:
                self.client.add(data)
            else:
                self.client.add(data, int(self.argv.pop(0)))
            print("set " + self.queue + "\n" + data)

    def quit(self):
        sys.exit(0)

if __name__ == '__main__':
    cli = CommandLine(sys.argv)
    if len(sys.argv) == 0:
        cli.shell()
    else:
        cli.execute()
