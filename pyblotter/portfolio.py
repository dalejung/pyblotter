import trtools.rpy.conversion
from rpy2.robjects import r

def get_portfolio(portname):
    port = r['getPortfolio'](portname)
    return port
