from .Port_slot import Port_slot
from .Link import Link


# this class could be implemented as a dictionaty in Node_iface
class Port:
    def __init__(self, parent):
        self._parent=parent
        self._port_slots=[]

    @property
    def port_slots(self):
        return self._port_slots.copy()

    @property
    def name(self):
        return self._parent.get_port_name(self)

    @property
    def full_name(self):
        return self._parent.name+"."+self._parent.get_port_name(self)

################################################################################
# public
################################################################################

    def connect_int_port(self, link):
        slot=Port_slot(self, link, ext=False)
        self._port_slots.append(slot)
        link.connect(slot)

    def connect_ext_port(self, link):
        slot=Port_slot(self, link)
        self._port_slots.append(slot)
        link.connect(slot)

    def dump_ext_ports(self, indent):
        if len(self._port_slots) > 0:
            ret=""
            for i in self._port_slots:
                ret+=i.dump_ext_ports(indent)
            return ret
        else:
            raise Exception("this should never happen")

    def dump_int_ports(self, indent):
        if len(self._port_slots) > 0:
            ret=""
            for i in self._port_slots:
                ret+=i.dump_int_ports(indent)
            return ret
        else:
            raise Exception("this should never happen")

    def dump_ext_port_connections(self, indent="            "):
        if len(self._port_slots) > 0:
            ret=""
            for i in self._port_slots:
                ret+=i.dump_ext_port_connections(indent)
            return ret
        else:
            raise Exception("this should never happen")

    # from slots:
    def get_slot_index(self, slot):
        if len(self._port_slots) == 1:
            return None
        elif len(self._port_slots) > 1:
            # this explicitly fails if graph is broken
            index=self._port_slots.index(slot)
            try:
                self._port_slots.index(slot, index)
                raise Exception("same slot multiple times")
            except:
                pass
            return index
        else:
            raise Exception ("this should never happen")

# from generators...initially
    def set_dir(self, portdir, forall=False):
        if len(self._port_slots) == 1:
            self._port_slots[0].set_dir(portdir)
        elif len(self._port_slots) > 1:
            if forall == True:
                for i in self._port_slots:
                    i.set_dir(portdir)
            else:
                raise Exception("dunno what to do here")
        else:
            raise Exception("this should never happen")

    def set_link_type(self, t, forall=False):
        if len(self._port_slots) == 1:
            self._port_slots[0].set_link_type(t)
        elif len(self._port_slots) > 1:
            if forall == True:
                for i in self._port_slots:
                    i.set_link_type(t)
            else:
                raise Exception("dunno what to do here")
        else:
            raise Exception("this should never happen")

    def get_port_cfg(self):
        if len(self._port_slots) == 1:
            return self._port_slots[0].cfg
        elif len(self._port_slots) > 1:
            raise Exception("dunno what to do here")
        else:
            raise Exception("this should never happen")

    def set_port_cfg(self, cfg, forall=False):
        if len(self._port_slots) == 1:
            self._port_slots[0].cfg=cfg
        elif len(self._port_slots) > 1:
            if forall == True:
                for i in self._port_slots:
                    i.cfg=cfg
            else:
                raise Exception("dunno what to do here")
        else:
            raise Exception("this should never happen")

################################################################################
# debug
################################################################################

    def report(self, indent=""):
        slots_report=""
        for i in self._port_slots:
            slots_report+=i.report(indent+"  ")
        return (
            indent+"port set: "+self.name+"\n"
            +slots_report
        )

################################################################################
# fix python
################################################################################

    @name.setter
    def name(self, x):
        raise Exception("forbiden")
        self._name=x

    @property
    def parent(self):
        raise Exception("forbiden")
        return self._parent.copy()

    @parent.setter
    def parent(self, x):
        raise Exception("forbiden")
        self._parent=x

    @port_slots.setter
    def port_slots(self, x):
        raise Exception("forbiden")
        return self._port_slots.copy()

    @port_slots.setter
    def port_slots(self, x):
        raise Exception("forbiden")
        self._port_slots=x

    @port_slots.setter
    def port_slots(self):
        raise Exception("forbiden")
