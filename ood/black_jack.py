# Card: Represents a single card with a suit and rank, encapsulating its properties and behavior.
# Deck: Manages a deck of cards, allowing shuffling and dealing.
# Hand: Holds a collection of cards and provides methods to calculate the hand's value, check for Blackjack, and determine if it's soft.
# Player: Represents the player, who makes decisions (hit or stand) based on a simple strategy.
# Dealer: Represents the dealer, who follows fixed rules (hits on soft 17).
# Game: Orchestrates the game flow, managing the deck, player, and dealer, and determining the winner.
import random


class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self, suit, rank):
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def get_value(self):
        if self.rank == "A":
            return 11
        elif self.rank in ['J', 'Q', 'K']:
            return 10
        else:
            return int(self.rank)
        
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        random.shuffle(self.cards)
        
    def deal(self):
        if not self.cards:
            raise ValueError("Deck is empty")
        random_index = random.randrange(len(self.cards))
        return self.cards.pop(random_index)
    
class Hand:
    def __init__(self):
        self.hand = []
        
    def add_card(self, card):
        self.hand.append(card)
        
    def calculate_value(self):
        value = sum(card.get_value() for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.rank == 'A')
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value
    
    def is_blackjack(self):
        return len(self.hand) == 2 and self.calculate_value() == 21
    
    def is_soft(self):
        value_with_ace_as_11 = sum(card.get_value() for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.rank == "A")
        if num_aces == 0:
            return False
        for _ in range(num_aces):
            if value_with_ace_as_11 <= 21:
                return True
            value_with_ace_as_11 -= 10
        return False
    def is_busted(self):
        return self.calculate_value() > 21
    
    
    def __str__(self):
        return ', '.join(str(card) for card in self.hand)
    
class Player:
    def __init__(self):
        self.hand = Hand()
        
    def decide(self, dealer_up_card):
        hand_value = self.hand.calculate_value()
        if self.hand.is_soft():
            return 'hit' if hand_value < 18 else 'stand'
        else:
            return 'hit' if hand_value < 17 else 'stand'
class Dealer:
    def __init__(self):
        self.hand = Hand()
        
    def play(self, deck):
        while self.hand.calculate_value() < 17:
            self.hand.add_card(deck.deal())
            
class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        
    def deal_init_cards(self):
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())
            
    def play(self):
        self.deal_init_cards()
        print(f"Player's hand: {self.player.hand}")
        print(f"Dealer's up card: {self.dealer.hand.hand[0]}")
        
        while self.player.decide(self.dealer.hand.hand[0]) == 'hit':
            self.player.hand.add_card(self.deck.deal())
            print(f"Player hits, new hand: {self.player.hand}")
            if self.player.hand.calculate_value() > 21:
                print("Player busts")
                return "Player loses"
            
        self.dealer.play(self.deck)
        print(f"Dealer's hand: {self.dealer.hand}")
        
        player_value = self.player.hand.calculate_value()
        dealer_value = self.dealer.hand.calculate_value()
        
        if self.dealer.hand.is_blackjack():
            if self.player.hand.is_blackjack():
                print("push")
            else:
                print("Player loses")
        elif self.player.hand.is_blackjack():
            print("Player wins")
        else:
            if player_value > 21:    
                print("Player loses")
            elif dealer_value > 21:
                print("Player wins")
            elif player_value > dealer_value:
                print("Player wins")
            elif player_value == dealer_value:
                print("Push")
            else:
                print("Player loses")
                
        return "Game over"
import unittest


class TestCard(unittest.TestCase):
    def test_valid_card(self):
        """Test that a card initializes correctly with valid suit and rank."""
        card = Card('Hearts', 'A')
        self.assertEqual(str(card), 'A of Hearts')
        self.assertEqual(card.get_value(), 11)

    def test_invalid_suit(self):
        """Test that an invalid suit raises a ValueError."""
        with self.assertRaises(ValueError):
            Card('InvalidSuit', '2')

    def test_invalid_rank(self):
        """Test that an invalid rank raises a ValueError."""
        with self.assertRaises(ValueError):
            Card('Hearts', '1')

    def test_get_value(self):
        """Test the get_value method for different ranks."""
        self.assertEqual(Card('Spades', '10').get_value(), 10)
        self.assertEqual(Card('Diamonds', 'J').get_value(), 10)
        self.assertEqual(Card('Clubs', '5').get_value(), 5)

class TestDeck(unittest.TestCase):
    def test_deck_initialization(self):
        """Test that a new deck has 52 cards."""
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deal(self):
        """Test that dealing a card reduces deck size and returns a Card."""
        deck = Deck()
        card = deck.deal()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), 51)

    def test_deal_empty_deck(self):
        """Test that dealing from an empty deck raises an error."""
        deck = Deck()
        for _ in range(52):
            deck.deal()
        with self.assertRaises(ValueError):
            deck.deal()

class TestHand(unittest.TestCase):
    def test_add_card(self):
        """Test adding a card to a hand."""
        hand = Hand()
        card = Card('Hearts', '10')
        hand.add_card(card)
        self.assertEqual(len(hand.hand), 1)
        self.assertEqual(str(hand), '10 of Hearts')

    def test_calculate_value(self):
        """Test hand value calculation, including Ace adjustments."""
        hand = Hand()
        hand.add_card(Card('Spades', '10'))
        hand.add_card(Card('Hearts', '5'))
        self.assertEqual(hand.calculate_value(), 15)

        # Test with Aces
        hand = Hand()
        hand.add_card(Card('Diamonds', 'A'))
        hand.add_card(Card('Clubs', '10'))
        self.assertEqual(hand.calculate_value(), 21)

        hand.add_card(Card('Spades', 'A'))
        self.assertEqual(hand.calculate_value(), 12)  # A, 10, A -> 11 + 10 + 1

    def test_is_blackjack(self):
        """Test Blackjack detection."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'A'))
        hand.add_card(Card('Spades', '10'))
        self.assertTrue(hand.is_blackjack())

        hand.add_card(Card('Clubs', '2'))
        self.assertFalse(hand.is_blackjack())  # More than 2 cards

        hand = Hand()
        hand.add_card(Card('Diamonds', '10'))
        hand.add_card(Card('Clubs', 'J'))
        self.assertFalse(hand.is_blackjack())  # Two 10-value cards

    def test_is_soft(self):
        """Test soft hand detection."""
        hand = Hand()
        hand.add_card(Card('Hearts', 'A'))
        hand.add_card(Card('Spades', '6'))
        self.assertTrue(hand.is_soft())  # A + 6 = 17 (soft)

        hand.add_card(Card('Clubs', '10'))
        self.assertFalse(hand.is_soft())  # A + 6 + 10 = 17 (hard, A = 1)

        hand = Hand()
        hand.add_card(Card('Diamonds', '10'))
        hand.add_card(Card('Clubs', '7'))
        self.assertFalse(hand.is_soft())  # No Aces

class TestPlayer(unittest.TestCase):
    def test_decide_hit_soft(self):
        """Test player decision to hit on soft 17."""
        player = Player()
        player.hand.add_card(Card('Hearts', 'A'))
        player.hand.add_card(Card('Spades', '6'))  # Soft 17
        self.assertEqual(player.decide(Card('Clubs', '10')), 'hit')

    def test_decide_stand_soft(self):
        """Test player decision to stand on soft 18."""
        player = Player()
        player.hand.add_card(Card('Hearts', 'A'))
        player.hand.add_card(Card('Spades', '7'))  # Soft 18
        self.assertEqual(player.decide(Card('Clubs', '10')), 'stand')

    def test_decide_hit_hard(self):
        """Test player decision to hit on hard 16."""
        player = Player()
        player.hand.add_card(Card('Diamonds', '10'))
        player.hand.add_card(Card('Clubs', '6'))  # Hard 16
        self.assertEqual(player.decide(Card('Clubs', '10')), 'hit')

    def test_decide_stand_hard(self):
        """Test player decision to stand on hard 17."""
        player = Player()
        player.hand.add_card(Card('Diamonds', '10'))
        player.hand.add_card(Card('Clubs', '7'))  # Hard 17
        self.assertEqual(player.decide(Card('Clubs', '10')), 'stand')

class TestDealer(unittest.TestCase):
    def test_play(self):
        """Test dealer plays until hand value is 17 or higher."""
        dealer = Dealer()
        deck = Deck()
        dealer.hand.add_card(deck.deal())
        dealer.hand.add_card(deck.deal())
        initial_value = dealer.hand.calculate_value()
        dealer.play(deck)
        final_value = dealer.hand.calculate_value()
        self.assertGreaterEqual(final_value, 17)
        if initial_value < 17:
            self.assertGreater(final_value, initial_value)

if __name__ == '__main__':
    game = Game()
    game.play()