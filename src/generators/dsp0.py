def update(node):
    node.set_port_cfg("cfg_in", generate_cfg_port_cfg(node))
    node.set_port_cfg("cfg_out", generate_cfg_port_cfg(node))
    to_apply={
        "input": "in",
        "output": "out",
        "cfg_in": "in",
        "cfg_out": "out"
    }
    for portname in to_apply:
        node.set_dir(portname, to_apply[portname])
        node.set_link_type(portname, "Fifo")

    return node

def generate_cfg_port_cfg(node):
    return node.get_port_cfg("input")

def dump(node):
    return [(
        "dsp0.vhd",
        "dsp0 stub"
    )]
