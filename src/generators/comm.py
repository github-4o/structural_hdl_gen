from ..Ip_node import Ip_node

def update(node):
    ports=node.ports

    return Comm_node(node)

class Comm_node(Ip_node):
    _number=0
    def __init__(self, node):
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
        self.set_dir("iRs", "in")
        self.set_dir("oRs", "out")
        self.set_link_type("iRs", "Parallel")
        self.set_link_type("oRs", "Parallel")

    def dump(self):
        ret=self._dump_me()
        ret+=self._dump_dependencies()
        return ret

################################################################################
# private
################################################################################

    def _dump_me(self):
        return [
            (
                self.name+".vhd",
                (
                    "library ieee;\nuse ieee.std_logic_1164.all;\n\n\n"
                    +self.dump_entity()+"\n"
                    +self._dump_architecture()
                )
            )
        ]

    def _dump_architecture(self):
        cfg={}
        cfg["out_num"]=self.get_out_port_num()
        cfg["in_num"]=self.get_in_port_num()
        return (
            "architecture v1 of {}".format(self.name)+" is\n"
            +"\n"
            +self._dump_components(cfg["out_num"], cfg["in_num"])
            +"begin\n"
            +"\n"
            +self._dump_instances()
            +"end v1;\n"
        )

    def _dump_dependencies(self):
        return [
            ("serdes.vhd", self._dump_serdes())
        ]

    def _dump_components(self, out_num, in_num):
        return (
            self._dump_uart_component()
            +self._dump_proto_component(out_num, in_num)
            +self._dump_serdes_component()
        )

    def _dump_instances(self):
        return (
            self._dump_uart_instance()
            +"\n"
            +self._dump_proto_instance()
            +"\n"
            +self._dump_serdes_instances()
        )

    def _dump_uart_component(self):
        return (
            "    component uart\n"
            +"        port (\n"
            +"            iRs: in std_logic;\n"
            +"            oRs: out std_logic;\n"
            +"\n"
            +"            oNd: out std_logic;\n"
            +"            oData: out std_logic_vector (7 downto 0);\n"
            +"            iNd: in std_logic;\n"
            +"            iData: in std_logic_vector (7 downto 0);\n"
            +"\n"
            +"            iClk: in std_logic;\n"
            +"            iReset: in std_logic\n"
            +"        );\n"
            +"    end component;\n"
            +"\n"
            +"    signal sRx_nd: std_logic;\n"
            +"    signal sRx_data: std_logic_vector (7 downto 0);\n"
            +"    signal sTx_nd: std_logic;\n"
            +"    signal sTx_data: std_logic_vector (7 downto 0);\n"
            +"\n"
        )

    def _dump_uart_instance(self):
        return (
            "    uart_inst: uart\n"
            +"        port map (\n"
            +"            iRs => iRs,\n"
            +"            oRs => oRs,\n"
            +"\n"
            +"            oNd => sRx_nd,\n"
            +"            oData => sRx_data,\n"
            +"            iNd => sTx_nd,\n"
            +"            iData => sTx_data\n"
            +"\n"
            +"            iClk => iClk,\n"
            +"            iReset => iReset\n"
            +"        );\n"
        )

    def _dump_proto_component(self, out_num, in_num):

        if out_num > 0:
            out_ports_section=(
                "            oNd"+self.slv(out_num, "out")
                +"            oData"+self.slv(out_num*8, "out")
            )
        else:
            out_ports_section=""

        if in_num > 0:
            in_ports_section=(
                "            iNd"+self.slv(in_num, "in")
                +"            iData"+self.slv(in_num*8, "in")
            )
        else:
            in_ports_section=""

        return (
            "    component proto\n"
            +"        port (\n"
            +"            oNd: out std_logic;\n"
            +"            oData: out std_logic_vector (7 downto 0);\n"
            +"            iNd: in std_logic;\n"
            +"            iData: in std_logic_vector (7 downto 0);\n"
            +"\n"
            +in_ports_section
            +out_ports_section
            +"\n"
            +"            iClk: in std_logic;\n"
            +"            iReset: in std_logic\n"
            +"        );\n"
            +"    end component;\n\n"
            +self.generate_proto_signals(out_num, in_num)
            +"\n"
        )

    def _dump_proto_instance(self):

        return (
            "    proto_inst: proto\n"
            +"        port map (\n"
            +"            oNd => sTx_nd,\n"
            +"            oData => sTx_data,\n"
            +"            iNd => sRx_nd,\n"
            +"            iData => sRx_data,\n"
            +"\n"
            +"            iNd => sIn_nd,\n"
            +"            iData => sIn_data,\n"
            +"            oNd => sOut_nd,\n"
            +"            oData => sOut_data,\n"
            +"\n"
            +"            iClk => iClk,\n"
            +"            iReset => iReset\n"
            +"        );\n"
        )

    def _dump_serdes_component(self):
        return (
            "    component serdes\n"
            +"        port (\n"
            +"            iNd: in std_logic;\n"
            +"            iData: in std_logic_vector;\n"
            +"            oNd: out std_logic;\n"
            +"            oData: out std_logic_vector;\n"
            +"\n"
            +"            iClk: in std_logic;\n"
            +"            iReset: in std_logic\n"
            +"        );\n"
            +"    end component;\n\n"
        )

    def _dump_serdes_instances(self):
        ret=""
        # dump "out" instances
        data_port=self._ports["data"]
        port_slots=data_port.port_slots
        # dump "in" instances
        index=0
        for i in range(0, len(port_slots)):
            if port_slots[i].dir=="in":
                ret+=(
                    "    serdes_in{}: serdes\n".format(index)
                    +"        port map (\n"
                    +"            iNd => sOut_nd ({}),\n".format(index)
                    +"            iData => sOut_data ({}),\n".format(index)
                    +"            oNd => data_{}_nd,\n".format(i)
                    +"            oData => data_{}_data,\n".format(i)
                    +"\n"
                    +"            iClk => iClk,\n"
                    +"            iReset => iReset\n"
                    +"        );\n"
                )
                index+=1

        index=0
        for i in range(0, len(port_slots)):
            if port_slots[i].dir=="in":
                ret+=(
                    "    serdes_out{}: serdes\n".format(index)
                    +"        port map (\n"
                    +"            iNd => data_{}_nd,\n".format(i)
                    +"            iData => data_{}_data\n".format(i)
                    +"            oNd => sIn_nd ({}),\n".format(index)
                    +"            oData => sIn_data ({}),\n".format(index)
                    +"\n"
                    +"            iClk => iClk,\n"
                    +"            iReset => iReset\n"
                    +"        );\n\n"
                )
                index+=1
        return ret

    def get_out_port_num(self):
        if "data" not in self._ports:
            return 0

        data_port=self._ports["data"]
        port_slots=data_port.port_slots
        ret=0
        for i in port_slots:
            if i.dir == "out":
                ret+=1
        return ret

    def get_in_port_num(self):
        if "data" not in self._ports:
            return 0

        data_port=self._ports["data"]
        port_slots=data_port.port_slots
        ret=0
        for i in port_slots:
            if i.dir == "in":
                ret+=1
        return ret

    def slv(self, width, dir):
        return ": {} std_logic_vector ({} downto 0);\n".format(dir, width-1)

    def generate_proto_signals(self, out_num, in_num):
        if out_num > 0:
            out_ports_section=(
                "    sOut_nd"+self.slv(out_num, "out")
                +"    sOut_data"+self.slv(out_num*8, "out")
            )
        else:
            out_ports_section=""

        if in_num > 0:
            in_ports_section=(
                "    sIn_nd"+self.slv(in_num, "in")
                +"    sIn_dData"+self.slv(in_num*8, "in")
            )
        else:
            in_ports_section=""
        return out_ports_section+in_ports_section

################################################################################
# serdes
################################################################################

    def _dump_serdes(self):
        return (
            "library ieee;\n"
            +"use ieee.std_logic_1164.all;\n"
            +"\n"
            +"\n"
            +"entity serdes is\n"
            +"    port (\n"
            +"        iNd: in std_logic;\n"
            +"        iData: in std_logic_vector;\n"
            +"        oNd: out std_logic;\n"
            +"        oData: out std_logic_vector;\n"
            +"\n"
            +"        iClk: in std_logic;\n"
            +"        iReset: in std_logic\n"
            +"    );\n"
            +"end entity;\n"
            +"\n"
            +"architecture v1 of serdes is\n"
            +"\n"
            +"    constant cIw: natural := iData'length;\n"
            +"    constant cOw: natural := oData'length;\n"
            +"\n"
            +"begin\n"
            +"\n"
            +"    simo: if cIw > cOw generate\n"
            +"        assert false\n"
            +"            report \"not implemented\"\n"
            +"            severity failure;\n"
            +"    end generate;\n"
            +"\n"
            +"    miso: if cIw < cOw generate\n"
            +"        assert false\n"
            +"            report \"not implemented\"\n"
            +"            severity failure;\n"
            +"    end generate;\n"
            +"\n"
            +"    bypass: if cIw = cOw generate\n"
            +"        oNd <= iNd;\n"
            +"        oData <= iData;\n"
            +"    end generate;\n"
            +"\n"
            +"end v1;\n"
        )



# library ieee;
# use ieee.std_logic_1164.all;


# entity proto is
#     port (
#         oNd: out std_logic;
#         oData: out std_logic_vector (7 downto 0);
#         iNd: in std_logic;
#         iData: in std_logic_vector (7 downto 0);

#         iProto_nd: in std_logic_vector (2 downto 0);
#         iProto_data: in std_logic_vector (23 downto 0);
#         oProto_nd: out std_logic_vector (2 downto 0);
#         oProto_data: out std_logic_vector (23 downto 0);

#         iClk: in std_logic;
#         iReset: in std_logic
#     );
# end entity;

# architecture v1 of proto is

#     type tMem is array (255 downto 0) of std_logic_vector (7 downto 0);

# begin

#     rx: block
#         signal sRd: std_logic;
#         signal sRd_data: std_logic_vector;
#         signal sCount: unsigned (8 downto 0);
#     begin

#         rx_mem: block
#             signal sWr_addr: unsigned (7 downto 0);
#             signal sRd_addr: unsigned (7 downto 0);
#             signal sMem: tMem;
#             signal sCheck: std_logic_vector (1 downto 0);
#         begin

#             process (iClk, iReset)
#             begin
#                 if iReset = '0' then
#                     sWr_addr <= (others => '0');
#                 else
#                     if iNd = '1' then
#                         sWr_addr <= sWr_addr +1;
#                         sMem (to_integer(sWr_addr)) <= iData;
#                     end if;
#                 end if;
#             end process;

#             process (iClk, iReset)
#             begin
#                 if iReset = '0' then
#                     sRd_addr <= (others => '0');
#                 else
#                     if sRd = '1' then
#                         sRd_addr <= sRd_addr +1;
#                         sRd_data <= sMem (to_integer(sRd_addr));
#                     end if;
#                 end if;
#             end process;

#             sCheck <= sRd & iNd;

#             process (iClk, iReset)
#             begin
#                 if iReset = '0' then
#                     sCount <= (others => '0');
#                 else
#                     case sCheck is
#                         when "01" =>
#                             if sCount = 256 then
#                                 assert false
#                                     report "overflow"
#                                     severity failure;
#                             sCount <= sCount+1;
#                         when "10" =>
#                             if sCount = 0 then
#                                 assert false
#                                     report "underflow"
#                                     severity failure;
#                             sCount <= sCount-1;
#                         when "11" =>
#                             sCount <= sCount;
#                         when others =>
#                             sCount <= sCount;
#                     end case;
#                 end if;
#             end process;

#         end block;

#     end block;

#     tx: block
#     begin
#     end block;

# end v1;
