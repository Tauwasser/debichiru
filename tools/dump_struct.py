# #!/usr/bin/env python3
# coding: utf-8

import argparse
from textwrap import dedent
from re import compile, fullmatch
from struct import unpack
from math import log, ceil
from os import makedirs
import sys

from read_charmap import read_charmap
from util import *
import gb

format_pattern = '([0-9]*)([cbnhw])'
format_lengths = {'b': 1, 'c': 1, 'h': 2, 'n': 1}

if __name__ == '__main__':
    # argument parser
    ap = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument('-O', dest='outdir', help='split file output directory')
    ap.add_argument('-o', dest='outfile', default=sys.stdout, help='output file name')
    ap.add_argument('-m', dest='charmap', default='charmap.asm', help='charmap file name')
    ap.add_argument('-s', '--split', dest='split', default=False, help='split into individual files', action='store_true')
    ap.add_argument('-l', '--label', dest='label', default=False, help='label each element with \'.loc_<address>\'', action='store_true')
    ap.add_argument('-n', '--names', dest='namefile', help='file containing output file names')
    ap.add_argument('rom', help='path to ROM')
    ap.add_argument('start', help='start offset', type=gb.str2address)
    ap.add_argument('format', help=dedent('''\
                                          element description
                                          sequence of [length]specifier
                                          c - character
                                          n - two nibbles
                                          b - byte
                                          h - 16-bit word
                                          
                                          Ex: 16ch2nh
                                          16 (text) characters, one 16-bit word,
                                          two bytes parsed as nibbles and one 16-bit word.
                                          
                                          ''')
                               , type=str
                   )
    ap.add_argument('elems', help='number of elements in array of structs', type=lambda x: int(x,0))
    
    args = ap.parse_args()
    romname = args.rom
    addr = args.start
    format = args.format
    elems = args.elems
    outfile = args.outfile
    outdir = args.outdir
    split = args.split
    namefile = args.namefile
    label = args.label
    
    if (split and outdir is None):
        raise RuntimeError('Cannot split without output directory.')
    
    if (not split and outdir):
        raise RuntimeError('Did you forget to specify --split?')
    
    if fullmatch('({0:s})+'.format(format_pattern), format) is None:
        raise ValueError('Format string invalid: \'{0}\'.'.format(format))
    
    f_regex = compile(format_pattern)
    
    if ('c' in format):
        charmap = read_charmap(args.charmap)
    
    names = []
    if (namefile is not None):
        with open(namefile, 'r', encoding='utf-8') as f:
            names = f.readlines()
    
    #           '{0NX}' with N is number of required figures
    namelabel = '{{0:0{0:d}X}}'.format(1 if elems == 1 else ceil(log(elems, 16)))
    
    matches = f_regex.findall(format)
    
    # calc elem length
    length = 0
    for n, c in matches:
        n = int(n) if n != '' else 1
        length += n * format_lengths[c]
    
    # read data
    with open(romname, 'rb') as r:
        r.seek(addr)
        data = r.read(length * elems)
    
    # create split directory
    if (split):
        makedirs(outdir, exist_ok=True)
    
    i = 0
    e = 0
    
    with open(outfile, 'wb') if outfile != sys.stdout else outfile.buffer as f:
        while (True):
        
            if (i + length > len(data)):
                break
            
            if (e >= elems):
                break
        
            outdirfile = outdir + '/' + (namelabel.format(e) if e >= len(names) else names[e].strip()) + '.inc'
            
            with open(outdirfile, 'wb') if split else disable_context(f) as of:
            
                if (label):
                    f.write('.loc_{0:06X}:\n'.format(addr).encode('utf-8'))
                # parse element
                for n, c in matches:
                    n = int(n) if n != '' else 1
                    
                    line = ''
                    
                    if ('b' == c):
                        line += 'db '
                        line += ', '.join(['${0:02X}'.format(e) for e in data[i:i+n]])
                        line += '\n'
                    elif ('h' == c):
                        line += 'dw '
                        line += ', '.join(['${0:04X}'.format(e) for e in unpack('{0:d}H'.format(n), data[i:i+n*2])])
                        line += '\n'
                    elif ('n' == c):
                        line += 'dn '
                        line += ', '.join(['${0:1X}, ${1:1X}'.format(e >> 4, e & 0x0F) for e in data[i:i+n]])
                        line += '\n'
                    elif ('c' == c):
                        line += 'db "'
                        line += ''.join([charmap.get(e, '\ufffd') for e in data[i:i+n]])
                        line += '"\n'
                 
                    of.write(line.encode('utf-8'))
                    i += n * format_lengths[c]
            
                if (not split):
                    of.write('\n'.encode('utf-8'))
            
            if (split):
                f.write('INCLUDE "{0:s}" ; 0x{1:06X}--0x{2:06X}\n'.format(outdirfile, addr, addr + length).encode('utf-8'))
            
            e += 1
            addr += length
    print('Done')