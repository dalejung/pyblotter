import trtools.rpy.api as trpy
from rpy2.robjects import r

def get_portfolio(portname):
    port = r['getPortfolio'](portname)
    return port

class BlotterPortfolio(object):
    def __init__(self, symbols=None, summary=None, currency=['USD']):
        self.symbols = symbols
        self.summary = summary
        # symbol portfolios. Portfolio$symbols
        self.sports = {}
        self.currency = currency

    def __repr__(self):
        return "Symbols: "+"\t".join(self.symbols)

    def __getattr__(self, name):
        # provide access to symbol portfolios
        if name in self.symbols:
            return self.sports[name]
        raise AttributeError()

class SymbolPortfolio(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.txn = None
        self.posPL = None
        self.posPL_ccy = {}

def convert_blotter_portfolio(bport):
    r_summary = bport.summary
    r_symbols = bport.symbols
    symbols = list(r_symbols.names)
    bp = BlotterPortfolio(symbols=symbols)
    bp.summary = r_summary
    for s in symbols:
        sport = convert_symbol_portfolio(bport, s)
        bp.sports[s] = sport
    return bp

def convert_symbol_portfolio(bp, s):
    r_sport = bp.symbols.rx2(s)
    sp = SymbolPortfolio(s)
    sp.txn = r_sport.rx2('txn')
    sp.posPL = r_sport.rx2('posPL')
    for c in bp.currency:
        sp.posPL_ccy[c] = r_sport.rx2("posPL.{0}".format(c)) 
    return sp


if __name__ == '__main__':
    port = get_portfolio('faber')
    bp = convert_blotter_portfolio(port)
    print bp
