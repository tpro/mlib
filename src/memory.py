import types
import sys,os
import struct
from StringIO import StringIO


### sys._getframe(1).f_code.co_name
class M(object):

    TRANSL = { 'byte':('B',1),'word':('H',2),'dword':('I',4),'qword':('Q',8) }
    
    def __init__(self,d,end_fmt=''):
        self._len = len(d)
        self.b = StringIO(d)

    def _get_bytes(self,fmt,s,at=False,off=0):
        return struct.unpack(fmt,self.read_at(off,s) if at else self.read(s) )[0]
    
    def skip(self,n):
        self.b.seek(n,os.SEEK_CUR)
        
    def unskip(self,n):
        self.b.seek(-n,os.SEEK_CUR)
        
    def read(self, n):
	return self.b.read(n)

    def read_at(self,off,n):
        old_l = self.b.tell()
        self.b.seek(off,os.SEEK_SET)
        r = self.b.read(n)
        self.b.seek(old_l,os.SEEK_SET)
        return r

    # def bytes(self,t):
    #     s=  self.dword()
    #     return self.read
    def __len__(self):
	return self._len

    def __getattr__(self, name):
        at =False
        if name.endswith('_at'):
            at = True
            name = name.strip('_at')
        
        if name in M.TRANSL:
            f,s = M.TRANSL[name]
            return (lambda off : self._get_bytes(f,s,at,off)) if at else (lambda: self._get_bytes(f,s))
        
    #setattr(M,typ+'_at',lambda cl,off: struct.unpack(fmt,cl.read_at(off,s))[0])

if __name__ == '__main__':
    m  =M(sys.stdin.read())
    print dir(m)
    print m.word,m.byte
#    print m.byte()
    print m.dword()
#    print m.word_at(0)
