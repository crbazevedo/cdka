# E-recurrent-v16 — frozen library, exact recurrent law and internal traces

2026-11-05. New recurrent benchmark; v15 physical voter inherited. Do not compare its survival numbers to v15's terminal task.

## Reproduction

```sh
python -m unittest discover -s tests -p 'test_recurrent*.py' -v
python -m experiments.recurrent_sweep --write --check
node --test tests/recurrent-lab.test.mjs
```

The common baseline model is defined in `Model`. The16 stationary programs are frozen before ranking. The eight-cycle separating target beta=.915 is illustrative and chosen after observing the exact gap, not preregistered.

## Actual local verification

17 scientific Python tests plus one research-memory test, seven JS tests.192 independent raw microkernel rows;192 exact policy/phase factorization identities;2048 scalar task gate/sensor-mask cases;16 programs and4 blind baselines. The certificate contains116 complete conditional branch rows for four physical sources. It is generated from the exact code rather than hand-edited.

Mean eight-cycle survival: diagnostic .9174767896493894; best blind .9115317652171799; no service .7325971487141393. Expected service attempts1.2734000271470125 versus3.850739034520345. Conditional health outcomes, costs, failure masses and uninformative-diagnostic controls are retained.

The exact evaluator dimension is12 phases versus64 microstates. This is stochastic renewal, not a physically observable health partition. No runtime claim is made from counting fewer states; model construction and arithmetic costs remain separate.

## Visual verification

Local standalone bytes rendered in Chromium with Playwright set_content at1440×1100 and390×844. Seven controls, three panels, two SVGs; no JavaScript exception or horizontal overflow. These are offline checks, not independent navigation to the published GitHub Pages address.

GitHub CI tests the canonical checkout independently. Historical uploaded source copies were used only to reconstruct a local dependency runtime when external cloning was unavailable; the new voter table is checked directly against `cdka.boundary_voting` in the repository suite.
