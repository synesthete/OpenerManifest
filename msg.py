import sys
import subprocess
import re
import os
import shutil
import json
from collections import OrderedDict # http://stackoverflow.com/a/10982037

if len(sys.argv) < 2:
    print "No path specified"
    sys.exit()
    
path = sys.argv[1]

data = json.loads(open(path).read(), object_pairs_hook=OrderedDict) # http://stackoverflow.com/a/6921760

import msgpack
packed_dict = msgpack.packb(data)
open(path.replace('.json', '.msgpack'), 'w').write(packed_dict)