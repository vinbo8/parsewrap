import sys

def evaluate(gold, test):
    uas = 0
    las = 0
    total = 0
    sents = 1

    with open(gold, 'r') as f, open(test, 'r') as ref:
        while True:
            g = f.readline()
            s = ref.readline()

            if g == "":
                break

            g = g.split('\t')
            s = s.split('\t')
            
            if len(g) == len(s) == 10:
                if s[6] == g[6]:
                    uas += 1
                if s[6] == g[6] and s[7] == g[7]:
                    las += 1

                total += 1

    uas = uas * 100 / total
    las = las * 100 / total
    return (uas, las)
