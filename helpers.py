A, B = "A", "B"

tone_map={
    "Abm": [1, A],
    "G#m": [1, A],
    "B": [1, B],
    "Ebm": [2, A],
    "Gb": [2, B],
    "F#": [2, B],
    "Bbm": [2, A],
    "Db": [3, B],
    "Fm": [4, A],
    "Ab": [4, B],
    "Cm": [5, A],
    "Eb": [5, B],
    "Gm": [6, A],
    "Bb": [6, B],
    "Dm": [7, A],
    "F": [7, B],
    "Am": [8, A],
    "C": [8, B],
    "Em": [9, A],
    "G": [9, B],
    "Bm": [10, A],
    "D": [10, B],
    "Gbm": [11, A],
    "F#m": [11, A],
    "A": [11, B],
    "Dbm": [12, A],
    "C#m": [12, A],
    "E": [12, B],
}

def get_shifted_key_tone(tone, shift):
    new_tone = (tone[0] - 1 - (5 * shift)) % 12 + 1
    return [new_tone, tone[1]]

def tone_repr(tone):
    return "{}{}".format(tone[0], tone[1])