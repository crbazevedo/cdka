# CDKA — Catálogo de hipóteses, instrumentos e alternativas v7

**Fonte canônica:** [`research-options.json`](research-options.json). Atualização v7: **37 abordagens, 18 simplificações rejeitadas e apenas dois ramos ativos (R11/R14)**. Esta taxonomia é o registro das alternativas identificadas no programa, não um levantamento bibliográfico exaustivo.

Cada item preserva hipótese, estado, gatilho de reativação, teste mínimo, instrumentos, critério de saída, alternativas, proveniência e classificação de novidade. Não confundir uma abordagem estacionada com uma abordagem refutada.

## Mapa de retomada

| ID | Abordagem | Estado | Gatilho para retomada | Alternativas |
|---|---|---|---|---|
| R01 | Causal frame | validated_scope | Counterfactual comparison changes its initial equilibrium or failure set | R05, R20 |
| R02 | Action sufficiency | instrument | A new task requires a minimal deterministic decision representation | R03, R23 |
| R03 | Soft decision information | parked | Nonzero mistakes or nonuniform context priors are admitted | R04, R17 |
| R04 | Rare-event epistemic reliability | instrument | Mean accuracy masks catastrophic small-noise effects | R08, R27 |
| R05 | Finite-time physical action | instrument | Physical repair/sensing operation needs a calibrated failure law | R06, R07 |
| R06 | Critical scaling | parked | Direct numerical rates fail near a critical parameter | R07, R27 |
| R07 | Higher-dimensional variational fallback | parked | One-dimensional quadrature no longer applies | R05, R27 |
| R08 | Correlated substrate noise | instrument | Independence gives implausible redundancy or joint benefit | R29, R30 |
| R09 | Fallible corrector upkeep | validated_scope | An otherwise safe code relies on an ideal corrector | R11, R18 |
| R10 | Changing world / stale memory | validated_scope | Static-context results are mistaken for continuing knowledge | R22, R11 |
| R11 | Hidden health and paid diagnostics | active | Readable health is the remaining idealized interface | R14, R28 |
| R12 | Approximate compositional certificate | validated_scope | Exact symmetry breaks but calibrated row error is uniformly small | R13, R29 |
| R13 | Exact readable quotient | validated_scope | Microstate enumeration becomes large or a proposed statistic may hide W | R12, R23 |
| R14 | Coupled implementation costs | active | A rowwise optimization invents a common physical selector | R15, R28 |
| R15 | Physical action/resource signaling | instrument | A no-go claims all information was erased | R11, R14 |
| R16 | Persistent versus fresh randomness | instrument | Convexifying policies improves a robust objective | R17, R14 |
| R17 | Profiles and survivor mass | instrument | Good aggregate metric accompanies collapse in some contexts | R18, R21 |
| R18 | Support and spectral lifetime | instrument | Positive life extension is interpreted as infinite safety | R19, R30 |
| R19 | Switching and coordination | parked | A mode-by-mode spectral no-go is used for a switching controller | R14, R18 |
| R20 | Financed reconfiguration | instrument | A safe component is assumed available at time zero | R09, R14 |
| R21 | Finite design versus indefinite policy | instrument | Leading budget asymptotics are claimed to imply indefinite viability | R18, R27 |
| R22 | Active sensing / dual control | parked | Passive refresh lacks strategic information value | R11, R14 |
| R23 | Dynamic compatibility topology | parked | Aggregation merges three or more contexts | R02, R13 |
| R24 | Replicator / evolutionary memory | parked | A regulatory mechanism library is allowed to reproduce or reweight | R25, R26 |
| R25 | Semantic information and purpose | parked | Ontological claims exceed the finite control contract | R26, R17 |
| R26 | Autonomy / external replay | parked | A controller is called autonomous because behavior looks intelligent | R09, R25 |
| R27 | Physical calibration / thermodynamics | parked | Dimensionless reliability law is given a physical interpretation | R05, R08 |
| R28 | Formal scalable synthesis | parked | Exact controller enumeration exhausts feasible small models | R13, R14 |
| R29 | Nonrectangular uncertainty | queued | Robust local composition becomes unnecessarily pessimistic | R12, R08 |
| R30 | Nonfatal errors and redundancy | instrument | n log n or positive-hazard no-go is stated universally | R09, R18 |
| R31 | Unifying objectives as competitors | parked | A universal scalar is proposed to replace causal distinctions | R25, R26 |
| R32 | Oscillators and continuous agency models | parked | Finite structural result survives but requires physical realization | R05, R24 |
| R33 | Costed health diagnosis value and critical accuracy | validated_scope | A new organization has different action payoffs, priors or diagnostic risk | R11, R14, R17 |
| R34 | Temporal relevance of organizational diagnosis | validated_scope | Diagnostic-to-actuation delay, changing health or deadline appears | R10, R11, R22 |
| R35 | Budget/outcome traces as covert information channels | queued | A policy impossibility follows from only examining the diagnostic register | R15, R14, R11 |
| R36 | Hidden-health stage-dependent finite-memory control | validated_scope | Removing a health flag or other designer-only state from the physical interface | R11, R13, R12 |
| R37 | Deteriorating meta-selector and program library costs | queued | A multi-period control proof assumes the contingent selector is permanently reliable | R14, R20, R28 |

## Simplificações rejeitadas

| ID | Afirmação que não deve reaparecer sem hipóteses adicionais | Por quê | Rotas |
|---|---|---|---|
| D01 | Changing the initial equilibrium while comparing actions | Refuted as a causal comparison, valid only as a separate equilibrated parameter scan | R01, R05 |
| D02 | Safe-action compatibility is determined pairwise | Three-way intersections can be empty despite every pair overlapping | R02, R23 |
| D03 | One initial bit suffices forever | Repair can erase it; world changes can make a retained bit obsolete | R09, R10 |
| D04 | Every fixed repair erases information, so any feedback erases it | Action-dependent mode selection can transport a bit | R15, R14 |
| D05 | High accuracy among survivors implies organizational viability | Conditioning discards failure mass | R17 |
| D06 | All randomization convexifies physical policies for free | Persistent policy coordination requires physical storage | R16 |
| D07 | Uniform resource allocation is always optimal | Complementarity creates a convex scarcity regime | R14, R21 |
| D08 | Finite-horizon n log n cost determines indefinite survival | Lower-order terms and causal resource timing remain decisive | R21 |
| D09 | Local error marginals determine task failure | Coupling and task event alter error cancellation and common-mode failures | R08 |
| D10 | Transient isolated modes imply every coordinated system fails | Mode products can preserve a safe cycle | R19 |
| D11 | Install a better architecture at the earliest feasible instant | Risk paid during funding can favor a later installation | R20 |
| D12 | A bounded-fault code proves safety with arbitrary thermal noise | Tiny uncorrectable support changes infinite-horizon guarantees | R18, R27 |
| D13 | Count-only quotient remains exact with arbitrary cell qualities | Current counterexample has same disagreement count but row-TV difference 513619/2000000 | R13, R12 |
| D14 | A coarse approximation with small one-step error proves indefinite safety | The finite-horizon coupling bound saturates and says nothing by itself about support | R12, R18 |
| D15 | A designer-sufficient quotient remains a runtime signal after hiding health | (k,h,b) is an exact v6 mathematical quotient; h becomes hidden in v7, leaving only (k,b) readable and a strict value gap | R36, R11, R13 |
| D16 | A perfect diagnostic necessarily improves achievable physical control | The contingent policy requires both a funded selector and an affordable action; B=3 v7 has perfect diagnosis but zero gain | R33, R14, R35 |
| D17 | One bit of diagnosis remains equally useful after a physical delay | Health drift attenuates the observation-to-action correlation and crosses a critical decision threshold | R34, R10, R22 |
| D18 | A useful diagnostic cannot reduce survival | Even a perfect measurement may carry procedure failure; with zeta >= 0.02817661 in the stated fixture its net value is zero | R33, R11, R17 |

## Procedimento obrigatório diante de um dead-end

1. Congelar o estado físico inicial, a autoridade de intervenção, o evento de falha e o prazo da hipótese avaliada.
2. Identificar a categoria: contradição, erro de implementação, ausência de interface física, deficiência de prova, limite numérico, certificado vazio, anterioridade equivalente ou falta de poder explicativo.
3. Preservar prova, contraexemplo e dados. Não apagar resultados negativos.
4. Ativar a alternativa cujo **gatilho** seja satisfeito, não a que seja visualmente mais interessante. Executar o teste mínimo declarado antes de expandir o modelo.
5. Após dois exemplos sucessivos sem novo enunciado matemático, suspender expansão de modelos e auditar literatura / independência dos pressupostos.

O programa mantém como frentes ativas R11 (saúde oculta, diagnóstico pago e memória física) e R14 (biblioteca de seletores e custo conjunto). R24 (replicador), R27 (calibração físico-termodinâmica) e R32 (osciladores) permanecem preservados com gatilhos de retomada.
