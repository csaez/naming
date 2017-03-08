rule = "{description}_{side}_{type}"
tokens = {
    "description": None,
    "side": {
        "left": "L",
        "right": "R",
        "middle": "M",
        "center": "M",
    },
    "type": {
        "animation": "anim",
    },
}


def solve(**kwds):
    values = dict()
    for k, v in kwds.iteritems():
        lookup = tokens[k]
        if lookup is None:
            values[k] = v
            continue
        values[k] = lookup[v]
    return rule.format(**values)
