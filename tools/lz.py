# #!/usr/bin/env python3
# coding: utf-8

import argparse
import gb

def decompress(data):
    
    buffer = list()
    buf_ix = 0
    i = 0
    
    success = False
    
    while (i < len(data)):
    
        d = data[i]
        i += 1
    
        l = (d & 0x1F) + 1
        b = d & 0xE0
        
        if (0x80 == b):
            # literal copy
            buffer += data[i:i + l]
            buf_ix += l
            i += l
                
        elif (0xA0 == b):
            # 1bpp copy
            [buffer.extend(r) for r in zip([0] * l, data[i:i + l])]
            buf_ix += 2 * l
            i += l
            
        elif (0xC0 == b):
            # fill
            l += 1
            buffer += [data[i]] * l
            buf_ix += l
            i += 1
            
        elif (0xE0 == b):
            # fill zero
            if (0x20 == l):
                # extended fill zero
                l += data[i]
                i += 1
            
            buffer += [0] * l
            buf_ix += l
            
        else:
            # LZ code
            if (0x7F == d and 0xFF == data[i]):
                # end code
                success = True
                i += 1
                break
            
            l = ((d >> 2) & 0x1F) + 2
            back = ((d & 0x03) << 8) | data[i]
            back ^= 0x3FF
            back += 1
            i += 1
            
            if (buf_ix - back < 0):
                raise RuntimeError('LZ code {0:04X} at 0x{1:04X} tried to fetch from before start of uncompressed data.'
                                   .format((d << 8) | data[i - 1], i - 2)
                                  )
            
            buffer += buffer[buf_ix - back:buf_ix - back + l]
            buf_ix += l
    
    if (not success):
        raise RuntimeError('Decompression unsuccessful. Did not reach end code word after {0:d} bytes.'
                           .format(l(data))
                          )
    
    return i, bytearray(buffer)

if __name__ == '__main__':
    # argument parser
    ap = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument('infile', help='input file name')
    ap.add_argument('outfile', help='output file name for uncompressed data')
    ap.add_argument('start', help='start offset', type=gb.str2address)
    
    args = ap.parse_args()
    infile = args.infile
    outfile = args.outfile
    addr = args.start
    
    # read data
    with open(infile, 'rb') as f:
        f.seek(addr)
        data = f.read(gb.bank_size)
    
    compressed_size, uncompressed_data = decompress(data)
    
    with open(outfile, 'wb') as f:
        f.write(uncompressed_data)
    
    print('Compressed size: 0x{0:x}\nUncompressed size: 0x{1:x}'.format(compressed_size, len(uncompressed_data)))