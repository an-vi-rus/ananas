from PIL import Image, ImageTk
from itertools import combinations
import random

rank_sym = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
suit_sym = ('♥♠♦♣')

def show_cards(cards: list):
    r = ''
    for item in cards: 
        r += rank_sym[item // 4]
        r += suit_sym[item % 4] + ' '
    return r
def set_card_imgs(w, h):
    global card_imgs
    card_imgs = []
    card_ranks=('2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace')
    card_suits = ('hearts', 'spades', 'diamonds', 'clubs')
    for i in range(13):
        for j in range(4):
            filename = 'images/' + card_ranks[i] + '_of_' + card_suits[j]
            filename = filename + '2.png' if i > 8 and i < 12 else filename + '.png'
            with Image.open(filename) as f:
                img = ImageTk.PhotoImage(f.resize((w - 2, h - 2), 2))
                card_imgs.append(img)
# Function returns arrays of sample size sample_size from deal with size 3 and deal_size amount
def get_samples(deal_size: list, sample_size: list):
    samples = {}
    for d in deal_size:
        samples[d] = []
        deals = list(combinations(range(d), 3))
        for s in sample_size:
            sample = random.sample(deals, s)
            samples[d].append(sample)
    return samples



