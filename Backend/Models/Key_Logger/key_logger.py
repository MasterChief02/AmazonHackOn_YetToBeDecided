import sys

def string_mismatch(str1, str2, m, n):
    if m == 0:
        return n
    if n == 0:
        return m
    if str1[m-1] == str2[n-1]:
        return string_mismatch(str1, str2, m-1, n-1)

    return 1 + min(string_mismatch(str1, str2, m, n-1),    # Insert
                   string_mismatch(str1, str2, m-1, n),    # Remove
                   string_mismatch(str1, str2, m-1, n-1)    # Replace
                   )

def string_distance(str1, str2):
    str1 = str(str1)
    str2 = str(str2)
    return string_mismatch(str1, str2, len(str1), len(str2))/max(len(str1), len(str2))


if __name__ == "__main__":
    print(string_distance(sys.argv[1], sys.argv[2]))