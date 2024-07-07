import random

subjects = ["The cat", "A dog", "The bird", "A person", "The teacher"]
verbs = ["eats", "jumps over", "runs to", "looks at", "reads"]
objects = ["the food", "a book", "the car", "the tree", "a ball"]

def generate_random_sentence():
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    obj = random.choice(objects)
    return f"{subject} {verb} {obj}."