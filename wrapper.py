# -*- coding: utf-8 -*-

class Wrapper(object):
    """"""
    _textlines  = []
    _tokens     = [] # Line Tokens
    _maxlinelen = 58 # Value for Taimanin Asagi 2 Premium Box. Change accordingly for your game
    _maxlines   = 3 # max lines in a text block
    _newline    = u'\r\n'
    _doublewidthchars = [u'「', u'」', u'『', u'』', u'\u3000']
    _baselineno = None
    
    def __init__(self):
        pass
    
    def clear(self):
        """
        Resets the object to its initial state
        """
        self._tokens  = [] # Lines Tokens
    
    def wrap(self, textlines, baselineno):
        self._textlines = textlines
        self._baselineno = baselineno
        dowrap = False
        
        # Only wrap if one or more lines exceed the max length
        for line in self._textlines:
            #print self.lenignoretag(line)
            if (self.lenignoretag(line) > self._maxlinelen):
                dowrap = True;
                break
        
        if (not dowrap):
            return self._textlines
            #print "map", map(self.tokenize, self._textlines)f._textlines
        
        # Wrap segment
        self._tokens = map(self.tokenize, self._textlines)
        
        # Flatten tokens list
        flattokens = []
        for i in range(len(self._tokens)):
            flattokens += self._tokens[i]
        #print "Flattokens", flattokens
        
        # Wrap loop
        tmp = []
        newtokens = []
        n = 0
        for t in flattokens:
            if (n + self.lenignoretag(t) <= self._maxlinelen):
                n += self.lenignoretag(t)
                tmp.append(t)
            else:
                # Line is full
                newtokens.append(tmp)
                n = 0
                if (t != u' '):
                    tmp = [t]
                    n += self.lenignoretag(t)
                else:
                    tmp = []
                
        newtokens.append(tmp)
        
        #print "N:", len(newtokens)
        #print "Newtokens:", newtokens
        return self.tokenstostringlist(newtokens)
    
    # ============================================================================
    
    def lenignoretag(self, line):
        n = 0
        level = 0
        for c in line.rstrip():
            if (c == u'['):
                level += 1
                continue
            elif (c == u']'):
                level -= 1
                continue
            
            if (level == 0):
                n += 1
                
        return n
    
    # ============================================================================
    
    def tokenstostringlist(self, tokens):
        lines = []
        #print "Token:", tokens
        for tokenlist in tokens:
            line = u''
            for word in tokenlist:
                line += word
            line += self._newline
            lines.append(line)
        #print "lines:", lines
        return lines
    
    # ============================================================================
    
    def tokenize(self, line):
        """
        Breaks the line into tokens: wide spaces, spaces, words, tags. Removes trailing control characters
        Returns a list of tokens representing their string values.
        """
        T = []
        lvl = 0
        tok_ini = 0
        s = u''
        
        for i in range(len(line)):
            if(line[i] == u'\u3000' and lvl == 0):
                # Detect word
                s = line[tok_ini:i]
                if(len(s) > 0):
                    T.append(s)
                T.append(u'\u3000')
                tok_ini = i+1
            elif(line[i] == u' ' and lvl == 0):
                # Detect word
                s = line[tok_ini:i]
                if(len(s) > 0):
                    T.append(s) #single word
                T.append(u' ')
                tok_ini = i+1
            elif(line[i] == u',' and lvl == 0):
                # Detect word
                s = line[tok_ini:i+1]
                T.append(s) #single word
                tok_ini = i+1
            elif(line[i] == u'['):
                # Detect start tag
                lvl += 1
                T.append(line[tok_ini:i])
                tok_ini = i
            elif(line[i] == u']'):
                # Detect end tag
                lvl -= 1
                T.append(line[tok_ini:i+1])
                tok_ini = i+1
            else:
                pass
                                    
        s = line[tok_ini:len(line)].rstrip()
        if(len(s) > 0):
            T.append(s)
                                        
        #print "Tokens:", len(T)
        #print T
        return T