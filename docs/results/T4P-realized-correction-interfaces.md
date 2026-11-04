# T4.P / T3.L — Realized correction changes the sufficient interface

**2026-11-04 · CDKA v15.** Executed contribution: a construction and falsification method connecting physical voting topology, exact stochastic boundary reduction over successive updates, and costed corrective maintenance in the unchanged v13/v14 terminal task. The probability/lumping instruments are established; the implementation-relative certificate, strict context witness and comparative resource result are concrete adaptations.

## 1. Two linked experiments, not an undeclared larger agent

**Portfolio:** the same SERVICE-first plant, three equally likely initial diagnostics, hidden health, terminal HOLD/REFRESH, deadline and failure event. Nominal encoding is (11,00,00). The same four-gate sequential selector is used. Its replicas read the SAME received cells and syndrome: internal faults are independent conditional on that actual input, not independent unconditional diagnoses.

**Boundary:** a separate register-level grammar tests two successive updates of three stored command bits under persistent hidden substrate mode Z. It does not solve two new full plant epochs. It uses the same concrete six-NAND voter. Evaluator knowledge of Z is not a runtime observation.

## 2. Ideal majority symmetry is not physical stochastic symmetry

Inputs a,b,c are wires0,1,2. The installed voter is:

    n0=NAND(a,b); n1=NAND(a,c); n2=NAND(b,c)
    n3=NAND(n0,n1); n4=NAND(n3,n3); out=NAND(n2,n4).

Each NAND independently flips its physical output with probability gamma; fanout reuses the SAME signal. Wires, constants and routing retain the common idealizations of v14. With no faults this computes majority.

Exact expansion of all64 fault masks gives:

    f_gamma(011)-f_gamma(101)=2 gamma(1-gamma)(1-2 gamma)^2.

Its coefficient vector is (0,2,-10,16,-8,0,0), verified exactly, not fitted from samples. It is positive for0<gamma<1/2. The implemented circuit treats a differently from b,c. Interchanging b,c only swaps identically distributed internal faults, so that smaller symmetry remains valid.

## 3. A sufficient boundary for successive updates

Full state (Z,a,b,c) has16 possibilities. Z determines per-gate error .001 or .02. Healthy degrades with probability1/20 after an update; degraded stays degraded. These are explicit model calibrations.

Allowed operations:
- DIFFUSE: independently flip each cell with probability e.
- REGENERATE: run the actual voter, broadcast its noisy output and write three cells with independent write error e. The common voted bit correlates the written cells.

After each operation, hidden health changes according to the declared transition. For both operations, the12-state signature

    C=(Z,a,b+c)

admits exact independently constructed quotient kernels satisfying K L=L Kbar.

**Proof:** the primitive kernels are equivariant under b↔c. Transition masses to the orbits coincide. The algebraic oracle uses a one-bit channel for a and binomial convolutions for b+c. Regeneration mixes first over the actual voted output, then performs writes, preserving their common cause. Sum over the health transition. Induction proves all permitted finite compositions, including both-update sequences. QED.

The law can contain arbitrary dependence between Z and the register. The reduced law preserves it. This is a stochastic evaluator interface, not a free readable health flag or a physical-memory bit count.

### The tempting smaller quotient fails

For an abstract symmetric majority followed by one symmetric output flip, (Z,a+b+c) would give an exact eight-state quotient. For the actual voter, degraded registers011 and101 have the same count but different aggregate continuation laws. Their total variation is .03604117192704 after one regeneration and .03115580218128438 after two.

Registers000 with healthy versus degraded Z have identical current visible states. Discarding Z yields different next bit laws, with TV=.10419182986230009. Present visible marginals cannot replace a persistent future-noise source.

Independent stable-partition refinement finds8 classes for the symmetric primitive,12 for the actual grammar. Their invariant response-space ranks are5 and10 respectively. The physical rank profile is2→4→7→9→10→10. These statements concern the fixed rational fixture; changing rates or primitives requires recertification.

## 4. Paid correction and a fair alternative

For a selector output probability r_x conditional on actual input x, three physically independent modules have joint probability r_x^k(1-r_x)^(3-k). The real voter produces

    T_v(r)=sum_bits f_v(bits) r^(number of ones)(1-r)^(number of zeros).

Only at v=0 does this become3r²−2r³. Three selector copies cost12 NANDs and the voter costs6:18 installed gates. Fanning out one selector output instead costs10 gates total but supplies the correlated law P(000)=1-r,P(111)=r, not three independent samples.

One paid maintenance action services ONE bank: either the four-gate selector or six-gate voter. With probability s it sets that bank's error to gamma_low; otherwise the bank remains at gamma_high. The result is hidden. The operation costs one of the three resource tokens remaining after initial SERVICE, leaving two, so HOLD and REFRESH remain affordable. It fits the declared pre-command interval and has no fatal procedure risk in the principal fixture. When procedure failure is introduced, ALL survival mass is multiplied by its success probability.

Bank-service prices are a declared library contract, not a universal energy law. We compare a fixed portfolio, not every18-gate design.

For p=.01, degraded gates=.02, restored gates=.001 and maintenance success=.8:

| Design | NAND capacity | Bank services | Survival |
|---|---:|---:|---:|
| Common trusted fixed REFRESH bypass |0 adjustable|0|.8091779607700227|
| Single sequential selector |4|0|.8089390485441446|
| Single selector, maintained |4|1|**.8093283371516880**|
| Triplicated selectors + voter |18|0|.8088541412374230|
| Triplicated, voter maintained |18|1|**.8092776292466612**|
| One selector output fanned into voter |10|0|.8085015416408805|

Voter maintenance restores a useful redundant design. Maintaining the simpler selector is both smaller and better in this fixture. The bypass's0 is adjustable gate cost, not a claim that a physical organism has no infrastructure.

## 5. Exact thresholds and interval certificate

V(s)=V_bad+s(V_good−V_bad). If the slope is positive, improvement over the bypass begins at

    s_critical=(V_ref−V_bad)/(V_good−V_bad).

The exact thresholds in the fixed fixture are .4909719344438053 for selector service and .6117189163059938 for voter service.

At s=0 and s=1, selector service exceeds voter service by .00008490730672148528 and .00004215805460313470. Their difference is affine, proving dominance for EVERY s∈[0,1], not only grid points. Other noise rates, tasks or service prices require new analysis.

A maintained bank is a mixture of JOINT conditional gate laws, not independent gates operating at the mean error. Replacing the hidden mode by average error .0048 gives .8092786610665256 instead of .8092776292466612. The numerical gap is small; the claimed equality is false because marginalizing a persistent common cause creates dependencies.

## 6. The last-port bound remains intact

At uniform gate error .02, the v14 last-port bound rules out beating the bypass under its independent single-output contract, regardless of upstream redundancy. A same-technology voter merely creates another last faulty gate. Maintenance changes that gate bank's physical law; conditional bounds can be mixed by the service-success probability. This is not a counterexample to the bound.

## 7. Contribution and scope

The correction circuit determines which distinctions the stochastic boundary must preserve. Resource allocation can favor maintenance of an existing interface over installing more copies. The executed package provides exact reduction, an algebraic topology witness, two-update certificates, complete fault traces and an affordable attaining maintenance policy in a declared portfolio.

The register and portfolio studies share the same voter but are not yet one jointly optimized recurrent agent. Routing, diagnostics and maintenance selection retain explicit idealizations. No general agency, thermodynamic cost or global18-gate optimality is claimed.

## 8. Evidence

17 scientific Python tests plus one additive catalog test; seven JS tests. Independent raw voter execution2048 mask/input cases; replica/voter raw oracle2560 cases; quotient192 rows; two-update384 compositions;128 complete conditional traces. Polynomial equality checked coefficientwise; continuous maintenance dominance by exact affine endpoints. Values use Fraction arithmetic.

Run `python -m unittest discover -s tests -p 'test_boundary*.py' -v`, `python -m experiments.boundary_voting_sweep --write --check`, `node --test tests/boundary-voting-lab.test.mjs`.

## 9. Predecessors and next gate

Probabilistic transfer matrices: https://ieee-ceda.org/media/accurate-reliability-evaluation-and-enhancement-probabilistic-transfer-matrices .
Buchholz, Exact and ordinary lumpability in finite Markov chains,1994: https://doi.org/10.2307/3215235 .
Banisch & Lima, symmetry-based aggregation: https://arxiv.org/abs/1209.3902 .
Fault-tolerant voters: https://doi.org/10.3390/electronics8030332 .

Next: one small recurrent process with hidden selector/corrector health, an actually updated memory and paid selection of maintenance. Reuse the certified boundary to keep the problem finite. Produce a strict compositional viability statement or a smallest implementability failure before expanding further.
