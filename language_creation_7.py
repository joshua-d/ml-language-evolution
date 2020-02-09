import neural_env
import random


days_per_round = 50
n_subjects = 2
n_verbs = 2
n_nouns = 2
letters_per_word = 3
word_structure = ['c', 'v', 'c']
letters_per_neuron = 3
consonants = ['b', 'c', 'd']
vowels = ['a', 'e', 'i']

class Lang:
    def __init__(self, population, nenv_speak, nenv_receive):
        self.population = population
        self.nenv_speak = nenv_speak
        self.nenv_receive = nenv_receive

        self.generation = 0


lang = Lang([], None, None)


class Person:

    def __init__(self, speak_network, receive_network):
        self.speak_network = speak_network
        self.receive_network = receive_network

        self.task = None
        self.sentence = None
        self.decision = None

        self.s_success = 0
        self.r_success = 0

    def get_task(self):
        self.task = []

        for i in range(n_subjects + n_verbs + n_nouns):
            self.task.append(0)

        subject = random.randint(0, n_subjects - 1)
        verb = random.randint(0, n_verbs - 1)
        noun = random.randint(0, n_nouns - 1)

        self.task[subject] = 1
        self.task[verb + n_subjects] = 1
        self.task[noun + n_subjects + n_verbs] = 1

    def speak(self, receiver):
        self.sentence = []
        self.speak_network.input_data(self.task)
        output_list = self.speak_network.get_output_neurons()
        for neuron in output_list:
            self.sentence.append(neuron.value)
        receiver.receive(self)

    def receive(self, speaker):
        self.receive_network.input_data(speaker.sentence)
        output_list = self.receive_network.get_output_neurons()

        self.decision = []

        for i in range(n_subjects + n_verbs + n_nouns):
            self.decision.append(0)

        subject = 0
        subject_val = output_list[0].value
        for i in range(1, n_subjects):
            if output_list[i].value > subject_val:
                subject_val = output_list[i].value
                subject = i

        verb = n_subjects
        verb_val = output_list[verb].value
        for i in range(n_subjects + 1, n_subjects + n_verbs):
            if output_list[i].value > verb_val:
                verb_val = output_list[i].value
                verb = i

        noun = n_subjects + n_verbs
        noun_val = output_list[noun].value
        for i in range(n_subjects + n_verbs + 1, n_subjects + n_verbs + n_nouns):
            if output_list[i].value > noun_val:
                noun_val = output_list[i].value
                noun = i

        self.decision[subject] = 1
        self.decision[verb] = 1
        self.decision[noun] = 1

    def reset(self):
        self.task = None
        self.sentence = None
        self.decision = None
        self.s_success = 0
        self.r_success = 0


def do_day(population):
    random.shuffle(population)
    for i in range(len(population)):
        speaker = population[i]
        receiver = population[(i + 1) % len(population)]

        speaker.get_task()
        speaker.speak(receiver)

        correct = True
        for j in range(len(receiver.decision)):
            if receiver.decision[j] != speaker.task[j]:
                correct = False
        if correct:
            speaker.s_success += 1
            receiver.r_success += 1


def do_round(population, nenv_s, nenv_r):

    for i in range(days_per_round):
        do_day(population)

    fitnesses = []

    for person in population:
        fitness = -person.s_success - person.r_success
        person.speak_network.fitness = fitness
        person.receive_network.fitness = fitness

        fitnesses.append(fitness)

    nenv_s.reproduce()
    nenv_r.reproduce()

    for i in range(len(population)):
        population[i].reset()
        population[i].speak_network = nenv_s.networks[i]
        population[i].receive_network = nenv_r.networks[i]

    best = 0
    mean = 0
    for fitness in fitnesses:
        mean += fitness
        if fitness < best:
            best = fitness
    mean /= len(fitnesses)

    lang.generation += 1
    return str(best) + " " + str(mean)


def translate_sentence(sentence):
    words = ["", "", ""]

    increment = 1 / letters_per_neuron

    for w in range(3):
        for i in range(letters_per_word):
            for j in range(1, letters_per_neuron + 1):
                if sentence[i + w * letters_per_word] <= j * increment:
                    if word_structure[i] == 'c':
                        words[w] += consonants[j - 1]
                    else:
                        words[w] += vowels[j - 1]
                    break

    return words[0] + " " + words[1] + " " + words[2]


def save_networks(population, nenv_s, nenv_r):
    for i in range(len(population)):
        nenv_s.export_network(population[i].speak_network, "speak_network_" + str(i) + ".txt")
        nenv_r.export_network(population[i].receive_network, "receive_network_" + str(i) + ".txt")


def import_networks(nenv_s, nenv_r):
    for i in range(len(nenv_s.networks)):
        nenv_s.networks[i] = nenv_s.import_network("speak_network_" + str(i) + ".txt")
        nenv_r.networks[i] = nenv_r.import_network("receive_network_" + str(i) + ".txt")


def setup():
    random.seed(3)

    pop_size = 100

    s_input = n_subjects + n_verbs + n_nouns
    s_output = letters_per_word * 3
    s_hidden = s_input + (s_output - s_input) / 2
    r_input = s_output
    r_output = s_input
    r_hidden = s_hidden

    lang.nenv_speak = neural_env.NeuralEnv(pop_size, s_input, s_hidden, s_output, 2)
    lang.nenv_receive = neural_env.NeuralEnv(pop_size, r_input, r_hidden, r_output, 2)

    lang.population = []
    lang.generation = 0
    # Create Population
    for i in range(pop_size):
        lang.population.append(Person(lang.nenv_speak.networks[i], lang.nenv_receive.networks[i]))


def get_population():
    return lang.population


def get_nenv_s():
    return lang.nenv_speak


def get_nenv_r():
    return lang.nenv_receive


def get_generation():
    return lang.generation


def main():
    random.seed(3)

    pop_size = 100

    s_input = n_subjects + n_verbs + n_nouns
    s_output = letters_per_word * 3
    s_hidden = s_input + (s_output - s_input) / 2
    r_input = s_output
    r_output = s_input
    r_hidden = s_hidden

    lang.nenv_speak = neural_env.NeuralEnv(pop_size, s_input, s_hidden, s_output, 2)
    lang.nenv_receive = neural_env.NeuralEnv(pop_size, r_input, r_hidden, r_output, 2)

    # Create Population
    for i in range(pop_size):
        lang.population.append(Person(lang.nenv_speak.networks[i], lang.nenv_receive.networks[i]))

    for i in range(500):
        print(str(i) + " " + do_round(lang.population, lang.nenv_speak, lang.nenv_receive))

    lang.nenv_speak.export_network(lang.population[0].speak_network, "speak_network.txt")
    lang.nenv_receive.export_network(lang.population[0].receive_network, "receive_network.txt")


# main()