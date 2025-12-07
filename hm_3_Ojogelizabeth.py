from timeit import timeit

# ---------------------- TIME MEASUREMENT ----------------------

def measure_time(func, text, pattern, number=100):
    return timeit(lambda: func(text, pattern), number=number)

# ---------------------- KMP ALGORITHM ----------------------

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(main_string, pattern):
    M, N = len(pattern), len(main_string)
    lps = compute_lps(pattern)

    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j
    return -1

# ---------------------- BOYER–MOORE ALGORITHM ----------------------

def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

# ---------------------- RABIN–KARP ALGORITHM ----------------------

def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    h = 0
    for i, char in enumerate(s):
        h = (h * base + ord(char)) % modulus
    return h

def rabin_karp_search(text, pattern):
    m, n = len(pattern), len(text)
    if m > n:
        return -1

    base = 256
    modulus = 101

    pattern_hash = polynomial_hash(pattern, base, modulus)
    current_hash = polynomial_hash(text[:m], base, modulus)

    h_multiplier = pow(base, m - 1, modulus)

    for i in range(n - m + 1):
        if current_hash == pattern_hash:
            if text[i:i+m] == pattern:
                return i

        if i < n - m:
            current_hash = (current_hash - ord(text[i]) * h_multiplier) % modulus
            current_hash = (current_hash * base + ord(text[i + m])) % modulus
            current_hash = (current_hash + modulus) % modulus

    return -1

# ---------------------- READ FILES ----------------------

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

text1 = read_file("article1.txt")
text2 = read_file("article2.txt")

# ---------------------- SUBSTRINGS TO TEST ----------------------

existing1 = "алгоритм"
missing1  = "qwertyzxcv"

existing2 = "даних"
missing2  = "asdfghjkl"

# ---------------------- TEST ALL ALGORITHMS ----------------------

algorithms = [
    ("KMP", kmp_search),
    ("Boyer-Moore", boyer_moore_search),
    ("Rabin-Karp", rabin_karp_search)
]

for name, func in algorithms:
    print(f"\n===== {name} =====")

    print(f"Article 1 (exists):   {measure_time(func, text1, existing1):.6f} s")
    print(f"Article 1 (missing):  {measure_time(func, text1, missing1):.6f} s")

    print(f"Article 2 (exists):   {measure_time(func, text2, existing2):.6f} s")
    print(f"Article 2 (missing):  {measure_time(func, text2, missing2):.6f} s")
