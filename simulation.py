# Jaewan Yun <jaeyun@ucdavis.edu>

import random


class Species:
	def __init__(self, label):
		self.label = label

	def __hash__(self):
		return hash(tuple(sorted(self.__dict__.items())))

	def __eq__(self, other):
		if isinstance(other, Species):
			return self.label == other.label
		return False


class Rxn:
	def __init__(self, reactants, products):
		# Convert to species object if string provided
		self.reactants = {}
		for k, v in reactants.items():
			if not isinstance(k, Species):
				self.reactants[Species(k)] = v
			else:
				self.reactants[k] = v
		self.products = {}
		for k, v in products.items():
			if not isinstance(k, Species):
				self.products[Species(k)] = v
			else:
				self.products[k] = v

	def __str__(self):
		reactants = []
		products = []
		for k, v in self.reactants.items():
			reactants.append('{} {}'.format(v, k.label))
		for k, v in self.products.items():
			products.append('{} {}'.format(v, k.label))
		products = products or ['0']
		return '{} -> {}'.format(' + '.join(reactants), ' + '.join(products))


class Sim:
	def __init__(self, species, rxns):
		# Convert to species object if string provided
		self.species = {}
		for k, v in species.items():
			if not isinstance(k, Species):
				self.species[Species(k)] = v
			else:
				self.species[k] = v
		self.rxns = rxns

	def __str__(self):
		species_str = []
		for k, v in self.species.items():
			species_str.append('{}: {}'.format(k.label, str(v).ljust(4)))
		return '\n'.join(species_str)

	def size(self):
		t = 0
		for _, v in self.species.items():
			t += v
		return t

	def sample(self):
		rand = random.randint(0, self.size()-1)
		n = 0
		for k, v in self.species.items():
			n += v
			if n > rand:
				return k

	def step(self):
		a, b = self.sample(), self.sample()
		if a == b:
			return None

		for rxn in self.rxns:
			if (a in rxn.reactants and
				b in rxn.reactants and
				self.species[a] >= rxn.reactants[a] and
				self.species[b] >= rxn.reactants[b]):

				# Decrease reactants by reaction stoichiometry
				self.species[a] -= rxn.reactants[a]
				self.species[b] -= rxn.reactants[b]

				# Increase products by reaction stoichiometry
				for k, v in rxn.products.items():
					if k not in self.species:
						self.species[k] = 0
					self.species[k] += v

				return rxn
		return None


def main():
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

	max_steps = 1000
	for i in range(max_steps):
		rxn = sim.step()
		if rxn is not None:
			print('\nReaction {}: {}'.format(i, rxn))
			print(sim)

	print('\vSimulation complete')
	print(sim)

if __name__ == "__main__":
	main()
