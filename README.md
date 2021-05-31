# reg2json

```bash
usage: reg2json.py [-h] [-f [FILES [FILES ...]]] [--timeline] [--jst]

optional arguments:
  -h, --help            show this help message and exit
  -f [FILES [FILES ...]], --files [FILES [FILES ...]]
                        registry file1, registry file2...
  --timeline            sort key 'LastKeyWrite'
  --jst                 utc to jst

Examples: reg2json.py -f SYSTEM SOFTWARE
Examples: reg2json.py -f SYSTEM --timeline --jst
```
