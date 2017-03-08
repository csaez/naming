import string

rule = "{description}_{side}_{type}"
tokens = {
    "description": None,
    "side": {
        "left": "L",
        "right": "R",
        "middle": "M",
        "center": "M",
        "_default": "M",
    },
    "type": {
        "animation": "anim",
        "control": "ctrl",
        "joint": "jnt",
        "_default": "ctrl",
    },
}


def solve(**kwds):
    values = dict()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    for f in fields:
        lookup = tokens[f]
        if lookup is None:
            values[f] = kwds[f]
            continue
        values[f] = lookup[kwds.get(f, "_default")]
    return rule.format(**values)
