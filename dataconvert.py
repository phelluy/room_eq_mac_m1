#!/usr/bin/env python3
import re
import yaml
import sys

template_conf = "config_template.yml"

def convert(inputfile,outputfile=None,template=template_conf):
    if outputfile is None:
        outputfile = inputfile.replace(".txt",".yaml")

    template = yaml.load(open(template,"r").read())

    filters = [re.split(r"\s+",line.replace(":","")) for line in open(inputfile,"r").read().split("\n") if re.search(r"^Filter\s+[0-9]+:\s+ON\s+PK",line)]

    template["pipeline"].append({"channel": 0, "names": [], "type": "Filter"})
    template["pipeline"].append({"channel": 1, "names": [], "type": "Filter"})
    for filter in filters:
        template["filters"][f"biquad{filter[1]}"] = {
            "parameters": {
                "gain": float(filter[8]),
                "freq": float(filter[5]),
                "q": float(filter[11]),
                "type": "Peaking"
            },
            "type": "Biquad"
        }
        template["pipeline"][-2]["names"].append(f"biquad{filter[1]}")
        template["pipeline"][-1]["names"].append(f"biquad{filter[1]}")
    open(outputfile,"w").write(yaml.dump(template))

if __name__ == "__main__":
    convert(*sys.argv[1:])