'''
utilities
'''
import re
import yaml
from subprocess import Popen,PIPE

import logging

logger = logging.getLogger(__name__)


def fix_sentence_spacing(txt,N=1):
    """
    Replace any period followed by a sequence of spaces with
    a period followed by N spaces.
    """
    return re.sub('[.][ ]+', '.'+' '*N, txt)


def parse_metadata(doc,join='\n'):
    """
    Parse the metadata from a document and parse it
    as a YAML dict and return it.
    """
    doc = doc.strip()
    if doc.startswith('---\n') and ('...' in doc or '---' in doc[4:]):
        # found starting yaml block
        yblock = doc[4:].split('...')[0].split('---')[0]
        meta = yaml.load(yblock, Loader=yaml.SafeLoader)
        for k in meta.keys():
            val = meta[k]
            if isinstance(val,list):
                meta[k] = join.join(val)
        meta['metadata_yaml_length'] = len(yblock) + 7
        return meta
    else:
        # No yaml
        return {}

def pandoc(input, *args):
    """
    Run pandoc with the given arguments and return
    the contents of stdout as a string.
    """
    out,err = Popen(["pandoc"] + list(args),encoding='utf8',stdin=PIPE,stdout=PIPE).communicate(input=input)

    if err:
        print(err)
    return out

def oascript(script):
    """
    Execute the given script as AppleScript
    Using the oascript command line tool.
    """
    Popen(['osascript', '-'], encoding='utf8', stdin=PIPE, stdout=PIPE).communicate(script)

def get_in(D,keys,default):
    logger.debug(f"GET_IN {D} {keys} {default}")
    try:
        value = D[keys[0]]
        if len(keys) > 1:
            return get_in(value,keys[1:],default)
        else:
            return value
    except KeyError as e:
        logger.debug(f"get_in KeyError: {e}")
        return default
    except TypeError as e:
        logger.debug(f"get_in TypeError: {e}")
        return default

def int_to_roman(input):
    """ Convert an integer to a Roman numeral. """

    if not isinstance(input, type(1)):
        raise TypeError(f"expected integer, got {type(input)}") 
    if not 0 < input < 4000:
        raise ValueError(f"Argument must be between 1 and 3999. Got {input}.")
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)
