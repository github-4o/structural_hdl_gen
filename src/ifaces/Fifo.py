def create_inst(cfg):
    return Fifo(cfg)

class Fifo:
    type="Fifo"
    def __init__(self, parent):
        self._parent=parent

    @property
    def cfg(self):
        return self._parent.cfg

    @property
    def name(self):
        return self._parent.name


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

    def dump_ext_port_connections(self, prefix):
        return (
            prefix+"_nd => {}_nd,\n".format(self.name)
            +prefix+"_data => {}_data,\n".format(self.name)
        )

    def dump_signals(self, indent, prefix):
        return (
            indent+"signal "+prefix+"_nd: std_logic;\n"
            +indent+"signal "+prefix+"_data: std_logic_vector ({} downto 0);\n".format(
                self.cfg["width"]-1
            )
        )

################################################################################
# fix python
################################################################################

    @cfg.setter
    def cfg(self, x):
        raise Exception("forbiden")
