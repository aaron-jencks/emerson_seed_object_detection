import base64
import random
import timeit
import array
import struct


test = [random.randint(0, 255) for x in range(3000)]


if __name__ == "__main__":
    print("Data Encoding")
    print('raw: {}, {}'.format(len(test), test))
    b = str(test).encode('latin-1')
    print('bytes: {}, {}'.format(len(b), b))
    b6 = base64.b85encode(b)
    print('base64: {}, {}'.format(len(b6), b6))

    print("Unpacking data")
    print('Array: {}'.format(array.array('H', b)[:5]))
    print('Struct: {}'.format(struct.unpack('{}H'.format(len(b)//2), b)[:5]))
    print("Array: {}".format(timeit.timeit('array.array("H", b)', setup='from __main__ import b, array')))
    print("Struct: {}".format(timeit.timeit('struct.unpack("{}H".format(len(b)//2), b)',
                                            setup='from __main__ import b, struct')))
