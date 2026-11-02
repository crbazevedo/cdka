# T4.K / T3.I — A continuation code is not a physical controller

**2026-11-02. Status:** exact finite-library synthesis and continuous-parameter certificates using known joint coding, state assignment, Bayes decision and polynomial optimization tools. Mathematical priority is **not established**. No universal agency or thermodynamic law follows.

## 1. Fixed causal frame and finite hardware library

The v6 physical plant and v9 two-epoch continuations remain byte-identical. Initial readable syndrome k=0 and physical resource balance b=4; hidden health is fair. The three equally likely diagnostic signals have healthy probabilities .01,.5,.99, exactly as in v9. The encoder sees Y once, writes a two-bit physical register, and Y is thereafter unavailable.

Before any plant action, both diagnostic bits independently flip with probability p in [0,1/2]. This transport interval affects only this register in the declared model: health/world timing, available physical observations and terminal survival event are common to all competing encoders. After this interval the **received** two-bit word is retained across the two plant epochs. No original Y, designer posterior or separate unpriced policy-tree pointer is supplied. A controller reads that word, newly observed physical (k,b) and the declared stage clock. A chosen continuation is implemented by a fixed table mapping these actual inputs to commands.

This is NOT a model of ongoing noisy rewrites or a wholly self-maintaining selector. Encoding, retention after transport and the installed lookup are ideal within a declared finite hardware library. The added register always has TWO physical cells and FOUR possible received words. 'Two used diagnostic codewords' does not mean the physical system has only two reachable memory states.

The optional joint implementation constraint is at most L installed continuation templates for the entire decoder. Independently optimizing a different arbitrary plan for every word without this cap is a relaxation. A separate funded experiment charges c(L-1) model tokens up front for L slots, leaving b=B-c(L-1) for the same plant. The fee is paid before Y; a resource residual cannot signal Y. The two latches, base selector, initial diagnostic and clock are common/sunk. This is an explicit microprogram-library contract, **not** a gate-count minimum or joule calibration.

## 2. Joint algebra: optimize encoder AND the complete decoder

Let alpha_pi(h) be v9's exact survival vector for a two-step physical continuation. Let mu_y(h)=P(Y=y,H=h), E map three Y values to words x in {00,01,10,11}, and T_p(r|x) be the binary symmetric product channel. A deterministic complete decoder D maps each received r to one continuation, with |image(D)|<=L.

    V(E,D;p) = sum_(y,h,r) mu_y(h) T_p(r|E(y)) alpha_D(r)(h).

For any finite chosen library Gamma':

    max_D V(E,D;p) = sum_r max_(pi in Gamma') sum_(y,h) mu_y(h) T_p(r|E(y)) alpha_pi(h).

The cardinality-limited optimum maximizes this expression over |Gamma'|<=L and all physical encoders E. It is NOT obtained by minimizing abstract code cardinality first and assigning labels later. A deterministic encoder/decoder suffices for the finite mean objective when the allowed maps are unrestricted apart from the declared image cap. Conditional encoder/decoder stochasticity gives a multilinear objective; sequentially replacing each stochastic map by a maximizing vertex does not decrease value. Persistent seeds, correlated programs and average-cost rather than pathwise constraints are different architectures.

## 3. Proposition K1 — exact continuation-library reduction, with a sharp scope

The 64 original v9 alpha vectors have three active upper-envelope plans:
- A=50: service now, then hold on a unanimous register or refresh on disagreement.
- B=58: service now, then refresh.
- C=42: refresh now, then refresh.

For fixed E, take any feasible decoder. Group all received words mapped to one plan pi. Their total initial-health mass is nonnegative. Replacing pi by a plan that maximizes this aggregate mass weakly improves survival. On a binary-health prior interval, some upper-envelope plan always attains that maximum. Replace each group separately. No more than the previous L different plans are needed. Therefore pruning 64 plans to A/B/C is exact **under cardinality-only, equal-price template constraints**. QED.

The designer uses aggregate health masses to compile a table; they are not runtime observations.

**Falsifier:** alpha vectors (1,0), (0,1), (.49,.49). The last is never on the unconstrained upper envelope. If the first two cost one installation token and the last costs zero, at zero budget the off-envelope plan is the only feasible one. Pruning the unpriced hull is invalid for unequal program or shared subcircuit costs. A new cost-aware envelope is required.

## 4. Proposition K2 — physical relabeling is not arbitrary permutation

At p=0 all injective encodings preserve Y. At p>0, transitions depend on Hamming distance:

    T_p(r|x) = p^d_H(x,r) (1-p)^(2-d_H(x,r)).

Any simultaneous XOR translation or coordinate permutation is a symmetry of this channel. An arbitrary permutation of the four abstract state labels need not be. Decoder relabeling preserves value only if the whole channel and implementation constraints transform covariantly.

At p=.01 the best decoder for E=(00,01,10) gives .8191473791341661; for E=(00,01,11) it gives .8198838467360139. Both preserve all three signals noiselessly and use the SAME two cells and physical plant. Label geometry alone changes the achievable value.

This is a state-assignment/joint source-channel phenomenon, not a new general principle.

## 5. Proposition K3 — global phase diagram, certified on the continuum

With b=4, freely installed up to three templates, and the declared sensor, the optimum over all 4^3 encoders and 3^4 decoders is the upper envelope of three quadratics:

    V_A(p) = .8206900304121558 - .0800481277297360 p - .0570239884454699 p^2
    V_B(p) = .8204089133546236 - .0224619051692019 p - .1512308737274672 p^2
    V_C(p) = .8091779607700227.

Decimals above are presentation only. All coefficients are exact rational numbers in `joint-compilation-certificate.json` and the Python generator.

Witnesses (received-word order 00,01,10,11):

| Regime | Encoder for low/mid/high signals | Decoder | Distinctions used |
|---|---|---|---|
| very low noise | (00,01,11) | (A,B,B,C) | three diagnostic classes, three plans |
| intermediate noise | (00,00,11) | (B,B,B,C) | two classes, two plans |
| high noise | constant | (B,B,B,B) | no diagnostic distinction used |

Let p1 be the smaller root of V_A-V_B and p2 the positive root of V_B-V_C. Then

    p1 = .004921292856323312...   (about .492129% per bit)
    p2 = .2081876270782522...     (about 20.818763% per bit).

V*=V_A on [0,p1], V_B on [p1,p2], V_C on [p2,1/2], with ties at the boundaries. For each interval an attaining physical encoder/table is exhibited.

**Continuum certificate.** Every encoder/table gives a quadratic because there are two binary faults. There are 5,184 joint deterministic assignments, yielding 486 distinct rational coefficient triples. For each phase curve, subtract every competitor and check nonnegativity on the relevant interval: check both endpoints and, for a convex quadratic with an interior vertex, its vertex. Endpoints are quadratic surds; all signs and rational comparisons are computed exactly by squaring with sign checks. Thus 1,458 interval inequalities certify the complete [0,1/2] domain; a plotted grid is NOT the proof. Combined with K1 this covers the original 64-plan library under its stated pricing.

## 6. A lossy distinction can protect more valuable distinctions

At p=.10, the globally best noninjective encoder gives .8166504141004288 survival; the best of **all injective encoders** gives .8126175908010297. The improvement is .40328232994 percentage point, not a universal large engineering effect.

The noninjective register carries about .67838 bit of mutual information I(Y;received word), while the best injective design carries about .88604 bit. More mutual information about Y does not guarantee higher task survival. This is not a violation of data processing: two different physical encoders induce generally incomparable information experiments. No extra bit noise is being advertised as beneficial; the optimized value is nonincreasing with p in the tested family and the certified envelope.

The word pair 00/11 has Hamming distance two. It does NOT correct every single-bit error: 01 and 10 are ambiguous. The task decoder maps ambiguous words to plan B because of its asymmetric continuation losses. Do not describe this as a universal one-error-correcting code.

## 7. A program's installation competes with operating resources

With total B=4 and one token per extra installed template slot, paid before observing Y:

| Slots provisioned | Installation fee | Balance for physical operation | Best zero-noise survival |
|---:|---:|---:|---:|
| 1 | 0 | 4 | .8091779607700227 |
| 2 | 1 | 3 | .8204089133546236 |
| 3 | 2 | 2 | .8009990604815288 |

The joint optimum provisions two slots even at p=0. Provisioning three does not force all three to be used; an unused purchased slot still consumes its fee. With b=2, costly first actions leave insufficient balance for some second refreshes. The value reduction is computed through the SAME v6 pathwise resource law, not an arbitrary utility penalty after optimization.

This is NOT the claim that additional optional hardware lowers an optimized value. The controller may select the smaller program. It is a counterexample to 'install the unconstrained exact-memory solution first, then pay its resource cost'. It also does not establish universal program prices. Cheap alternative circuitry could change this table; the cost contract must be derived for a physical implementation before interpreting it beyond this library.

## 8. Analysis and next proof obligation

At p=0, the noise-free three-class advantage is .0002811170575321. Its derivative is about -.0800481 versus -.0224619 for the two-class protected distinction. Balancing the initial value gain with these sensitivities predicts a small crossing; the exact quadratic root provides the certificate. Differentiation is for fixed programs; the optimized envelope has kinks at switches.

Executed: joint deterministic encoder, actual noisy state transition, complete continuation decoder, global template cap, pre-observation installation and exact physical event. Not executed: repeated uncertain memory updating, unequal gate-level program costs, evolving selector health or charged retention/clock primitives. No original theory of agency has been proved.

The next theorem must characterize a cost-aware, recursively updateable interface under a **nonseparable physical circuit library**. Use the present optimum as a small oracle. If the statement is only standard real-time source-channel coding or FSM state assignment, preserve it as an instrument and audit the unresolved physical restriction before adding another component.

## 9. Prior-art map

- Walrand & Varaiya, *Optimal Causal Coding-Decoding Problems*, Berkeley UCB/ERL M82/3 (1982), later IEEE TIT (1983). Causal source/channel coding and decoding through noisy memoryless channels already form a developed theory. [Institutional record](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1982/28518.html). This increment does not claim their subject as new.
- De Micheli, Brayton & Sangiovanni-Vincentelli, *Optimal State Assignment for Finite State Machines*, IEEE TCAD (1985). Encoding affects implementation, and symbolic minimization/state assignment are linked. [Institutional abstract](https://research.ibm.com/publications/optimal-state-assignment-for-finite-state-machines). Full theorem equivalence audit not performed here.
- Poupart & Boutilier, *Value-directed Compression of POMDPs* (2002). [Author abstract](https://www.cs.toronto.edu/~cebly/Papers/vdib-abs.html). v9 continuation compression remains a known foundational instrument.
- Junges et al., *Finite-State Controllers of POMDPs using Parameter Synthesis* (2018). [Primary proceedings](https://proceedings.mlr.press/r16/junges18a.html). Needed for recurrent joint synthesis, not displaced by this finite example.

Primary records/abstracts inspected; no exhaustive novelty claim. Source: `cdka/joint_compilation.py`; independent tests: `tests/test_joint_compilation.py`; exact certificates: `python -m experiments.joint_compilation_sweep`.
