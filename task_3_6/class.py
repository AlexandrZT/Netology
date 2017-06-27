# --*--coding: utf-8 --*--
import random


class Animal:
    alive = False
    toxic_substances = ['phosphoryl chloride', 'aziridine', 'mercury', 'arsine']
    favotite_meal = []
    weight = 0
    name = ''
    grow_factor = 0
    my_words = ''

    def born_me(self):
        self.alive = True
        print('Haliiluaaa')

    def kill_me(self):
        self.alive = False
        print('Boom, boom...')

    def existance(self):
        return self.alive

    def say_something(self):
        if self.alive:
            print(self.my_words)
            return True
        else:
            return False

    def is_fatal(self, material):
        if material in self.toxic_substances:
            self.kill_me()


class Hens(Animal):
    favotite_meal = ['wheat', 'worm', 'insects']
    grow_factor = 0.25
    my_words = 'Ko, ko!'

    def test_it(self, what):
        if what in self.toxic_substances:
            self.kill_me()
        if what in self.favotite_meal:
            self.say_something()
            self.weight += self.grow_factor * 2
        else:
            self.weight += self.grow_factor


class Ducks(Animal):
    favotite_meal = ['wheat', 'insects', 'leech']
    grow_factor = 0.25
    my_words = 'Quack, quack!'

    def say_something(self):
        if self.alive:              # Hard way
            print('Quack, quack!')  #

    def test_it(self, what):
        if what in self.toxic_substances:
            self.kill_me()
        if what in self.favotite_meal:
            self.say_something()
            self.weight += self.grow_factor * 2
        else:
            self.weight += self.grow_factor


class Geese(Animal):
    favotite_meal = ['wheat', 'insects', 'leech']
    grow_factor = 0.15
    my_words = 'Eeeeg, Eeeg!'

    def test_it(self, what):
        if what in self.toxic_substances:
            self.kill_me()
        if what in self.favotite_meal:
            self.say_something()
            self.weight += self.grow_factor * 2
        else:
            self.weight += self.grow_factor


class Cows(Animal):
    favotite_meal = ['wheat', 'grass', 'apple']
    grow_factor = 4
    my_words = 'Muuu, Muuu!'

    def test_it(self, what):
        if what in self.toxic_substances:
            self.kill_me()
        if what in self.favotite_meal:
            self.say_something()
            self.weight += self.grow_factor * 2
        else:
            self.weight += self.grow_factor


class Goats(Animal):
    favotite_meal = ['grass', 'beet', 'apple']
    grow_factor = 2
    my_words = 'Meee, Meee!'

    def test_it(self, what):
        if what in self.toxic_substances:
            self.kill_me()
        if what in self.favotite_meal:
            self.say_something()
            self.weight += self.grow_factor * 2
        else:
            self.weight += self.grow_factor


class Sheeps(Animal):
    favotite_meal = ['grass', 'leaf', 'bread']
    grow_factor = 2.5
    my_words = 'Beee, Beee!'

    def test_it(self, what):
        if what in self.toxic_substances:
            self.kill_me()
        if what in self.favotite_meal:
            self.say_something()
            self.weight += self.grow_factor * 2
        else:
            self.weight += self.grow_factor


class Pigs(Animal):
    favotite_meal = ['wheat', 'bread', 'beet']
    grow_factor = 1.5
    my_words = 'Oink, Oink!'

    def test_it(self, what):
        if what in self.toxic_substances:
            self.kill_me()
        if what in self.favotite_meal:
            self.say_something()
            self.weight += self.grow_factor * 2
        else:
            self.weight += self.grow_factor


avaliable_food = ['insects', 'wheat', 'worm', 'beet', 'bread', 'apple', 'leech', 'grass', 'leaf', 'phosphoryl chloride',
                  'aziridine', 'mercury', 'arsine']
print('Let survaival begins!')
random.seed()
my_little_zoo = []
animal_hen = Hens()
animal_hen.name = 'Mr. Hen'
my_little_zoo.append(animal_hen)
animal_duck = Ducks()
animal_duck.name = 'Donald Duck'
my_little_zoo.append(animal_duck)
animal_geese = Geese()
animal_geese.name = 'Mr. Geese'
my_little_zoo.append(animal_geese)
animal_cow = Cows()
animal_cow.name = 'Borka'
my_little_zoo.append(animal_cow)
animal_goat = Goats()
animal_goat.name = 'Lovely'
my_little_zoo.append(animal_goat)
animal_sheep = Sheeps()
animal_sheep.name = 'Mr. Bee'
my_little_zoo.append(animal_sheep)
animal_pig = Pigs()
animal_pig.name = 'Yashko'
my_little_zoo.append(animal_pig)
for animal in my_little_zoo:
    animal.born_me()
    print('{} was born'.format(animal.name))
rounds = 3
continue_it = True
while continue_it:
    print('Round {} begins'.format(rounds))
    for animal in my_little_zoo:
        yammy = random.choice(avaliable_food)
        print('And Now {} will taste: {}'.format(animal.name, yammy))
        animal.test_it(yammy)
    if len(my_little_zoo) == 1 or rounds == 1:
        continue_it = False
    rounds -= 1
    print('-'*50)
print('Our champions!')
for animal in my_little_zoo:
    if animal.existance():
        print('{} is survived! His weight is {:.1f} kg'.format(animal.name, animal.weight))
