def soundcomp(comp):
    r = comp.real if comp.real != 0 else 0
    i = comp.imag if comp.imag != 0 else 0
    return 'r' + '%.4f'%r + 'i' + '%.4f'%i

class SoundexDict(dict):
    def __getitem__(self, key):
        return super().__getitem__(soundcomp(key))

    def __setitem__(self, key, value):
        super().__setitem__(soundcomp(key), value)

print(soundcomp(-0-0.25j))
print(soundcomp(-0.25j))
print(-0 == 0)