# Card: Represents a single card with a suit and rank, encapsulating its properties and behavior.
# Deck: Manages a deck of cards, allowing shuffling and dealing.
# Hand: Holds a collection of cards and provides methods to calculate the hand's value, check for Blackjack, and determine if it's soft.
# Player: Represents the player, who makes decisions (hit or stand) based on a simple strategy.
# Dealer: Represents the dealer, who follows fixed rules (hits on soft 17).
# Game: Orchestrates the game flow, managing the deck, player, and dealer, and determining the winner.
import random
class Card:
    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    def __init__(self, suit, rank):
        if suit not in self.SUITS:
            raise ValueError("Not valid suit")
        if rank not in self.RANKS:
            raise ValueError("Not a valid rank")
        self.rank = rank
        self.suit = suit
    
    def get_value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        random.shuffle(self.deck)
    def deal(self):
        if not self.deck:
            raise ValueError("The deck is empty")
        
        
        return self.deck.pop()
    

        
        
        
    
class Hand:
    def __init__(self):
        self.cards = []
        
    def add_card(self, card):
        if not isinstance(card, Card):
            raise TypeError
        self.cards.append(card)
           
    def calculate_value(self):
        value = sum(card.get_value() for card in self.cards)
        ace_num = sum(1 for card in self.cards if card.rank == "A")
        while value > 21 and ace_num > 0:
            value -= 10
            ace_num -= 1
        return value
    def is_blackjack(self):
        return self.calculate_value() == 21 and len(self.cards) == 2 and sum(1 for card in self.cards if card.rank == "A") == 1
    def is_softhand(self):
        if not any(card.rank == "A" for card in self.cards):
            return False
        min_value = sum(1 if card.rank == "A" else card.get_value() for card in self.cards)
        
        return self.calculate_value() > min_value
    def is_busted(self):
        return self.calculate_value() > 21
    def __str__(self):
        return ", ".join(str(card) for card in self.cards)
                
class Player():
    def __init__(self):
        self.hand = Hand()
        
    def decision(self):
        if self.hand.is_softhand() and self.hand.calculate_value() < 18:
            
            return "Hit"
        elif not self.hand.is_softhand() and self.hand.calculate_value() < 17:
            
            return "Hit"
        else:
            return "Stand"
            
class Dealer():
    def __init__(self):
        self.hand = Hand()
        
    def strategy(self, deck):
        while self.hand.calculate_value() < 17 or (self.hand.calculate_value() == 17 and self.hand.is_softhand()):
            self.hand.add_card(deck.deal())
class Game():
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        
    def play(self):
        #first draw 2 cards for player and dealler
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())
        
        #show cards 
        print(f"Player's hand {self.player.hand}")
        print(f"Dealer's up card {self.dealer.hand.cards[0]}")
        #player use his rule
        while self.player.decision() == "Hit":
            self.player.hand.add_card(self.deck.deal())
            print(f"Player hits, new hand: {self.player.hand}") 
            if self.player.hand.is_busted():
                print("Player busts")
                print("Player loses")
                return "Game over"
        self.dealer.strategy(self.deck)
        print(f"Dealer's hand: {self.dealer.hand}")
        #dealer use his rule
        #get result
        
        player_val = self.player.hand.calculate_value()
        dealer_val = self.dealer.hand.calculate_value()
        
        if self.dealer.hand.is_blackjack():
            if not self.player.hand.is_blackjack():
                print("BlackJack, Player lose")
            else:
                print("Push")
        elif self.player.hand.is_blackjack():
            print("BlackJack, Player win")
        
        else:
            if player_val > 21:
                print("Player lose")
            elif dealer_val > 21:
                print("Dealer lose")
            elif dealer_val > player_val:
                print("Player lose")
            elif dealer_val == player_val:
                print("push")
            else:
                print("Player win")
        return "Game over"
        
# 测试用例
def test_game_player_busts():
    print("=== Test Case: Player Busts ===")
    game = Game()
    
    # 清空并加载特定的牌堆，确保玩家爆牌
    game.deck.deck = [
    Card("Spades", "10"),   # 玩家第一张
    Card("Clubs", "10"),      # 玩家第二张
    Card("Hearts", "10"),    # 庄家第一张（可为任意牌，只要不影响测试目标）
    Card("Diamonds", "2"),   # 庄家第二张（可为任意牌）
    Card("Spades", "6")      # 玩家 Hit 的牌，导致爆牌 10+10+6=26
][::-1]
  # 反转以模拟从顶部发牌
    
    result = game.play()
    print(f"Test result: {result}\n")

if __name__ == "__main__":
    # 运行测试用例
    test_game_player_busts()
    # 运行随机游戏
    print("=== Random Game ===")
    Game().play()            
        