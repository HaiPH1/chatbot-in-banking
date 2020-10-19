from unicodedata import normalize

replace_list = {
        'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả',
        'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè',
        'óe': 'oé', 'ỏe': 'oẻ', 'õe': 'oẽ',
        'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý',
        'ủy': 'uỷ', 'ũy': 'uỹ', 'ụy': 'uỵ',
        'uả': 'ủa'
    }


def normalize_text(text):
    text = text.lower()
    text = normalize('NFC', text)
    for k, v in replace_list.items():
        text = text.replace(v, k)

    return text
