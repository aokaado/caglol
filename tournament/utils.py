

# Create tiered list from flat list of tier 0 matches to be used in templates
def create_tiered_list(flat_list):
    list2 = []
    while (len(flat_list) > 0):
        m = flat_list.pop(0)
        if m in list2:
            continue
        if m.seedsto is not None:
            flat_list.append(m.seedsto)
        list2.append(m)

    tier_list = []
    ctier = 0
    arr = []
    while(len(list2) > 0):
        m = list2.pop(0)
        if not m.tier == ctier:
            ctier = m.tier
            tier_list.append(arr)
            arr = []
        arr.append(m)
    tier_list.append(arr)
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
