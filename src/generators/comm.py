from ..Ip_node import Ip_node

def update(node):
    ports=node.ports

    return Comm_node(node)

class Comm_node(Ip_node):
    _number=0
    def __init__(self, node):
        print("!!!!! comm node {}".format(__class__._number))
        self.__dict__.update(node.__dict__)
        self._number=__class__._number
        self._name="comm_{}".format(__class__._number)
        __class__._number+=1

    def post_register_hook(self):
        self._parent.connect(
            "{}.iRs".format(self.name),
            "{}.iRs".format(self._parent.name)
        )
        self._parent.connect(
            "{}.oRs".format(self.name),
            "{}.oRs".format(self._parent.name)
        )

    def dump(self):
        return [
            (
                self.name+".vhd",
                (
                    "library ieee;\nuse ieee.std_logic_1164.all;\n\n\n"
                    +self.dump_entity()+"\n"
                    +self.dump_architecture()
                )
            )
        ]

    def dump_architecture(self):
        return (
            "architecture v1 of {}".format(self.name)+" is\n"
            +"begin\n"
            +"end v1;\n"
        )
