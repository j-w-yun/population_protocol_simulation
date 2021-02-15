# population_protocol_simulation

Example configuration

```
init_config = {
	'A': 10,
	'B': 10,
	'T': 0,
}
rxns = [
	Rxn(reactants={'A': 1, 'B': 1,},
		products={'Af': 1, 'Bf': 1,}),

	Rxn(reactants={'A': 1, 'Bf': 1,},
		products={'A': 1, 'Af': 1,}),

	Rxn(reactants={'B': 1, 'Af': 1,},
		products={'B': 1, 'Bf': 1,}),

	Rxn(reactants={'Af': 1, 'Bf': 1,},
		products={'T': 2,}),

	Rxn(reactants={'A': 1, 'T': 1,},
		products={'A': 1, 'Af': 1,}),

	Rxn(reactants={'B': 1, 'T': 1,},
		products={'B': 1, 'Bf': 1,}),
]
sim = Sim(init_config, rxns)
```

Run
```
$ python simulation.py
```
