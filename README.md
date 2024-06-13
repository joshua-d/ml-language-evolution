# ml-language-evolution
Neural Networks learn to communicate with each other using their own language.

IMPORTANT: Pygame must be installed to run.

This was my submission to the HackBU Hackathon 2020. It won the "Best Machine Learning Hack" award, and I received a $50 Amazon gift card. It uses my homemade NEAT utility that I consistently developed when I was younger ([neural-env-py](https://github.com/joshua-d/neural-env-py)).

Each person has 2 neural networks. One translates a task into a sentence, and the other translates a sentence back into a task. Natural selection and NEAT is used to ultimately create a simple language between persons, such that one may tell another a task that needs to be done using a sentence, and the other will "understand" and perform the task.
