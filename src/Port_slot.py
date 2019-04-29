class Port_slot:
    def __init__(self, parent, link, ext=True):
        self._parent=parent
        self._dir=None # for ext port
        if ext == True:
            self._ext_link=link
            self._int_link=None
        else:
            self._ext_link=None
            self._int_link=link

    @property
    def name(self):
        index=self._parent.get_slot_index(self)
        if index != None:
            return self._parent.name+"_{}".format(index)
        else:
            return self._parent.name

    @property
    def full_name(self):
        index=self._parent.get_slot_index(self)
        if index != None:
            return self._parent.full_name+"_{}".format(index)
        else:
            return self._parent.full_name

    @property
    def cfg(self):
        return self._ext_link.cfg

    @cfg.setter
    def cfg(self, x):
        self._ext_link.cfg=x
        if self._int_link == None:
            print("{}: this piece not implemented".format(__file__))
        else:
            self._int_link.cfg=x


################################################################################
# public
################################################################################

    def dump_ext_ports(self, indent):
        if self._ext_link != None:
            return self._ext_link.dump_ext_ports(indent+self.name, self._dir)
        else:
            return ""

    def dump_int_ports(self, indent):
        if self._int_link != None:
            return self._int_link.dump_ext_ports(indent+self.name, self._dir)
        else:
            return ""

    def dump_ext_port_connections(self, indent):
        return self._ext_link.dump_ext_port_connections(indent, self)

    def set_dir(self, portdir, propagate=True):
        if self._dir != None:
            if self._dir != portdir:
                raise Exception("this should never happen")
        else:
            self._dir=portdir
            if propagate:
                self._ext_link.set_dir_for_other_port_slot(portdir, self)

    def set_link_type(self, t):
        if self._ext_link == None:
            raise Exception("this should never hapenn....probably")
        self._ext_link.load_implementation(t)

        if self._int_link == None:
            print("{}: this piece not implemented".format(__file__))
        else:
            self._ext_link.load_implementation(t)

    # from a link
    def replace_link(self, old_link, new_link):
        if self._ext_link == old_link:
            self._ext_link=new_link
            return
        if self._int_link == old_link:
            self._int_link=new_link
            return
        raise Exception("this should never happen")

    def is_internal(self, link):
        return self._int_link == link

################################################################################
# private
################################################################################

################################################################################
# debug
################################################################################

    def report(self, indent=""):
        if self._ext_link != None:
            one=(
                indent+"ext port: "+self.name+"\n"
                +self._ext_link.report(indent+"  ")
            )
        else:
            one=""

        if self._int_link != None:
            two=(
                indent+"ext port: "+self.name+"\n"
                +self._int_link.report(indent+"  ")
            )
        else:
            two=""

        return one+two

################################################################################
# fix python
################################################################################

    @property
    def parent(self):
        raise Exception("forbiden")
        return self._parent.copy()

    @parent.setter
    def parent(self, x):
        raise Exception("forbiden")
        self._parent=x

    @property
    def link(self):
        raise Exception("forbiden")
        return self._ext_link

    @link.setter
    def link(self, x):
        raise Exception("forbiden")
        self._ext_link=link

    @name.setter
    def name(self, x):
        raise Exception("this should never happen")
