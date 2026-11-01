"""Exact, reproducible causal-cut counterexample and resource-horizon grid."""
from fractions import Fraction as F
from cdka.causal_cut import (
    CausalCutSystem, deterministic_minimal_obstructions,
    physical_configuration_bypass
)


def main():
    print("Minimal deterministic obstructions (perfect sensor, mandatory reset):")
    for sensor,reset,p in deterministic_minimal_obstructions():
        print(" sensor=",sensor,"repair=",reset,"success=",p)
    print("Memory-only vs fully observable organizational side channel:",
          physical_configuration_bypass())
    print("\nExact probability of choosing the correct viable action, rho=1/2:")
    print("n\\B",*(f"{b:>7}" for b in range(0,11)))
    for n in range(1,6):
        values=[]
        for b in range(0,11):
            s=CausalCutSystem(eta=F(0),rho=F(1,2),nu=F(0),
                              cycles=n,budget=b)
            values.append(f"{float(s.best_success()):7.3f}")
        print(f"{n:>3}",*values)
    print("All values are exact Fraction results shown as decimal approximations.")


if __name__ == "__main__":
    main()
