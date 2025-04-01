# File System Simulation
# This program simulates a simple in-memory file system with directories and files.
# Author : Smit Chokshi

class Item:
    def __init__(self, name, is_dir):
        self.name = name
        self.is_dir = is_dir
        self.parent = None
        self.first_child = None  
        self.next_sibling = None  

# Adds a child item to this directory
    def add_child(self, item):
        if not self.first_child:
            self.first_child = item
        else:
            node = self.first_child
            while node.next_sibling:
                node = node.next_sibling
            node.next_sibling = item
        item.parent = self

# Finds a child item by name
    def find_child(self, name):
        node = self.first_child
        while node:
            if node.name == name:
                return node
            node = node.next_sibling
        return None

# Lists the names of all children in this directory
    def list_children(self):
        names = []
        node = self.first_child
        while node:
            names.append(node.name)
            node = node.next_sibling
        return names


class FileSystem:
    def __init__(self):
        self.root = Item("/", True) # Create the root directory
        self.current = self.root

# Creates a new directory in the current directory
    def mkdir(self, name):
        if self.current.find_child(name):
            print(f"Can't make '{name}': already exists.")
            return
        self.current.add_child(Item(name, True))

# Creates a new file in the current directory
    def touch(self, name):
        if self.current.find_child(name):
            print(f"Can't create '{name}': already exists.")
            return
        self.current.add_child(Item(name, False))

# Lists the contents of the current directory
    def ls(self):
        items = self.current.list_children()
        if not items:
            print("(empty)")
        else:
            for name in items:
                print(name)

# Changes the current directory
    def cd(self, name):
        if name == "/":
            self.current = self.root
        elif name == "..":
            if self.current.parent:
                self.current = self.current.parent
        else:
            node = self.current.find_child(name)
            if node and node.is_dir:
                self.current = node
            else:
                print(f"No directory named '{name}' found.")

# Main program to interact with the file system
if __name__ == "__main__":
    fs = FileSystem()   # Initialize the file system
    print("Welcome to your tiny in-memory file system.")
    print("Commands: mkdir <name>, touch <name>, ls, cd <dir>, cd .., exit")

    while True:
        try:
            line = input(f"{fs.current.name}> ").strip()
            if not line:
                continue

            parts = line.split()
            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else None

            if cmd == "exit":
                print("Bye!")
                break
            elif cmd == "mkdir" and arg:    # Create a directory
                fs.mkdir(arg)
            elif cmd == "touch" and arg:    # Create a file
                fs.touch(arg)
            elif cmd == "ls":               # List contents of the current directory
                fs.ls()
            elif cmd == "cd" and arg:       # Change directory
                fs.cd(arg)
            else:   # Handle unrecognized commands
                print("Hmm, I don't recognize that command.")
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break