from ..Link import Link


def create_inst(cfg):
    return Fifo(cfg)

class Fifo(Link):
    type="Fifo"
    def __init__(self, parent):
        self.__dict__.update(parent.__dict__)

################################################################################
# public
################################################################################

    def dump_ext_ports(self, prefix, dir):
        if dir == None:
            dir="<dir>"
        return (
            prefix+"_nd: {} std_logic;\n".format(dir)
            +prefix+"_data: {} std_logic_vector ({} downto 0);\n".format(
                dir,
                self.cfg["width"]-1
            )
        )

    def dump_ext_port_connections(self, indent, port):
        return (
            indent+"{}_nd => {}_nd,\n".format(port.name, self.name)
            +indent+"{}_data => {}_data,\n".format(port.name, self.name)
        )

    def _dump_signals(self, indent):
        return (
            indent+"signal "+self.name+"_nd: std_logic;\n"
            +indent+"signal "+self.name+"_data: std_logic_vector ({} downto 0);\n".format(
                self.cfg["width"]-1
            )
        )

    def load_implementation(self, t):
        if t != "Fifo":
            raise Exception("this should never happen")
