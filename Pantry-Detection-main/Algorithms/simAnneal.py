import random
import string
import math
import Levenshtein

def read_english_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def generate_neighbor(word):
    pos = random.randint(0, len(word) - 1)
    new_char = random.choice(string.ascii_lowercase)
    neighbor = word[:pos] + new_char + word[pos + 1:]
    return neighbor

def similarity_score(word1, word2):
    return sum(1 for a, b in zip(word1, word2) if a == b)

def levenshtein_score(word1, word2):
    return -Levenshtein.distance(word1, word2)

def is_valid_word(word, english_words):
    return word in english_words

def total_score(word, misspelled_word, english_words):

    in_dict_bonus = 100 if is_valid_word(word, english_words) else 0

    scores = [(w, similarity_score(misspelled_word, w) + 
               levenshtein_score(misspelled_word, w) +
               in_dict_bonus) 
              for w in english_words]

    best_word, best_score = max(scores, key=lambda x: x[1])

    penalty = -levenshtein_score(misspelled_word, best_word) / 2

    best_score += penalty

    return best_score


def simulated_annealing(initial_word, temperature, cooling_rate, iterations, english_words):
    current_word = initial_word
    best_word = current_word

    for _ in range(iterations):
        neighbor_word = generate_neighbor(current_word)

        current_score = total_score(current_word, initial_word, english_words)
        neighbor_score = total_score(neighbor_word, initial_word, english_words)

        # Update the current word with the neighbor word only if the neighbor score is higher
        if neighbor_score > current_score:
            current_word = neighbor_word
        else:
            acceptance_prob = math.exp((neighbor_score - current_score) / temperature)  
            if random.random() < acceptance_prob:
                current_word = neighbor_word


        # Always update the best word if the neighbor score is higher
        if neighbor_score > total_score(best_word, initial_word, english_words):
            best_word = neighbor_word

        temperature *= 1 - cooling_rate

    return best_word

if __name__ == "__main__":
    english_words = read_english_words("dictionary.txt")  # Update the path to your file

    misspelled_word = "appl"

    initial_temperature = 1.0
    cooling_rate = 0.001 
    iterations = 50000  

    result = simulated_annealing(misspelled_word, initial_temperature, cooling_rate, iterations, english_words)
    result_score = total_score(result, misspelled_word, english_words)
    
    print(f"Misspelled word: {misspelled_word}")
    print(f"Guessed word: {result}") 
    print(f"Guessed word score: {result_score}")
