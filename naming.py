import string

rule = "{description}_{side}_{type}"
tokens = {
    "description": None,
    "side": {
        "left": "L",
        "right": "R",
        "middle": "M",
        "_default": "M",
    },
    "type": {
        "animation": "anim",
        "control": "ctrl",
        "joint": "jnt",
        "_default": "ctrl",
    },
}


def solve(*args, **kwds):
    i = 0
    values = dict()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    for f in fields:
        lookup = tokens[f]
        if lookup is None:  # required
            if kwds.get(f) is not None:
                values[f] = kwds[f]
                continue
            values[f] = args[i]
            i += 1
            continue
        values[f] = lookup[kwds.get(f, "_default")]
    return rule.format(**values)


def parse(name):
    retval = dict()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    split_name = name.split("_")
    for i, f in enumerate(fields):
        value = split_name[i]
        lookup = tokens[f]
        if lookup is None:  # required
            retval[f] = value
            continue
        for k, v in lookup.iteritems():
            if v == value and k != "_default":
                retval[f] = k
                continue
    return retval
