from .Node_iface import Node_iface
from .Ip_node import Ip_node
from .Link import Link


class Structural_node(Node_iface):
    def __init__(self, name):
        super(Structural_node, self).__init__(name)
        self._nodes={}
        self._links=[]

################################################################################
# public
################################################################################

# from main
    def create_ip_node(self, prototype, name=None):
        if name == None:
            name = prototype
        self._nodes[name]=Ip_node(prototype, name)

    def connect(self, one, two, cfg=None, full_duplex=False):
        if isinstance(one, list):
            for i in one:
                self.connect(i, two, cfg, full_duplex)
        elif isinstance(one, str):
            if full_duplex == True:
                self.connect(one, two, cfg)
                self.connect(two, one, cfg)
            else:
                print("connecting {} {} {}".format(one, two, cfg))
                (node_one, port_one)=self._get_node_port(one)
                (node_two, port_two)=self._get_node_port(two)

                link=Link(cfg)
                self._links.append(link)

                self._connect_ext_port(node_one, port_one, link)
                self._connect_ext_port(node_two, port_two, link)
        else:
            raise Exception("this should never happen")

    def dump(self):
        return (
            "library ieee;\nuse ieee.std_logic_1164.all;\n\n"
            +self.dump_entity()
            +"\n"
            +self._dump_architecture()
        )

    def load_ifaces(self):
        for i in self._nodes:
            print("loading ifaces for node {}".format(self._nodes[i].name))
            print(self._nodes[i].report())
            self._nodes[i].load_ifaces()

################################################################################
# protected
################################################################################

    def _get_node_port(self, name):
        ar=name.split(".", 1)
        return (ar[0], ar[1])

    def _connect_ext_port(self, name, port, link):
        if name not in self._nodes:
            raise Exception("failed to find node ", name)
        self._nodes[name].connect_ext_port(port, link)

    def _dump_architecture(self):
        return (
            "architecture v1 of {} is\n".format(self._name)
            +"\n"
            +self._dump_components()
            +self._dump_signals()
            +"\n"
            +"begin\n"
            +"\n"
            +self._dump_instances()
            +"end v1;\n"
        )

    def _dump_components(self):
        ret=""
        for i in sorted(self._nodes):
            ret+=self._nodes[i].dump_component()+"\n"
        return ret

    def _dump_signals(self):
        ret=""
        for i in self._links:
            ret+=i.dump_signals("    ")
        return ret

    def _dump_instances(self):
        ret=""
        for i in sorted(self._nodes):
            ret+=self._nodes[i].dump_inst()+"\n"
        return ret
