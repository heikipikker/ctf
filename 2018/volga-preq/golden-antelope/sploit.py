from pwn import *

L = [0xf1, 0xef, 0x29, 0xbe, 0xb8, 0xf6, 0x4f, 0xaf, 0xb2, 0x92, 0xe3, 0xfc, 0xc6, 0x72, 0x48, 0xc3,
     0xbf, 0xa0, 0x10, 0xd1, 0x23, 0x34, 0x0c, 0x07, 0x7c, 0xf8, 0xae, 0xe8, 0xc9, 0xe1, 0x38, 0x36,
     0x4c, 0x2c, 0x0b, 0x70, 0x7b, 0xe7, 0xd7, 0xc5, 0xac, 0x57, 0xab, 0xd5, 0x4b, 0x77, 0xa5, 0xce,
     0xee, 0xf4, 0x47, 0x25, 0x8a, 0xf3, 0xfd, 0xbb, 0x5c, 0xe0, 0x2a, 0x19, 0x5d, 0xeb, 0xa6, 0x81,
     0x12, 0x61, 0x59, 0xcf, 0xc8, 0xa8, 0xfe, 0x3e, 0x31, 0x1e, 0x46, 0x7e, 0x3d, 0xd0, 0x3c, 0xc7,
     0xdc, 0x33, 0x8f, 0xca, 0x78, 0x6f, 0x0d, 0x62, 0x9d, 0xd9, 0x89, 0x73, 0x8c, 0x4e, 0xb7, 0xc0,
     0x03, 0x56, 0xb9, 0x79, 0x75, 0xda, 0x6e, 0x1c, 0xff, 0x67, 0x2f, 0xbc, 0x69, 0x91, 0x2b, 0x9b,
     0x7f, 0x17, 0x01, 0xde, 0xfa, 0x4a, 0x02, 0x0e, 0x8b, 0xa9, 0x58, 0x2d, 0xd8, 0xf9, 0x3b, 0xb3,
     0x49, 0x65, 0xcc, 0xa3, 0xbd, 0x16, 0x21, 0xd3, 0xe5, 0xd6, 0x42, 0x60, 0x4d, 0x20, 0x97, 0x5e,
     0x2e, 0xe9, 0x18, 0xc2, 0x63, 0x64, 0xf5, 0x6a, 0xd2, 0x68, 0x1b, 0x1f, 0xc4, 0xea, 0x74, 0xa2,
     0x45, 0x82, 0xb6, 0x32, 0x84, 0xed, 0x50, 0x26, 0xcb, 0x5f, 0x37, 0xa1, 0x15, 0xa4, 0x51, 0x53,
     0xb4, 0x09, 0xaa, 0x1a, 0x14, 0x43, 0xba, 0xdf, 0x87, 0x66, 0x85, 0x52, 0x3a, 0x28, 0x9a, 0xb1,
     0x44, 0x9f, 0x96, 0x41, 0xdd, 0x86, 0x88, 0x9e, 0x71, 0xb0, 0x13, 0x98, 0xe4, 0x05, 0xf7, 0x6c,
     0xb5, 0x93, 0x8e, 0x55, 0xec, 0x8d, 0xf2, 0x6d, 0x9c, 0xa7, 0xad, 0x00, 0x08, 0xf0, 0xe6, 0x6b,
     0x7a, 0xcd, 0xfb, 0x80, 0x0a, 0x83, 0x27, 0x39, 0x30, 0x06, 0x76, 0x90, 0x94, 0x35, 0x54, 0x04,
     0x0f, 0xc1, 0x5b, 0x99, 0x11, 0x40, 0x5a, 0xd4, 0xe2, 0x95, 0x3f, 0x22, 0x7d, 0x24, 0x1d, 0xdb]

def Ha(state):
    return int("".join(map(str, state[-1:-9:-1])), 2)

class Generator:
    def __init__(self, state):
        self.state = state

    def next_state(self, idxs):
        self.idxs = idxs
        y = 0
        for i in self.idxs:
            y ^= self.state[i]
        out = self.state[31]
        for i in range(31, 0, -1):
            self.state[i] = self.state[i - 1]
        self.state[0] = y

def init_generators(g1,g2,g3):
    RX = Generator(map(int, list(bin(g1)[2:].zfill(32))))
    RA = Generator(map(int, list(bin(g2)[2:].zfill(32))))
    RB = Generator(map(int, list(bin(g3)[2:].zfill(32))))

    return (RX, RA, RB)

def next_number(RX, RA, RB):
    X = [0, 4, 5, 8, 9, 10, 13, 15, 17, 18, 27, 31]
    A0 = [0, 1, 3, 4, 6, 7, 9, 10, 11, 15, 21, 22, 25, 31]
    A1 = [0, 1, 6, 7, 8, 9, 10, 12, 16, 21, 22, 23, 24, 25, 26, 31]
    B = [0, 2, 5, 14, 15, 19, 20, 30, 31]
    range_max = 256

    RX.next_state(X)
    if RX.state[29] == 0:
        RA.next_state(A0)
    else:
        RA.next_state(A1)
    if RX.state[26] == 0:
        RB.next_state(B)
    else:
        RB.next_state(B)
        RB.next_state(B)


    return (Ha(RX.state) + L[Ha(RA.state)] + L[Ha(RB.state)]) % 256

def H(state):
    return ((state & (1 << 7)) >> 7) | \
           ((state & (1 << 6)) >> 5) | \
           ((state & (1 << 5)) >> 3) | \
           ((state & (1 << 4)) >> 1) | \
           ((state & (1 << 3)) << 1) | \
           ((state & (1 << 2)) << 3) | \
           ((state & (1 << 1)) << 5) | \
           ((state & (1 << 0)) << 7)

def nexta(a):
    return [H((H(a) * 2) % 256), H((H(a) * 2 + 1) % 256)]

def nextb(b):
    return nexta(b)

def nextc(c):
    return [(H((H(c) * 4 + i) % 256)) for i in range(4)] + nexta(c)

def bf_round(prev_keys, i):
    keys = []
    for aa,bb,cc in prev_keys:
        for aaa in nexta(aa):
            for bbb in nexta(bb):
                for ccc in nextc(cc):
                    if (H(aaa) + L[H(bbb)] + L[H(ccc)]) % 256 == n[i]:
                        if (aaa, bbb, ccc) not in keys:
                            keys.append((aaa, bbb, ccc))
    return (keys)

def recover_states(keys):

    (a, b, c) = keys[-1]
    for i in range(len(keys) - 2, 0, -1):
        print "%x %x %x" % (a, b, c)
        aa,bb,cc = keys[i]
        a <<= 1
        a |= (aa & 1)
        a &= 0xFFFFFFFF

        b <<= 1
        b |= (bb & 1)
        b &= 0xFFFFFFFF

        if ((a >> 6) & 1) == 1:
            c <<= 2
            c |= (cc & 3)
            c &= 0xFFFFFFFF
        else:
            c <<= 1
            c |= (cc & 1)
            c &= 0xFFFFFFFF

    return (a, b, c)

def bf_round0(n):
    round0 = []
    r256 = range(256)
    for aa in r256:
        for bb in r256:
            for cc in r256:
                x = (aa + L[bb] + L[cc]) % 256

                if x == n[0]:
                    round0.append((H(aa), H(bb), H(cc)))
    return round0

def bf_keys(round0, n):
    keys = []
    zero = False
    for i in range(1, len(n)):
        r = bf_round(round0, i)
        round0 = r[:]
        log.info("ROund %d --> %d" % (i, len(round0)))
        if len(round0) == 1 or zero:
            zero = True
            keys.append(round0[0])
    return keys

p = remote('golden-antelope.quals.2018.volgactf.ru', 8888)
p.recvuntil("x[:24]=='")
puzzle = p.recvn(24)
p.send(subprocess.check_output(["./puzzle", puzzle]))

n = []
for i in range(29):
    log.info("Get number %d..." % i)
    p.recvuntil("[0, 256):", timeout=3)
    p.sendline("0")
    p.recvuntil("The number was ", timeout=3)

    a = p.recvn(3).replace('.', '').replace(' ', '')
    try:
        n.append(int(a))
    except:
        n.append(0)

log.info("N=%s" % str(n))
round0 = bf_round0(n)

keys = bf_keys(round0, n)

(a, b, c) = recover_states(keys)
log.info("RX = %x" % a)
log.info("RA = %x" % b)
log.info("RB = %x" % c)

(g1, g2, g3) = init_generators(a, b, c)

print [next_number(g1, g2, g3) for i in range(len(keys) - 2)]

for i in range(107):
    log.info("Guessing %d..." % i)
    print p.recvuntil("[0, 256):")
    p.sendline(str(next_number(g1, g2, g3)))
p.interactive()
