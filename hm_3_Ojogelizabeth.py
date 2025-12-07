from timeit import timeit

# ------------------ TIME MEASUREMENT FUNCTION ------------------

def measure_time(func, text, pattern, number=100):
    return timeit(lambda: func(text, pattern), number=number)


# ------------------ KMP ALGORITHM ------------------

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


def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)
    if M == 0 or N == 0:
        return -1

    lps = compute_lps(pattern)
    i = j = 0

    while i < N:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


# ------------------ BOYER-MOORE ------------------

def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift.get(text[i + len(pattern) - 1], len(pattern))

    return -1


# ------------------ RABIN-KARP ------------------

def polynomial_hash(s, base=256, modulus=101):
    hash_value = 0
    for i, ch in enumerate(s):
        power = pow(base, len(s) - i - 1, modulus)
        hash_value = (hash_value + ord(ch) * power) % modulus
    return hash_value


def rabin_karp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0 or n == 0 or m > n:
        return -1

    base = 256
    mod = 101

    pattern_hash = polynomial_hash(pattern, base, mod)
    window_hash = polynomial_hash(text[:m], base, mod)
    h = pow(base, m - 1, mod)

    for i in range(n - m + 1):
        if window_hash == pattern_hash:
            if text[i:i+m] == pattern:
                return i

        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * h) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod

    return -1


# ------------------ SAFE FILE READING ------------------

def read_file(path):
    try:
        return open(path, "r", encoding="utf-8").read()
    except UnicodeDecodeError:
        return open(path, "r", encoding="latin-1").read()


# ------------------ LOAD TEXT FILES ------------------

text1 = read_file("article1.txt")
text2 = read_file("article2.txt")

# ------------------ SELECT SUBSTRINGS ------------------

existing1 = "алгоритм"
missing1 = "qwertyzxcv"

existing2 = "даних"
missing2 = "asdfghjkl"

algorithms = [
    ("KMP", kmp_search),
    ("Boyer-Moore", boyer_moore_search),
    ("Rabin-Karp", rabin_karp_search),
]


# ------------------ RUN MEASUREMENTS ------------------

for name, func in algorithms:
    print(f"\n===== {name} =====")

    print(f"Article 1 (exists):   {measure_time(func, text1, existing1):.6f} s")
    print(f"Article 1 (missing):  {measure_time(func, text1, missing1):.6f} s")

    print(f"Article 2 (exists):   {measure_time(func, text2, existing2):.6f} s")
    print(f"Article 2 (missing):  {measure_time(func, text2, missing2):.6f} s")

    print("-" * 40)
