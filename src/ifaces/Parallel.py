from ..Link import Link


def create_inst(cfg):
    return Parallel(cfg)

class Parallel(Link):
    type="Parallel"
    def __init__(self, parent):
        self.__dict__.update(parent.__dict__)

################################################################################
# public
################################################################################

    def dump_ext_ports(self, prefix, dir):
        if dir == None:
            dir="<dir>"
        return (
            prefix+": {} std_logic;\n".format(dir)
        )

    def dump_ext_port_connections(self, indent, port):
        return super(Parallel, self).dump_ext_port_connections(indent, port)

    def _dump_signals(self, indent):
        return (
            indent+"signal "+self.name+"_nd: std_logic;\n"
        )

    def load_implementation(self, t):
        if t != "Parallel":
            raise Exception("this should never happen")
