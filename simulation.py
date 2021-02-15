# Jaewan Yun <jaeyun@ucdavis.edu>

import matplotlib.pyplot as plt
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

	def count_all(self):
		species = {}
		for rxn in self.rxns:
			for k in rxn.reactants:
				species[k] = 0
			for k in rxn.products:
				species[k] = 0
		for k, v in self.species.items():
			species[k] = v
		return species

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
	max_steps = 200000
	init_config = {
		'A': 101,
		'B': 100,
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
			products={'T': 1,}),

		Rxn(reactants={'A': 1, 'T': 1,},
			products={'A': 1, 'Af': 1,}),

		Rxn(reactants={'B': 1, 'T': 1,},
			products={'B': 1, 'Bf': 1,}),
	]
	sim = Sim(init_config, rxns)

	plot_x = [];
	plot_y = {k: [] for k in sim.count_all()}

	for i in range(max_steps):
		# Run one step
		rxn = sim.step()
		if rxn is not None:
			print('\nReaction {}: {}'.format(i, rxn))
			print(sim)

		# Log species count
		plot_x.append(i)
		for k, v in sim.count_all().items():
			plot_y[k].append(v)

	print('\vSimulation complete')
	print(sim)

	# Cut plot data to time that y changed last
	last_x = 0
	for k, v in plot_y.items():
		for x, y in enumerate(v):
			if y != v[-1] and x > last_x:
				last_x = x
	# Padding
	last_x = min(last_x+1, len(plot_x))

	# Render plot
	fig, ax = plt.subplots()
	for k, v in plot_y.items():
		ax.plot(plot_x[:last_x], v[:last_x], label=k.label)
	plt.legend()

	plt.xlabel('Simulation Step', fontsize=18)
	plt.ylabel('Species Count', fontsize=16)
	fig.savefig('out.jpg')
	plt.show()

if __name__ == "__main__":
	main()
