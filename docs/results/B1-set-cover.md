# B1 — Minimum action-sufficient fixed code (known baseline)

**Status:** proven elementary lemma / anticipated directly by prior art (Murray 2026). **Not original.**

Let W and A be finite. Let R⊆W×A mean "a is an acceptable one-shot action in w". Assume every world has at least one acceptable action, the current world can be observed without error before encoding, encoding and decoding are deterministic, and a single action is selected.

For each a define W_a={w∈W:R(w,a)}. Let k be the smallest number of internal messages necessary to guarantee success for every w.

**Proposition.**
\[
k=\min\{|B|:B\subseteq A,\ \cup_{a\in B}W_a=W\}.
\]

**Proof.** Any k-message decoder emits at most k distinct actions; these must cover all worlds, since the encoder guarantees a safe decoder output for each world. Conversely, a cover of size k gives a code that maps each w to a covering action and a decoder that executes that action. Hence equality.

**Corollary.** Worst-case fixed-width storage is \`ceil(log2 k)\` bits for k≥1, not generally \`I(W;M)=log2 k\`. If no actions cover the worlds, the task is infeasible. The empty-world convention is k=0, requiring zero bits.

**Higher-order compatibility.** For {A:{1,2}, B:{2,3}, C:{1,3}}, every pair shares an admissible action, but the triple has empty intersection. Thus pairwise conflict graphs do not characterize action sufficiency; the Dowker complex does.

**Verification.** \`python -m unittest discover -s tests -v\` independently checks all 512 binary 3×3 relations against partition enumeration. This is computational verification of finite cases, not a substitute for the proof.
