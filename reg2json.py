# -*- coding: utf-8 -*-
import os.path
from datetime import datetime
import json
import sys
try:
    from Registry import Registry
except Exception as e:
    print("[x]", "pip install python-registry")
    exit(0)

def registry2json(file_name):
    reg_json = dict()
    def _value(key):
        res = {"data": "", "timestamp": key.timestamp().strftime("%Y-%m-%d %H:%M:%S")}
        vals = dict()
        for value in [v for v in key.values() if v.value_type() == Registry.RegSZ or v.value_type() == Registry.RegExpandSZ]:
            vals[value.name()] = value.value()
        res["data"] = vals
        return res

    def _key(key, depth=0):
        vals = _value(key)
        if len(vals["data"]) != 0:
            reg_json[key.path()] = vals
        for subkey in key.subkeys():
            _key(subkey, depth + 1)

    reg = Registry.Registry(file_name)
    _key(reg.root())

    with open("{}.json".format(file_name), "w") as f:
        json.dump(reg_json, f, indent=4)

def main(argvs):
    if len(argvs) > 1:
        for file_name in argvs[1::]:
            if os.path.exists(file_name):
                print("[+]", "Now Processing ->", file_name)
                registry2json(file_name)
            else:
                print("[x]", "No sush file or directry ->", file_name)
    else:
        print("[x]", argvs[0], "hve_file1", "hve_file2", "...")

if __name__ == '__main__':
    main(sys.argv)
