import difflib


def find_string_differences(str1, str2, abbreviations=None):
    """
    Find and return the letter-wise differences between two strings.

    :param str1: The first string
    :param str2: The second string
    :param abbreviations: A dictionary of allowed abbreviations (optional)
    :return: A tuple containing two lists of strings representing the allowed and unallowed letter-wise differences
    """

    # Default abbreviations
    if abbreviations is None:
        abbreviations = {
            "ООО": "Общество с Ограниченной Ответственностью",
            "ЗАО": "Закрытое Акционерное Общество",
            "ОАО": "Открытое Акционерное Общество",
        }

    # Using the Differ class from difflib
    d = difflib.Differ()

    # Calculating the differences
    diff = list(d.compare(str1, str2))

    # Collecting the differences
    chunks = []
    chunk = ""
    for d in diff:
        if d.startswith("  "):
            # This is a match, reset the current chunk
            if chunk:
                chunks.append(chunk)
                chunk = ""
        elif d.startswith("- "):
            # This is a removal, ignore it
            pass
        else:
            # This is an addition, add to the current chunk
            chunk += d[2:]

    # Add the last chunk if it's non-empty
    if chunk:
        chunks.append(chunk)

    # Separate the differences into allowed and unallowed
    allowed = []
    unallowed = []
    for chunk in chunks:
        is_allowed = False
        for abbr, full in abbreviations.items():
            if chunk in full:
                is_allowed = True
                break
        if is_allowed:
            allowed.append(chunk)
        else:
            unallowed.append(chunk)

    return allowed, unallowed