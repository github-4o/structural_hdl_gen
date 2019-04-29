import os
from importlib import import_module

from .Node_iface import Node_iface


class Ip_node(Node_iface):
    def __init__(self, parent, prototype, name=None):
        if name == None:
            n=prototype
        else:
            n=name
        super(Ip_node, self).__init__(n)
        self._parent=parent
        self._prototype=prototype
        self._module=None

    @property
    def prototype(self):
        return self._prototype

################################################################################
# public
################################################################################

    def load_ifaces(self):
        self._module=self._load_module()
        return self._module.update(self)

    def dump(self):
        print("nothing to dump for ip node", self.name)
        return []

################################################################################
# protected
################################################################################

    def _load_module(self):
        p=os.path.dirname(os.path.relpath(__file__))
        modulename=p+".generators."+self._prototype
        print("loading prototype for {} ({})".format(self._name, modulename))
        print("loading module {}".format(modulename))
        return import_module(modulename)

################################################################################
# fix python
################################################################################

    @prototype.setter
    def prototype(self, x):
        raise Exception("forbiden")
