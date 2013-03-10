

# Create tiered list from flat list of tier 0 matches to be used in templates
def create_tiered_list(flat_list):
    list2 = []
    while (len(flat_list) > 0):
        m = flat_list.pop(0)
        if m in list2:
            continue
        if m.seedsto is not None and m.seedsto.level == m.level:
            flat_list.append(m.seedsto)
        list2.append(m)

    tier_list = []
    ctier = list2[0].tier
    arr = []
    while(len(list2) > 0):
        m = list2.pop(0)
        if not m.tier == ctier:
            ctier = m.tier
            lastlen = 0 if len(tier_list) == 0 else len(tier_list[-1]['data'])
            lastdiff = 0 if len(tier_list) == 0 else tier_list[-1]['diff']
            info = {'data': arr, 'diff': lastdiff + max(lastlen - len(arr), 0), 'tier': ctier}
            tier_list.append(info)
            arr = []
        arr.append(m)

    lastlen = 0 if len(tier_list) == 0 else len(tier_list[-1]['data'])
    lastdiff = 0 if len(tier_list) == 0 else tier_list[-1]['diff']
    info = {'data': arr, 'diff':  lastdiff + lastlen - len(arr), 'tier': ctier}
    tier_list.append(info)

    return tier_list


def pow2roundup(x):
    if x < 0:
        return 0
    x -= 1
    x |= x >> 1
    x |= x >> 2
    x |= x >> 4
    x |= x >> 8
    x |= x >> 16
    return x+1
