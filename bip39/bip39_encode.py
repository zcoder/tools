from collections import OrderedDict
import argparse

def load_words():
    words = OrderedDict()
    with open('english.txt', 'r') as f:
        for n, word in enumerate(f.readlines()):
            words[word.strip()]=n
    return words

def print_words(words):
    for k,v in words.items():
        print(f'{(v+1)} {k}')

def encode_words_to_num(src:list, words)-> list:
    result = []
    for s in src:
        assert s in words
        result.append(words[s])
    return result

def decode_words_from_num(src:list, words)->list:
    result = []
    for s in src:
        result.append(list(words.keys())[s])
    return result

def digit_encode(digits:list):
    r = 1
    for d in digits:
        r = r * 2048 + d
    return r

def digit_decode(digit:int):
    l = []
    r=digit
    while True:
        l.insert(0, r % 2048)
        r = r // 2048
        if r == 1:
            break
    return l

def main(args):
    words = load_words()

    if args.mode == 'encode':
        src = [s.strip() for s in args.list.split(',')]
        print(src)
        digits = encode_words_to_num(src=src, words=words)
        # print(encoded)
        encoded = digit_encode(digits)
        print(encoded)
        print(f'{encoded:x}')
        print(':'.join((str(d+1) for d in digits)))


        dec_nums = digit_decode(encoded)
        decoded = decode_words_from_num(src=dec_nums, words=words)
        print(decoded)

        print(f'check: {src==decoded}')

    elif args.mode == 'decode':
        # src = [int(s.strip()) for s in args.list.split(':')]
        if args.fmt == 'base10':
            dec_nums = digit_decode(int(args.list))
        elif args.fmt == 'base16':
            dec_nums = digit_decode(int(args.list, 16))
        elif args.fmt == 'list':
            dec_nums = [int(d)-1 for d in args.list.split(':')]
        else:
            raise NotImplemented()

        decoded = decode_words_from_num(src=dec_nums, words=words)
        print(decoded)

    elif args.mode == 'dict':
        print_words(words=words)

    else:
        assert NotImplemented()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='encode bip')
    parser.add_argument('--mode', dest='mode', default='encode', help='mode: encode|decode|dict')
    parser.add_argument('--fmt', dest='fmt', default='list', help='fmt: base10, base16, list')
    parser.add_argument('--list', dest='list', required=True, help='list of words or nums')

    debug_args = [
        '--mode', 'encode',
        '--list', "abandon, ability,  abandon, abandon, abandon, absurd, accident, know, labor, zoo, zoo, zoo, abandon, ability,  abandon, abandon, abandon, absurd, accident, know, labor, zoo, zoo, zoo",
        # '--list', "zoo",
    ]

    debug_args2 = [
        '--mode', 'decode',
        '--list', "29642781912141205145187619303130401618309341090787783132132310519182704016097279",
    ]



    # args = parser.parse_args(debug_args)
    args = parser.parse_args()
    main(args)