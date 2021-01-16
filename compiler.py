import sys
import os

INSTRUCTIONS = [
    'lda', 'ldx', 'ldy',
    'sta', 'stx', 'sty',
    'psha', 'pshx', 'pshy',
    'popa', 'popx', 'popy',
    'hlt', 'call', 'ret', 'nop',
    'cmp', 'beq', 'bne'
]

MINSTRUCT = {
    'lda': 0xa,
    'ldx': 0xb,
    'ldy': 0xc,

    'sta': 0xd,
    'stx': 0xe,
    'sty': 0xf,

    'psha': 0x10,
    'pshx': 0x11,
    'pshy': 0x12,

    'call': 0x19,
    'popa': 0x13,
    'popx': 0x14,
    'popy': 0x15,
    'hlt': 0xff,
    'ret': 0x1c,
    'nop': 0x1,
    'cmp': 0x16,
    'beq': 0x17,
    'bne': 0x18

    #'lda': 0x10,
    #'lda': 0x11,
    #'lda': 0x12,

#    'lda': 0x13,
#    'lda': 0x14,
#    'lda': 0x15,#

#    'lda': 0x16,
 #   'lda': 0x17,
}

class Token:
    def __init__(self, vtype, value=None):
        self.type = vtype
        self.value = value
    def __str__(self):
        return f"[{self.type}:{self.value or 0}]"

class Error:
    def __init__(self, name="Error", message=""):
        self.name = name
        self.message = message
    def throw(self):
        print(f"{self.name}: {self.message}")
        exit(1)
        

class Lexer:
    def __init__(self, fName):
        self.content = open(fName, "r").read()
        self.tokens = []
    def make_tokens(self):
       # words = self.content.split()
        currentLine = 0
        currentWord = -1
        wordsInLine = []
        incL = False
        commented = False
        lines = self.content.splitlines()
        for line in lines:
            words = line.split()
            wordsInLine = []    
            commented = False
            for word in words:
                wordsInLine.append(word)
                if ';' in word:
                    commented = True
                if commented:
                    self.tokens.append(Token("COMMENT", word))
                elif word.isnumeric():
                    self.tokens.append(Token('DIGIT', int(word)))
                elif word in INSTRUCTIONS:
                    self.tokens.append(Token('INSTRUCTION', word))
                elif word.startswith("."):
                    self.tokens.append(Token('LABEL', word))
                else:
                    Error('UNDEFINED TOKEN', word).throw()
        
        i = 0
        while i < 5:
            self.tokens.append(Token("NULL", "NULL"))
            i+=1

def convert(arr):
    i = 0
    while i < len(arr):
        if arr[i] < 0:
            arr[i] = 0
        elif arr[i] > 255:
            arr[i] = 255
        i += 1
    
    ost = bytearray(arr)
    #i = 0
    
    #    i += 1
    
    return ost

class Compiler:
    def __init__(self, tokens=[]):
        self.tokens = tokens
        self.current_token = 0
        self.tok = self.tokens[self.current_token]
    def _fetch(self):
        self.current_token += 1
        self.tok = self.tokens[self.current_token]
        return self.tok
    def compile(self, outfile='a.out'):
        bino = []
       # bino.append(1)
       # bino = bino*1024
       # print(bino)
        while self.current_token < (len(self.tokens)-1):
            if self.tok.type == 'INSTRUCTION':
                if self.tok.value.startswith('ld') and self.tok.value in INSTRUCTIONS:
                    bino.append(MINSTRUCT[self.tok.value])
                    bino.append(self._fetch().value)
                elif self.tok.value.startswith('st') and self.tok.value in INSTRUCTIONS:
                    bino.append(MINSTRUCT[self.tok.value])
                    bino.append(self._fetch().value)
                    bino.append(self._fetch().value)
                elif self.tok.value.startswith('psh') and self.tok.value in INSTRUCTIONS:
                    bino.append(MINSTRUCT[self.tok.value])
                elif self.tok.value == 'call' and self.tok.value in INSTRUCTIONS:
                    bino.append(MINSTRUCT[self.tok.value])
                    bino.append(self._fetch().value)
                    bino.append(self._fetch().value)
                elif self.tok.value == 'cmp' and self.tok.value in INSTRUCTIONS:
                    bino.append(MINSTRUCT[self.tok.value])
                    bino.append(self._fetch().value)
                    bino.append(self._fetch().value)
                elif self.tok.value == 'beq' or self.tok.value == 'bne':
                    bino.append(MINSTRUCT[self.tok.value])
                    bino.append(self._fetch().value)
                    bino.append(self._fetch().value)
                elif self.tok.value == 'hlt' and self.tok.value in INSTRUCTIONS:
                    bino.append(MINSTRUCT[self.tok.value])
                else:
                    Error("Compiler error", f"Wrong token: {self.tok}").throw()
                    #'okay'
            elif self.tok.type == 'LABEL':
                addr = self.tok.value[1::]
                print(len(bino))
                while int(addr) > len(bino)-5:
                    bino.append(0)
                
                j = 0
                while self.tok.value != 'ret':
                    self._fetch()
                    print(int(addr)+j)
                    if self.tok.type == 'INSTRUCTION':
                        bino.append( MINSTRUCT[self.tok.value])
                    elif str(self.tok.value).isnumeric():
                        bino.append(int(self.tok.value))
                    j += 1
                    
            self._fetch()
        open(outfile, 'wb').write(convert(bino))
            

if __name__ == '__main__':
    lex = Lexer(sys.argv[1])
    lex.make_tokens()
    tokens = lex.tokens
    for token in tokens:
        print(token)
    
    comp = Compiler(tokens)
    if os.path.exists(sys.argv[2]):
        os.remove(sys.argv[2])
    comp.compile(sys.argv[2])
    #print(sys.argv)