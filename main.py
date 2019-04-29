from src.Structural_node import Structural_node


def dump_files(hdl):
    print(hdl)
    for i in hdl:
        print("writing file ", i[0])
        with open("output/"+i[0], "w") as f:
            f.write(i[1])

test=0

if test == 0:

    top_node=Structural_node("dsp_wrap")

    print("***creating nodes:")
    top_node.create_ip_node("comm")
    top_node.create_ip_node("dsp0")
    top_node.create_ip_node("dsp1")

    top_node.connect("comm.data", "dsp0.input", cfg={"width": 8})
    top_node.connect("dsp0.output", "dsp1.input", cfg={"width": 8})
    top_node.connect("dsp1.output", "comm.data", cfg={"width": 8})

    top_node.connect(["dsp0.cfg_out", "dsp1.cfg_out"], "comm.data")
    top_node.connect(["dsp0.cfg_in", "dsp1.cfg_in"], "comm.data")

    top_node.load_ifaces()

    hdl=top_node.dump()

elif test == 1:
    top_node=Structural_node("dsp_wrap")
    top_node.create_ip_node("comm")
    top_node.load_ifaces()
    hdl=top_node.dump()
else:
    raise Exception("unknown test")

dump_files(hdl)

print("done")
