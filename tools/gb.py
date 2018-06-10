# #!/usr/bin/env python3
# coding: utf-8

bank_size = 0x4000

def bank(address):
    return address // bank_size

def ptr(address):
    if (address < bank_size):
        return address & (bank_size - 1)
    return bank_size + (address & (bank_size - 1))

def str2address(s):
    if ':' in s:
        bank, ptr = [int(m, 16) for m in s.split(':', 1)]
        return ptr2address(bank, ptr)
    return int(s, 0)

def ptr2address(bank, ptr):
    if (ptr < bank_size and bank != 0):
        raise argparse.ArgumentTypeError('Illegal ROM bank 0x00 address {0:02X}:{1:04X}. '
                                         'Bank 0x{0:02X} must be 0x00.'.format(bank, ptr))
    elif (ptr >= bank_size and bank == 0):
        raise argparse.ArgumentTypeError('Illegal ROM bank 0x00 address {0:02X}:{1:04X}. '
                                         'Address 0x{1:04X} > 0x{2:04X}.'.format(bank, ptr, bank_size - 1))
    elif (ptr >= 2*bank_size):
        raise argparse.ArgumentTypeError('Illegal ROM bank address {0:02X}:{1:04X}. '
                                         'Address 0x{1:04X} > 0x{2:04X}.'.format(bank, ptr, 2*bank_size - 1))
    return bank * bank_size + (ptr & (bank_size - 1))

def addres2str(address):
    return ptr2str(bank(address), ptr(address))
    
def ptr2str(bank, ptr):
    return '{0:02X}:{1:04X}'.format(bank, ptr)