# #!/usr/bin/env python3
# coding: utf-8

class disable_context:

    def __init__(self, f):
        self._f = f
    
    def __enter__(self):
        return self._f
        
    def __exit__(self, exc_type, exc_value, traceback):
        return False
