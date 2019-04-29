from .Port import Port


class Node_iface:
    def __init__(self, name, parent):
        self._name=name
        self._ports={}
        self._parent=parent

    @property
    def ports(self):
        return self._ports.copy()

    @property
    def name(self):
        return self._name[:]

################################################################################
# public
################################################################################

    def connect_int_port(self, name, link):
        if name not in self._ports:
            self._ports[name]=Port(self)
        else:
            print(self._report())
            raise Exception("break")
        self._ports[name].connect_int_port(link)

    def connect_ext_port(self, name, link):
        if name not in self._ports:
            self._ports[name]=Port(self)
        self._ports[name].connect_ext_port(link)

    def dump_entity(self):
        my_type=self.report_my_type()
        if len(self._ports) > 0:
            if my_type == "Structural_node":
                ports=self._dump_int_ports("        ")
            elif my_type == "Ip_node":
                ports=self._dump_ports("        ")
            else:
                raise Exception("this should never happen: {}".format(my_type))
            ports+="\n"
        else:
            ports=""

        return (
            "entity {} is\n".format(self._name)
            +"    port (\n"
            +ports
            +"        iClk: in std_logic;\n"
            +"        iReset: in std_logic\n"
            +"    );\n"
            +"end entity;\n"
        )

    def dump_component(self):
        return (
            "    component {} is\n".format(self._name)
            +"        port (\n"
            +self._dump_ports("            ")
            +"\n"
            +"            iClk: in std_logic;\n"
            +"            iReset: in std_logic\n"
            +"        );\n"
            +"    end component;\n"
        )

    def dump_inst(self):
        ret=(
            "    {}_inst: {}\n".format(self._name, self._name)
            +"        port map (\n"
        )
        for i in self._ports:
            ret+=self._ports[i].dump_ext_port_connections()
        ret+=(
            "\n"
            +"            iClk => iClk,\n"
            +"            iReset => iReset\n"
            +"        );\n"
        )
        return ret

# from ports
    def get_port_name(self, port):
        found=False
        for i in self._ports:
            if found:
                if self._ports[i] == port:
                    raise Exception("this should never happen")
            else:
                if self._ports[i] == port:
                    ret=i
        return ret[:]

# grom generators
    def set_dir(self, portname, portdir, forall=False):
        if portname not in self._ports:
            raise Exception("failed to find port")

        self._ports[portname].set_dir(portdir)

    def set_link_type(self, portname, t, forall=False):
        if portname not in self._ports:
            raise Exception("failed to find port")

        self._ports[portname].set_link_type(t)

    def get_port_cfg(self, portname):
        if portname not in self._ports:
            raise Exception("failed to find port")

        return self._ports[portname].get_port_cfg()

    def set_port_cfg(self, portname, cfg, forall=False):
        if portname not in self._ports:
            raise Exception("failed to find port")

        self._ports[portname].set_port_cfg(cfg, forall=True)

################################################################################
# protected
################################################################################

    def _dump_ports(self, indent="        "):
        ret=""
        for i in self._ports:
            ret+=self._ports[i].dump_ext_ports(indent)
        return ret

    def _dump_int_ports(self, indent="        "):
        ret=""
        for i in self._ports:
            ret+=self._ports[i].dump_int_ports(indent)
        return ret

################################################################################
# debug
################################################################################

    def report(self, indent=""):
        return self._report()

    def _report(self, indent=""):
        ports_report=""
        for i in self._ports:
            ports_report+=self._ports[i].report(indent+"  ")+"\n\n"
        return (
            indent+"name: "+self.name+"\n"
            +ports_report
        )

################################################################################
# fix python
################################################################################

    @name.setter
    def name(self, x):
        raise Exception("forbiden")

    @ports.setter
    def ports(self):
        raise Exception("forbiden")
