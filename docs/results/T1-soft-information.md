# T1.B — Hard decision codes versus soft information–risk trade-offs

**Status:** known binary rate–distortion theorem; applied as a counterexample to careless interpretations of CDKA information thresholds.

## Why

The 0-bit/1-bit discontinuity in T1 is a *zero-error, deterministic, fixed-width code* phenomenon. It must not be presented as a universal discontinuity in Shannon mutual information or as the emergence of a physical memory module.

In the middle regime of T1, the two equally probable hidden states \(W\in\{-1,+1\}\) require opposite corrective actions. Suppose a stochastic controller is allowed to choose the wrong action with probability \(\delta\).

When the distortion is Hamming loss \(d(w,a)=1\{a\text{ incorrect for }w\}\), the classical binary source rate–distortion formula gives
\[
\boxed{R(\delta)=\min_{p(a|w):P(\mathrm{error})\le\delta}I(W;A)
=\begin{cases}1-h_2(\delta),&0\le\delta\le1/2,\\0,&\delta>1/2.\end{cases}}
\]
Because we may choose the message \(M=A\) for a one-shot encoder/decoder, data processing makes this also the minimal \(I(W;M)\) under the assumed perfect input observation and lack of other constraints.

At \(\delta=0\), one bit is necessary. At \(\delta=0.1\), the minimum is about \(0.5310\) bits; at \(\delta=1/2\), zero. A deterministic fixed code with no error remains one bit throughout.

This distinction makes sense only once we declare what "information budget" measures: number of distinct codewords, fixed-width storage, expected description length, Shannon mutual information, or physical memory/measurement cost. These are not interchangeable.

## Consequence for strategy

The static set-cover problem B1 is the exact robust baseline. A rate-distortion/Blahut–Arimoto formulation should be used when the admissible failure rate is nonzero. In a dynamically changing system, one must also specify *when* measurement arrives and whether risk is average, worst-case per context, or cumulative over time.

**Research status:** no novelty claimed. Tool: Shannon rate–distortion and its causal / sequential variants for future T3/T4 analyses.
