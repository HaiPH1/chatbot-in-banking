from unicodedata import normalize

replace_list = {
        'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả',
        'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè',
        'óe': 'oé', 'ỏe': 'oẻ', 'õe': 'oẽ',
        'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý',
        'ủy': 'uỷ', 'ũy': 'uỹ', 'ụy': 'uỵ',
        'uả': 'ủa', 'ả': 'ả', 'ố': 'ố', 'u´': 'ố',
        'ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ',
        'ẫ': 'ẫ', 'ẩ': 'ẩ', 'ầ': 'ầ', 'ỏ': 'ỏ',
        'ề': 'ề', 'ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ',
        'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ', 'ẻ': 'ẻ',
        'àk': ' à ', 'aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ',
        'ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á'
    }


def normalize_text(text):
    text = text.lower()
    text = normalize('NFC', text)
    for k, v in replace_list.items():
        text = text.replace(k, v)

    return text
