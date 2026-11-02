# T3.E supplement — A physical realization of the coupled policy set

The contrast constraint need not remain an unexplained mathematical restriction. A finite erasure-gated selector realizes **exactly** the family

    Phi_sigma={(f0,f1) in [0,1]^2 : |f1-f0|<=sigma}.

With probability sigma, an interface exposes the current physical register m. Otherwise it returns an erasure symbol. On readable input i, the configured local circuit chooses action 1 with probability b_i. On erasure it chooses 1 with probability r, common to both hidden inputs. No extra trace of the erased input is accessible; the flag is not retained by the final controller. All coins are fresh, not a durable policy-selection seed.

Then f_i=(1-sigma)r+sigma b_i, so |f1-f0|<=sigma automatically.

Conversely, for 0<sigma<1 choose a common mass t in

    [max(0,max(f0,f1)-sigma), min(1-sigma,min(f0,f1))].

This interval is nonempty exactly under the stated contrast and probability bounds. Set r=t/(1-sigma) and b_i=(f_i-t)/sigma. These are valid probabilities and produce the requested prescription. At sigma=0 the implementable set is the diagonal; at sigma=1 it is the full square.

Thus the diagonal-strip geometry is the exact implementability set of this physical interface, not merely an arbitrary regularizer. Both commands remain available at each readable state, but their joint selection is limited by the reliability of the interface.

The effort law sigma(w)=1-exp(-w) remains stipulated; proving a particular thermodynamic implementation would still require a calibrated physical model. This is ordinary erasure-channel algebra, not an originality claim.

Source: `cdka/selector_realization.py`. Independent exact Fraction verification enumerates all 125 (f0,f1,sigma) triples on the quarter-probability grid and checks both exclusion and constructive realization.

**Scope refinement for T4.D section 6:** take a>=0 in the displayed log-log effort schedule. Alternatively any finite inadmissible initial terms can be replaced by nonnegative values; this does not change its tail-summability result. No universal noisy-computation law is claimed.
