# T3.F — Local error rates do not specify an organizational failure law

**Status:** exact derivations and counterexamples using classical coupling and coding theory. No originality claim. This tests the independence behind v4, keeping the logical task fixed within each comparison.

## 1. Correlated cascaded errors

A binary input W passes through XOR errors E1,E2. Write a=P(E1=1), b=P(E2=1), t=P(E1=E2=1). Their joint probabilities are:

| Errors | Probability |
|---|---:|
| 0,0 | 1-a-b+t |
| 1,0 | a-t |
| 0,1 | b-t |
| 1,1 | t |

Nonnegativity gives max(0,a+b-1)<=t<=min(a,b). Final command U=W XOR E1 XOR E2 therefore has

    P(U!=W)=a+b-2t,
    |a-b|<=P(U!=W)<=min(a+b,2-a-b).

For equal marginal errors a=b=.1, independent errors give .18, perfectly shared flips give zero final error, and mutually exclusive flips give .20. This concerns final logical correctness, not the absence of internal faults. The different event 'any component fault is fatal' instead has probability a+b-t.

The joint law and the task are essential; a common substrate is not universally beneficial.

## 2. Correlation can erase a redundancy advantage

Encode W as (W,W,W) and decode the corrupted register by majority. Independent bit flips with probability p give logical failure 3p^2-2p^3. If all bits flip together with probability p, their individual marginal error is unchanged, but logical failure is p. At p=.1, those values are .028 and .1.

The architecture's failure law requires the joint noise law AND the physical decoding operation. The corrector and terminal actuator here are ideal within the declared fault model. No thermodynamic conclusion about an actually perfect corrector is being claimed.

## 3. Changing the safe support, under bounded faults

Suppose each epoch flips at most one of the three physical bits. Noise may have strictly positive probability, but majority always recovers W. Rewriting the codeword creates the closed post-correction set

    G={(W=0,register=000),(W=1,register=111)}.

No new observation of W is supplied. The mechanism reads the register. The decoder/rewrite circuit and its maintenance must be counted as part of the physical organization.

Two binary codewords correct every radius-one error iff their Hamming distance is at least three. No register shorter than three bits can have that distance; repetition of a single logical bit in three cells attains it. This is classical coding theory, not a new CDKA theorem. Two added writable cells are a storage lower bound, not the total installation/maintenance cost.

### Structural fragility

With independent p>0, weight-two and weight-three masks regain positive probability. G is no longer non-killing. An arbitrarily small uncorrectable probability changes the infinite-horizon support certificate, although finite-horizon survival is continuous. For a fixed logical error delta:

    lim_(delta->0) lim_(n->infinity) (1-delta)^n = 0,
    lim_(n->infinity) lim_(delta->0) (1-delta)^n = 1.

A bounded-fault certificate is NOT an immortality result under full-support thermal diffusion.

## 4. Strategic payoff

Use a coupling polytope before optimizing reliability. Separate component faults, incorrect representations, wrong commands and absorbing organizational failure. Determine whether reconfiguration only lowers transition probabilities or removes every failure edge from a reachable controlled set. Treat ideal correction as an explicit boundary to be relaxed.

The earlier n log n budget law remains valid for its fixed fatal-error architecture. It is not a lower bound on all error-correcting organizations.

## 5. Verification and antecedents

165 rational joint error laws on a denominator-eight grid, exact bit-mask enumeration and support collisions for one-, two- and three-bit repetition registers are checked in `tests/test_reconfiguration.py`. Numerical tests do not establish novelty.

- Hamming (1950): https://doi.org/10.1002/j.1538-7305.1950.tb00463.x
- Institutional original record: https://www.nokia.com/bell-labs/publications-and-media/publications/error-detecting-and-error-correcting-codes/
- Finite-state controller synthesis: https://proceedings.mlr.press/r16/junges18a.html
