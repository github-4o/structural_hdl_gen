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
        self._nodes[name]=Ip_node(self, prototype, name)

    def connect(self, one, two, cfg=None, full_duplex=False):
        if isinstance(one, list):
            for i in one:
                self.connect(i, two, cfg, full_duplex)
        elif isinstance(one, str):
            if full_duplex == True:
                raise Exception("to tested")
                self.connect(one, two, cfg)
                self.connect(two, one, cfg)
            else:
                print("connecting {} {} {}".format(one, two, cfg))
                (node_one, port_one)=self._get_node_port(one)
                (node_two, port_two)=self._get_node_port(two)

                link=Link(cfg, self)
                self._links.append(link)

                if node_one == self.name:
                    self._connect_int_port(port_one, link)
                else:
                    self._connect_ext_port(node_one, port_one, link)

                if node_two == self.name:
                    self._connect_int_port(port_two, link)
                else:
                    self._connect_ext_port(node_two, port_two, link)
        else:
            raise Exception("this should never happen")

    def dump(self):
        ret=[
            ("{}.vhd".format(self.name),
                (
                    "library ieee;\nuse ieee.std_logic_1164.all;\n\n"
                    +self.dump_entity()
                    +"\n"
                    +self._dump_architecture()
                )
            )
        ]
        for i in self._nodes:
            ret+=self._nodes[i].dump()
        return ret

    def load_ifaces(self):
        replace=[]
        for i in self._nodes:
            print("loading ifaces for node {}".format(self._nodes[i].name))
            replacement_node=self._nodes[i].load_ifaces()
            new_name=replacement_node.name
            if new_name != i:
                replace.append((i, (new_name, replacement_node)))

        for i in replace:
            new_name=i[1][0]
            replacement_node=i[1][1]
            print("relpacing {}:{}".format(i[0], i[1][0]))
            self._nodes.pop(i[0])
            self._nodes[new_name]=replacement_node
            self._nodes[new_name].post_register_hook()

    # from a link
    def replace_link(self, old_link, new_link):
        print ("searching for {} in \n{}".format(old_link, self._links))
        if old_link in self._links:
            index=self._links.index(old_link)
            try:
                self._links.index(old_link, inde )
                raise Exception("found a link multiple times on the link list")
            except:
                pass
            self._links.pop(index)
            self._links.append(new_link)
        else:
            raise Exception("this should never happen")

################################################################################
# protected
################################################################################

    def _get_node_port(self, name):
        ar=name.split(".", 1)
        return (ar[0], ar[1])

    def _connect_int_port(self, port, link):
        self.connect_int_port(port, link)

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
