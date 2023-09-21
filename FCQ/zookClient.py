from kazoo.client import KazooClient

def print_help():
    print("Available commands:")
    print("ls <path> - list children of a node")
    print("get <path> - get data for a node")
    print("set <path> <data> - set data for a node")
    print("create <path> <data> - create a node")
    print("delete <path> - delete a node")
    print("exit - exit the client")

def print_children(client, path):
    children = client.get_children(path)
    for child in children:
        print(child)

def get_data(client, path):
    data, stat = client.get(path)
    print(data.decode())

def set_data(client, path, data):
    client.set(path, data.encode())

def create_node(client, path, data):
    client.create(path, data.encode())

def delete_node(client, path):
    client.delete(path)

def main():
    print_help()
    # zk = KazooClient(hosts='10.3.6.11:2181')
    # zk = KazooClient(hosts='207.244.87.209:2181')
    zk = KazooClient(hosts='116.203.81.23:2181')
    zk.start()
    while True:
        cmd = input("> ")
        if cmd.startswith("ls"):
            path = cmd.split()[1]
            print_children(zk, path)
        elif cmd.startswith("get"):
            path = cmd.split()[1]
            get_data(zk, path)
        elif cmd.startswith("set"):
            path, data = cmd.split()[1:]
            set_data(zk, path, data)
        elif cmd.startswith("create"):
            path, data = cmd.split()[1:]
            create_node(zk, path, data)
        elif cmd.startswith("delete"):
            path = cmd.split()[1]
            delete_node(zk, path)
        elif cmd == "exit":
            zk.stop()
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
