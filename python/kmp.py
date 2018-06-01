def partial_match_table(string):
    pmt = [0] * len(string)

    # whole substring is not considered
    i = 1
    prev_len = 0

    while i < len(string):
        if string[i] == string[prev_len]:
            prev_len += 1
            pmt[i] = prev_len
            i += 1
        else:
            if prev_len == 0:
                i += 1
            else:
                prev_len = pmt[prev_len - 1]
    return pmt


def kmp_match(string, pattern):
    pmt = partial_match_table(pattern)

    print(pmt)

    match_location = []

    string_size = len(string)
    pattern_size = len(pattern)

    i = 0  # index for string
    j = 0  # index for pattern

    while i < string_size:
        if j == pattern_size:
            match_location.append(i - pattern_size)
            j = pmt[j - 1]
            continue
        if string[i] == pattern[j]:
            i += 1
            j += 1
        else:
            if j == 0:
                i += 1
            else:
                j = pmt[j - 1]
    if j == pattern_size:
        match_location.append(i - pattern_size)

    return match_location


text = "AABAACAADAABAABA"
pattern = "AABA"

print(kmp_match(text, pattern))
