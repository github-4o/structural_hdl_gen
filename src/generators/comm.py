def update(node):
    ports=node.ports

    data_port=ports["data"]
    data_port_slots=data_port.port_slots

    print(ports)
    print(len(data_port_slots))

def dump(node):
    return [(
        "comm.vhd",
        "comm stub"
    )]
