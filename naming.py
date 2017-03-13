import string

_tokens = dict()
_rules = {"_active": None}


def add_rule(name, *fields):
    if has_rule(name):
        return False
    pattern = "{{{}}}".format("}_{".join(fields))
    _rules[name] = pattern
    if active_rule() is None:
        set_active_rule(name)
    return True

def flush_rules():
    _rules.clear()
    _rules["_active"] = None
    return True

def remove_rule(name):
    if has_rule(name):
        del _rules[name]
        return True
    return False

def has_rule(name):
    return name in _rules.keys()

def active_rule():
    k = _rules["_active"]
    return _rules.get(k)

def set_active_rule(name):
    if not has_rule(name):
        return False
    _rules["_active"] = name


def add_token(name, **kwds):
    if len(kwds) == 0:
        _tokens[name] = None
        return True
    if kwds.get("default"):
        kwds["_default"] = kwds["default"]
        del kwds["default"]
    _tokens[name] = kwds
    return True

def flush_tokens():
    _tokens.clear()
    return True

def remove_token(name):
    if has_token(name):
        del _tokens[name]
        return True
    return False

def has_token(name):
    return name in _tokens.keys()


def solve(*args, **kwds):
    i = 0
    values = dict()
    rule = active_rule()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    for f in fields:
        lookup = _tokens[f]
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
    rule = active_rule()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    split_name = name.split("_")
    for i, f in enumerate(fields):
        value = split_name[i]
        lookup = _tokens[f]
        if lookup is None:  # required
            retval[f] = value
            continue
        for k, v in lookup.iteritems():
            if v == value and k != "_default":
                retval[f] = k
                continue
    return retval
