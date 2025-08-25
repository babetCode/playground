"""
Generate ranked poker hands and save to CSV.
This script evaluates all possible 5-card poker hands from a standard deck,
assigns a rank based on poker hand rankings, and saves the results to a CSV file.
"""

import random
import pandas as pd
from itertools import combinations
from typing import Tuple

class Deck:
    """A deck of playing cards for poker"""
    
    def __init__(self):
        """Initialize a standard 52-card deck"""
        self.ranks = [n for n in range(2, 15)]
        self.suits = ['c', 'h', 's', 'd']  # Clubs, Hearts, Spades, Diamonds
        self.reset()
    
    def reset(self):
        """Reset the deck to a full 52-card deck"""
        self.cards = [(rank, suit) for rank in self.ranks for suit in self.suits]
        self.dealt_cards = []
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
        return self
    
    def deal_card(self):
        """Deal one card from the top of the deck"""
        if not self.cards:
            raise ValueError("Cannot deal from an empty deck!")
        
        card = self.cards.pop()
        self.dealt_cards.append(card)
        return card
    
    def deal_hand(self, num_cards=2):
        """Deal a hand of cards (default 2 for poker)"""
        return [self.deal_card() for _ in range(num_cards)]
    
    def deal_flop(self):
        """Deal the flop (3 cards) - burns one card first"""
        self.burn_card()  # Burn a card before the flop
        return [self.deal_card() for _ in range(3)]
    
    def deal_turn_river(self):
        """Deal the turn (1 card) - burns one card first"""
        self.burn_card()  # Burn a card before the turn
        return self.deal_card()
    
    def burn_card(self):
        """Burn (discard) the top card - standard in poker"""
        if self.cards:
            burned = self.cards.pop()
            self.dealt_cards.append(burned)
            return burned
        return None
    
def formatted_card(card: Tuple):
    rank_map = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    suit_symbols = {'c': '♣', 'h': '♥', 's': '♠', 'd': '♦'}
    return f"{rank_map[card[0]] if card[0] in rank_map else card[0]}{card[1]}"

def is_straight(ranks):
    """Check if ranks form a straight"""
    return len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4 or sorted(ranks) == [2, 3, 4, 5, 14])

def is_flush(suits):
    """Check if all cards are the same suit"""
    return len(set(suits)) == 1

def get_rank_counts(ranks):
    """Get count of each rank, sorted by count then rank"""
    from collections import Counter
    counts = Counter(ranks)
    # Sort by count (descending) then by rank (descending)
    return sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

def evaluate_hand(hand):
    """
    Evaluate a 5-card poker hand and return a tuple for ranking.
    Lower tuple values = better hands.
    
    Returns: (hand_type_rank, tiebreaker_tuple)
    """
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]
    
    is_flush_hand = is_flush(suits)
    is_straight_hand = is_straight(ranks)
    rank_counts = get_rank_counts(ranks)
    
    # For straights, handle A-2-3-4-5 (wheel) as low straight
    if is_straight_hand:
        sorted_ranks = sorted(ranks)
        if sorted_ranks == [2, 3, 4, 5, 14]:  # A-2-3-4-5 straight
            straight_high = 5  # 5-high straight
        else:
            straight_high = max(ranks)
    
    # Hand type rankings (lower number = better hand)
    if is_straight_hand and is_flush_hand:
        if sorted(ranks) == [10, 11, 12, 13, 14] and is_flush_hand:
            return (0, ())  # Royal flush
        else:
            return (1, (-straight_high,))  # Straight flush
    
    elif rank_counts[0][1] == 4:  # Four of a kind
        four_kind = rank_counts[0][0]
        kicker = rank_counts[1][0]
        return (2, (-four_kind, -kicker))
    
    elif rank_counts[0][1] == 3 and rank_counts[1][1] == 2:  # Full house
        three_kind = rank_counts[0][0]
        pair = rank_counts[1][0]
        return (3, (-three_kind, -pair))
    
    elif is_flush_hand:  # Flush
        sorted_ranks_desc = sorted(ranks, reverse=True)
        return (4, tuple(-r for r in sorted_ranks_desc))
    
    elif is_straight_hand:  # Straight
        return (5, (-straight_high,))
    
    elif rank_counts[0][1] == 3:  # Three of a kind
        three_kind = rank_counts[0][0]
        kickers = sorted([rank_counts[1][0], rank_counts[2][0]], reverse=True)
        return (6, (-three_kind, -kickers[0], -kickers[1]))
    
    elif rank_counts[0][1] == 2 and rank_counts[1][1] == 2:  # Two pair
        high_pair = max(rank_counts[0][0], rank_counts[1][0])
        low_pair = min(rank_counts[0][0], rank_counts[1][0])
        kicker = rank_counts[2][0]
        return (7, (-high_pair, -low_pair, -kicker))
    
    elif rank_counts[0][1] == 2:  # One pair
        pair = rank_counts[0][0]
        kickers = sorted([rank_counts[1][0], rank_counts[2][0], rank_counts[3][0]], reverse=True)
        return (8, (-pair, -kickers[0], -kickers[1], -kickers[2]))
    
    else:  # High card
        sorted_ranks_desc = sorted(ranks, reverse=True)
        return (9, tuple(-r for r in sorted_ranks_desc))

def get_hand_name(hand):
    """Get the name of a poker hand"""
    evaluation = evaluate_hand(hand)
    hand_type = evaluation[0]

    hand_names = {
        0: "RF", # Royal Flush
        1: "SF", # Straight Flush
        2: "4K", # Four of a Kind
        3: "FH", # Full House
        4: "FL", # Flush
        5: "ST", # Straight
        6: "3K", # Three of a Kind
        7: "2P", # Two Pair
        8: "1P", # One Pair
        9: "HC" # High Card
    }

    return hand_names[hand_type]

# Generate all hands and rank them
deck = Deck()
all_hands = list(combinations(deck.cards, 5))

print(f"Total number of 5-card hands: {len(all_hands)}")

# Evaluate all hands and create ranking
hand_evaluations = [(hand, evaluate_hand(hand)) for hand in all_hands]

# Sort by evaluation (better hands first)
hand_evaluations.sort(key=lambda x: x[1])

# Create DataFrame with ranks
df_data = []
current_rank = 1
prev_evaluation = None

for i, (hand, evaluation) in enumerate(hand_evaluations):
    # If this evaluation is different from the previous, update rank
    if evaluation != prev_evaluation:
        current_rank = i + 1
    
    df_data.append({
        'Hand': ' '.join(formatted_card(card) for card in hand),
        'Type': get_hand_name(hand),
        'Rank': current_rank
    })
    
    prev_evaluation = evaluation

df = pd.DataFrame(df_data)

# Save to CSV for analysis
df.to_csv('poker_hands_ranked.csv', index=False)
print("\nAll ranked hands saved to 'poker_hands_ranked.csv'")