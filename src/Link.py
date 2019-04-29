import os
from importlib import import_module


class Link:
    _number=0
    def __init__(self, cfg, parent):
        self._parent=parent
        self._port1=None
        self._port2=None
        self._cfg=cfg

        self._number=__class__._number
        self._name="s{}".format(__class__._number)
        __class__._number+=1

        print("creating link {} with cfg {}".format(self.name, self._cfg))

    @property
    def name(self):
        return self._name[:]

    @property
    def cfg(self):
        if self._cfg != None:
            return self._cfg.copy()
        else:
            return None

    @cfg.setter
    def cfg(self, x):
        print("setting cfg on link ", self.name)
        if self._cfg != None:
            raise Exception("link {} redifinition of link cfg detected".format(
                self.name))
        self._cfg=x

################################################################################
# public
################################################################################

    def connect(self, port):
        if self._port1 == None:
            self._port1=port
            return

        if self._port2 == None:
            self._port2=port
            return

        raise Exception("all ports are occupied")

    def dump_signals(self, indent):
        if self._port1.is_internal(self) or self._port2.is_internal(self):
            return ""
        else:
            return self._dump_signals(indent)

    # prefix = indent + name
    def dump_ext_ports(self, prefix, dir):
        return prefix+": ;\n"

    # prefix = indent + name
    def dump_ext_port_connections(self, indent, port):
        if self._port1.is_internal(self) or self._port2.is_internal(self):
            if port == self._port1:
                other_name=self._port2.name
            elif port == self._port2:
                other_name=self._port1.name
            else:
                raise Exception("this should never happen")

            return indent+"{} => {},\n".format(port.name, other_name)
        else:
            return indent+"{} => {},\n".format(port.name, self.name)

# from one of the port slots
    def set_dir_for_other_port_slot(self, portdir, ps):
        if ps == self._port1:
            if self._port2.is_internal(self):
                self._port2.set_dir(portdir, propagate=False)
            else:
                self._port2.set_dir(self._invert_dir(portdir), propagate=False)
        elif ps == self._port2:
            if self._port1.is_internal(self):
                self._port1.set_dir(portdir, propagate=False)
            else:
                self._port1.set_dir(self._invert_dir(portdir), propagate=False)
        else:
            raise Exception("this should never happen")

# generators-related magic
    # from block generators....initially
    def load_implementation(self, t):
        print("loading implementation {} for link {}".format(t, self._name))
        module=self._load_module(t)
        new_link=module.create_inst(self)
        self._parent.replace_link(self, new_link)
        self._port1.replace_link(self, new_link)
        self._port2.replace_link(self, new_link)

################################################################################
# private
################################################################################

    def _load_module(self, type):
        p=os.path.dirname(os.path.relpath(__file__))
        modulename=p+".ifaces."+type
        print("loading module {}".format(modulename))
        return import_module(modulename)

    def _dump_signals(self, indent):
        return indent+"signal {}: ;\n".format(self._name)

    def _invert_dir(self, portdir):
        if portdir == "in":
            return "out"
        elif portdir == "out":
            return "in"
        else:
            raise Exception("this should never happen")

################################################################################
# debug
################################################################################

    def report(self, indent=""):
        return (
            indent+"link: "+self.name+"\n"
            +indent+"  connects:\n"
            +indent+"    {} internal: {}".format(
                self._port1.full_name, self._port1.is_internal(self))+"\n"
            +indent+"    {} internal: {}".format(
                self._port2.full_name, self._port2.is_internal(self))+"\n"
        )

################################################################################
# fix python
################################################################################

    @name.setter
    def name(self, x):
        raise Exception("forbiden")
        self._name=x
