import random
from IPython.display import HTML, display

from itertools import combinations
from collections import Counter
from typing import List, Tuple

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
    
    def deal_turn(self):
        """Deal the turn (1 card) - burns one card first"""
        self.burn_card()  # Burn a card before the turn
        return self.deal_card()
    
    def deal_river(self):
        """Deal the river (1 card) - burns one card first"""
        self.burn_card()  # Burn a card before the river
        return self.deal_card()
    
    def burn_card(self):
        """Burn (discard) the top card - standard in poker"""
        if self.cards:
            burned = self.cards.pop()
            self.dealt_cards.append(burned)
            return burned
        return None
    
    def cards_remaining(self):
        """Return number of cards remaining in deck"""
        return len(self.cards)
    
    def peek_top(self, num=1):
        """Peek at the top card(s) without dealing them"""
        if num > len(self.cards):
            return self.cards[-len(self.cards):]
        return self.cards[-num:]
    
    def __len__(self):
        """Return number of cards in deck"""
        return len(self.cards)
    
    def __str__(self):
        """String representation showing cards remaining"""
        return f"Deck with {len(self.cards)} cards remaining"
    
    def __repr__(self):
        """Detailed representation"""
        return f"Deck(cards_remaining={len(self.cards)}, dealt={len(self.dealt_cards)})"

def evaluate_hand(cards: List[Tuple]) -> Tuple[str, int, List[Tuple]]:
    """Evaluates a 5-card hand and returns (hand_type, hand_rank, best_cards)."""
    ranks = sorted([card[0] for card in cards], reverse=True)
    suits = [card[1] for card in cards]
    rank_counts = Counter(ranks)
    # suit_counts = Counter(suits)
    
    is_flush = len(set(suits)) == 1
    is_straight = len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4 or ranks == [14, 5, 4, 3, 2])
    
    # Royal Flush
    if is_flush and ranks == [14, 13, 12, 11, 10]:
        return "RF", 10, cards
    
    # Straight Flush
    if is_flush and is_straight:
        return "SF", 9, cards
    
    # Four of a Kind
    if 4 in rank_counts.values():
        four_rank = next(r for r, c in rank_counts.items() if c == 4)
        kicker = max(r for r in ranks if r != four_rank)
        return "4k", 8, [c for c in cards if c[0] == four_rank or c[0] == kicker]
    
    # Full House
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        three_rank = next(r for r, c in rank_counts.items() if c == 3)
        pair_rank = next(r for r, c in rank_counts.items() if c == 2)
        return "FH", 7, [c for c in cards if c[0] in [three_rank, pair_rank]]
    
    # Flush
    if is_flush:
        return "FL", 6, cards
    
    # Straight
    if is_straight:
        return "ST", 5, cards
    
    # Three of a Kind
    if 3 in rank_counts.values():
        three_rank = next(r for r, c in rank_counts.items() if c == 3)
        kickers = sorted([r for r in ranks if r != three_rank], reverse=True)[:2]
        return "3K", 4, [c for c in cards if c[0] == three_rank or c[0] in kickers]
    
    # Two Pair
    if list(rank_counts.values()).count(2) >= 2:
        pair_ranks = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)[:2]
        kicker = max(r for r in ranks if r not in pair_ranks)
        return "2P", 3, [c for c in cards if c[0] in pair_ranks or c[0] == kicker]
    
    # Pair
    if 2 in rank_counts.values():
        pair_rank = next(r for r, c in rank_counts.items() if c == 2)
        kickers = sorted([r for r in ranks if r != pair_rank], reverse=True)[:3]
        return "PR", 2, [c for c in cards if c[0] == pair_rank or c[0] in kickers]
    
    # High Card
    return "HC", 1, cards

def texas_holdem_score(seven_cards: List[Tuple]) -> Tuple[str, int, List[Tuple]]:
    """Evaluates the best 5-card hand from seven cards and returns (hand_type, hand_rank, best_cards)."""
    if len(seven_cards) != 7:
        raise ValueError("Exactly seven cards are required")
    
    best_score = (None, 0, [], [])
    for combo in combinations(seven_cards, 5):
        hand_type, hand_rank, best_cards = evaluate_hand(list(combo))
        ranks = sorted([c[0] for c in best_cards], reverse=True)
        current_score = (hand_type, hand_rank, best_cards, ranks)
        if best_score[1] < hand_rank or (best_score[1] == hand_rank and ranks > best_score[3]):
            best_score = current_score
    
    return best_score[0], best_score[1], best_score[2]
    
def formatted_card(card: Tuple) -> str:

    def print_red(text):
        print(f'\033[1;31;47m{text}\033[0m')

    def print_black(text):
        print(f'\033[1;90;47m{text}\033[0m')
    
    rank_map = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    suit_symbols = {'c': '♣', 'h': '♥', 's': '♠', 'd': '♦'}
    return f"{rank_map[card[0]] if card[0] in rank_map else card[0]}{suit_symbols[card[1]]}"

def main():
    players = 5

    deck = Deck()
    deck.shuffle()

    hands_dict = {}
    for i in range(players):
        hands_dict[i] = deck.deal_hand()

    for player in hands_dict:
        hand = [formatted_card(card) for card in hands_dict[player]]
        print(f"{str(hand[0])} {str(hand[1])}", end=" | ")

    print("")

    table = deck.deal_flop()+[deck.deal_turn()]+[deck.deal_river()]

    for player in hands_dict:
        print(f"  {texas_holdem_score(hands_dict[player] + table)[0]}  | ", end="")

    print("")

    print([formatted_card(card) for card in table])

if __name__ == "__main__":
    main()
