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
		self.reactants = reactants
		self.products = products

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
		self.species = species
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
