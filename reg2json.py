# -*- coding: utf-8 -*-
import os.path
from datetime import datetime, timedelta, timezone
import json
import sys
import argparse
try:
    from Registry import Registry
    from Registry.Registry import RegSZ
    from Registry.Registry import RegExpandSZ
    from Registry.Registry import RegBin
    from Registry.Registry import RegDWord
    from Registry.Registry import RegMultiSZ
    from Registry.Registry import RegQWord
    from Registry.Registry import RegNone
    from Registry.Registry import RegBigEndian
    from Registry.Registry import RegLink
    from Registry.Registry import RegResourceList
    from Registry.Registry import RegFullResourceDescriptor
    from Registry.Registry import RegResourceRequirementsList
    from Registry.Registry import RegFileTime
    from Registry.Registry import DEVPROP_MASK_TYPE
except Exception as e:
    print("[x]", "pip install python-registry")
    exit(0)


class Registry2Json(object):
    def __init__(self, file_path, time_line=False, jst=False):
        self.reg_json = dict()
        self.file_path = file_path
        self.time_line = time_line
        self.jst = jst

        self.registry2json()
        self.save_json()

    def datetime2str(self, dtime):
        if self.jst:
            return (dtime + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            return dtime.strftime("%Y-%m-%d %H:%M:%S")
    

    def save_json(self):
        if self.time_line:
            self.reg_json = sorted(self.reg_json.items(), key=lambda x: x[1]["LastKeyWrite"])
        with open("{}.json".format(self.file_path), "w") as f:
            json.dump(self.reg_json, f, indent=4)
        print("[*]", "Save JSON file ->", "{}.json".format(self.file_path))


    def registry2json(self):
        def _value(key):
            res = {"data": "", "LastKeyWrite": self.datetime2str(key.timestamp())}
            vals = dict()

            for value in [v for v in key.values() if v.value_type() in [RegSZ, RegExpandSZ, RegBin, RegDWord, RegMultiSZ, RegQWord, RegNone, RegBigEndian, RegLink, RegResourceList, RegFullResourceDescriptor, RegResourceRequirementsList, RegFileTime, DEVPROP_MASK_TYPE]]:
                try:
                    tmp_v = value.value()
                    if type(value.value()) == bytes:
                        tmp_v = value.value().decode(encoding="utf-8", errors="ignore")
                    if type(value.value()) == int:
                        tmp_v = str(value.value())
                    if type(value.value()) == datetime:
                        tmp_v = self.datetime2str(value.value())
                    vals[value.name()] = tmp_v
                except Exception as e:
                    print("[x]", "err ->", e)

            res["data"] = vals
            return res

        def _key(key, depth=0):
            vals = _value(key)
            if len(vals["data"]) != 0:
                self.reg_json[key.path()] = vals
            for subkey in key.subkeys():
                _key(subkey, depth + 1)
        
        reg = Registry.Registry(self.file_path)
        _key(reg.root())


def main(args):
    for file_path in args.files:
        if os.path.exists(file_path):
            print("[+]", "Read Registry file ->", file_path)
            rg = Registry2Json(file_path, args.timeline, args.jst)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", nargs="*", help="registry file1, registry file2...")
    parser.add_argument("--timeline", action="store_true", help="sort key 'LastKeyWrite'")
    parser.add_argument("--jst", action="store_true", help="utc to jst")
    args = parser.parse_args()
    main(args)
