from operator import attrgetter

from models.cards import Card


class HandProcessor(object):
    """
    Class for processing hands based on the Psychic Poker Player problem that goes as follows:
    Normally the player cannot see the cards in the deck and so must use probability to decide which cards to discard.
    In this problem, we imagine that the poker player is psychic and knows which cards are on top of the deck.
    """

    def __init__(self, hand_n_deck):
        """
        Initializer for Poker Hand Processor.
        :param hand_n_deck: <str> Input specifying hand cards and top 5 deck cards, each separated with space
                            e.g 'TH JH QC QD QS QH KH AH 2S 6S'
        """
        assert isinstance(hand_n_deck, basestring), \
            "Invalid Parameter 'hand_n_deck'. Should be of type string"

        hand_n_deck_split = hand_n_deck.split()

        assert len(hand_n_deck_split) == 10, \
            "Invalid parameter 'hand_n_deck': '{hand_n_deck}'. Should specify 10 cards in total. " \
            "Each card is represented as a two-character code. The first character is the " \
            "face-value (A=Ace, 2-9, T=10, J=Jack, Q=Queen, K=King) and the second character is the suit " \
            "(C=Clubs, D=Diamonds, H=Hearts, S=Spades)".format(hand_n_deck=hand_n_deck)

        assert len(set(hand_n_deck_split)) == len(hand_n_deck_split), \
            "The list of cards provided should not contain duplicates"

        self.hand_n_deck_cards = [Card(value) for value in hand_n_deck_split]
        self.hand_cards = self.hand_n_deck_cards[:5]
        self.deck_cards = self.hand_n_deck_cards[5:]

    @staticmethod
    def get_same_suit_cards(cards):
        """
        Get same suit cards among the provided cards.
        :param cards: <list> Cards from which to identify same suit cards.
        :return: <dict> Returns dictionary of same suit cards with keys as suits and list of cards as values.
        """
        suit_cards_dict = dict()
        for card in cards:
            if card.suit not in suit_cards_dict:
                suit_cards_dict[card.suit] = list()

            suit_cards_dict[card.suit].append(card)

        return suit_cards_dict

    @staticmethod
    def get_consecutive_cards(cards):
        """
        Get list of consecutive card sets.
        :param cards: <list> Cards from which to identify consecutive cards.
        :return: <list> List of lists containing consecutive cards.
        """
        consecutive_cards_set_list = list()
        cards = sorted(cards, key=attrgetter('rank'))
        for card in cards:
            added = False
            for index, cc_list in enumerate(consecutive_cards_set_list):
                cc_ranks_list = sorted([card_.rank for card_ in cc_list])
                if card.rank not in cc_ranks_list and \
                        (card.rank + 1 == cc_ranks_list[0] or card.rank - 1 == cc_ranks_list[-1]):
                    consecutive_cards_set_list[index].append(card)
                    added = True
                    break

            if not added:
                consecutive_cards_set_list.append([card])

        return consecutive_cards_set_list

    @staticmethod
    def get_same_face_cards(cards):
        """
        Get same face cards among the provided cards.
        :param cards: <list> Cards from which to identify same face cards.
        :return: <dict> Returns dictionary of same face cards with keys as faces and list of cards as values.
        """
        face_cards_dict = dict()
        for card in cards:
            if card.face not in face_cards_dict.keys():
                face_cards_dict[card.face] = list()
            face_cards_dict[card.face].append(card)

        return face_cards_dict

    def get_hand_deck_required_cards(self, cards):
        hand_cards, deck_cards = list(), list()
        for card in cards:
            if card in self.hand_cards:
                hand_cards.append(card)
            else:
                deck_cards.append(card)

        return hand_cards, deck_cards

    def get_farthest_deck_card_location(self, required_deck_cards):
        locations = list()
        for required_deck_card in required_deck_cards:
            locations.append(self.deck_cards.index(required_deck_card) + 1)

        return max(locations) if locations else 0

    @staticmethod
    def get_number_of_discardable_hand_cards(required_cards):
        return 5 - len(required_cards)

    def draw_possibility(self, required_cards):
        required_hand_cards, required_deck_cards = self.get_hand_deck_required_cards(required_cards)
        farthest_location = self.get_farthest_deck_card_location(required_deck_cards)
        if farthest_location > self.get_number_of_discardable_hand_cards(required_hand_cards):
            return False
        return True

    def straight_flush_possible(self):
        """
        Function that determines whether a straight flush is possible.
        Straight Flush: Five cards of the same suit in sequence.
        :return: <bool> Returns True if possible else False.
        """
        same_suit_cards_dict = self.get_same_suit_cards(self.hand_n_deck_cards)
        for suit_cards_list in same_suit_cards_dict.itervalues():
            if not len(suit_cards_list) >= 5:
                continue

            consecutive_cards_set_list = self.get_consecutive_cards(suit_cards_list)
            for consecutive_cards_set in consecutive_cards_set_list:
                if not len(consecutive_cards_set) >= 5:
                    continue

                for index in range(0, len(consecutive_cards_set) - 4):
                    if self.draw_possibility(consecutive_cards_set[index: index + 5]):
                        return True

        return False

    def __times_of_a_kind_possible(self, times):
        """
        Function that returns the times of kind (3 or 4) hands.
        :param times: <int> number of times.
        :return: <bool> Returns True if possible else False.
        """
        same_face_cards_dict = self.get_same_face_cards(self.hand_n_deck_cards)
        for face_cards_list in same_face_cards_dict.itervalues():
            if not len(face_cards_list) == times:
                continue

            if self.draw_possibility(face_cards_list):
                return True

        return False

    def four_of_a_kind_possible(self):
        """
        Function that determines whether four of a kind hand is possible.
        Four Of A Kind: Four cards of the same rank - such as four queens.
        :return: <bool> Returns True if possible else False.
        """
        return self.__times_of_a_kind_possible(4)

    def three_of_a_kind_possible(self):
        """
        Function that determines whether three of a kind hand is possible.
        Three Of A Kind: Three cards of the same rank - such as three queens.
        :return: <bool> Returns True if possible else False.
        """
        return self.__times_of_a_kind_possible(3)

    def full_house_possibility(self):
        """
        Function that determines whether full-house hand is possible.
        Full House: Three cards of one rank and two cards of another rank.
        :return: <bool> Returns True if possible else False.
        """
        same_face_cards_dict = self.get_same_face_cards(self.hand_n_deck_cards)
        three_sets = list()
        two_sets = list()
        for same_face_cards_list in same_face_cards_dict.itervalues():
            if len(same_face_cards_list) >= 3:
                three_sets.append(same_face_cards_list)
            if len(same_face_cards_list) >= 2:
                two_sets.append(same_face_cards_list)

        if not (three_sets and two_sets):
            return False

        for three_set in three_sets:
            for index in range(0, len(three_set) - 2):
                if not self.draw_possibility(three_set[index: index + 3]):
                    continue

            for two_set in two_sets:
                if two_set == three_set:
                    continue

                for index_ in range(0, len(two_set) - 1):
                    if not self.draw_possibility(two_set[index_: index_ + 2] + three_set[index: index + 3]):
                        continue

                    return True

        return False

    def flush_possibility(self):
        """
        Function that determines whether flush hand is possible.
        Flush: Five cards of the same suit.
        :return: <bool> Returns True if possible else False.
        """
        same_suit_cards_dict = self.get_same_suit_cards(self.hand_n_deck_cards)
        for suit_cards_list in same_suit_cards_dict.itervalues():
            if not len(suit_cards_list) >= 5:
                continue

            for index in range(0, len(suit_cards_list) - 4):
                if self.draw_possibility(suit_cards_list[index: index + 5]):
                    return True

        return False

    def straight_possible(self):
        """
        Function that determines whether straight hand is possible.
        Straight: Five cards of mixed suits in sequence.
        :return: <bool> Returns True if possible else False.
        """
        consecutive_cards_set_list = self.get_consecutive_cards(self.hand_n_deck_cards)
        for consecutive_cards_set in consecutive_cards_set_list:
            if not len(consecutive_cards_set) >= 5:
                continue

            for index in range(0, len(consecutive_cards_set) - 4):
                if self.draw_possibility(consecutive_cards_set[index: index + 5]):
                    return True

        return False

    def __pair_possibility(self, no_of_pairs):
        """
        Function that determines whether given number of pairs hand is possible.
        :return: <bool> Returns True if possible else False.
        """
        same_face_cards_dict = self.get_same_face_cards(self.hand_n_deck_cards)
        pair_sets = list()
        for same_face_cards in same_face_cards_dict.itervalues():
            if len(same_face_cards) == 2:
                pair_sets.append(same_face_cards)

        if len(pair_sets) < no_of_pairs:
            return False

        drawable_pairs = list()
        for pair_set in pair_sets:
            drawable_cards = list()
            for drawable_pair in drawable_pairs:
                drawable_cards.extend(drawable_pair)

            if self.draw_possibility(pair_set + drawable_cards):
                drawable_pairs.append(pair_set)

        if len(drawable_pairs) >= no_of_pairs:
            return True

        return False

    def one_pair_possibility(self):
        """
        Function that determines whether one pair hand is possible.
        One Pair: A pair is a hand with two cards of equal rank.
        :return: <bool> Returns True if possible else False.
        """
        return self.__pair_possibility(1)

    def two_pair_possibility(self):
        """
        Function that determines whether two pair hand is possible.
        Two Pair: A pair is two cards of equal rank.
        :return: <bool> Returns True if possible else False.
        """
        return self.__pair_possibility(2)

    def best_hand_possible(self):
        """
        Function that determines which best hand is possible.
        :return: <str> Name of best hand possible.
        """
        if self.straight_flush_possible():
            return "Straight Flush"
        elif self.four_of_a_kind_possible():
            return "Four Of A Kind"
        elif self.full_house_possibility():
            return "Full House"
        elif self.flush_possibility():
            return "Flush"
        elif self.straight_possible():
            return "Straight"
        elif self.three_of_a_kind_possible():
            return "Three Of A Kind"
        elif self.two_pair_possibility():
            return "Two Pair"
        elif self.one_pair_possibility():
            return "One Pair"
        else:
            return "Highest Card"
