# population_protocol_simulation

Example configuration

```
init_config = {
	Species('A'): 10,
	Species('B'): 10,
	Species('T'): 0,
}
rxns = [
	Rxn(reactants={
			Species('A'): 1,
			Species('B'): 1,
		},
		products={
			Species('Af'): 1,
			Species('Bf'): 1,
		}),

	Rxn(reactants={
			Species('A'): 1,
			Species('Bf'): 1,
		},
		products={
			Species('A'): 1,
			Species('Af'): 1,
		}),

	Rxn(reactants={
			Species('B'): 1,
			Species('Af'): 1,
		},
		products={
			Species('B'): 1,
			Species('Bf'): 1,
		}),

	Rxn(reactants={
			Species('Af'): 1,
			Species('Bf'): 1,
		},
		products={
			Species('T'): 1,
			Species('T'): 1,
		}),

	Rxn(reactants={
			Species('A'): 1,
			Species('T'): 1,
		},
		products={
			Species('A'): 1,
			Species('Af'): 1,
		}),

	Rxn(reactants={
			Species('B'): 1,
			Species('T'): 1,
		},
		products={
			Species('B'): 1,
			Species('Bf'): 1,
		}),

]
sim = Sim(init_config, rxns)
```