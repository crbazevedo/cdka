"""Construct the whole contrast-bounded policy strip from a physical erasure gate."""
from fractions import Fraction as F


def erasure_selector(f0:F,f1:F,sigma:F)->tuple[F,F,F]:
    """Return fallback probability r and readable-input actions b0,b1.

    Input is readable with probability sigma; otherwise a flagged erasure
    arrives and the mechanism cannot condition on m. No flag persists.
    f_i=(1-sigma)*r+sigma*b_i. Fresh coins, no durable shared seed.
    """
    f0,f1,sigma=map(F,(f0,f1,sigma))
    if not (0<=sigma<=1 and 0<=f0<=1 and 0<=f1<=1 and abs(f1-f0)<=sigma):
        raise ValueError('not an implementable prescription')
    if sigma==0:return f0,F(0),F(0)
    if sigma==1:return F(0),f0,f1
    lo=max(F(0),max(f0,f1)-sigma)
    hi=min(1-sigma,min(f0,f1))
    if lo>hi:raise AssertionError('empty constructive interval')
    r=lo/(1-sigma)
    return r,(f0-lo)/sigma,(f1-lo)/sigma
