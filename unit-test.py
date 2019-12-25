from functools import reduce

if __name__ == '__main__':
    d = dict()
    d.update({'abc': 123})
    print(d)

    def A(x):
        print(x + 1)

    d.update({'epc': A})
    print(d)
    print(d['abc'])