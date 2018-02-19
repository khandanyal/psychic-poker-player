class Card(object):
    """
    Class of cards representing and checking the following constraints:
    Each card is represented as a two-character code. The first character is the
    face-value (A=Ace, 2-9, T=10, J=Jack, Q=Queen, K=King) and the second character is the
    suit (C=Clubs, D=Diamonds, H=Hearts, S=Spades).
    """
    FACE_VALUES = ["T", "J", "Q", "K", "A"] + map(lambda num: str(num), range(2, 10))
    SUIT_VALUES = ["C", "D", "H", "S"]
    FACE_RANKS = {"A": 1, "K": 13, "Q": 12, "J": 11}

    def __init__(self, value):
        """
        Initializer for cards object
        :param value: <str> Two-Character code for cards
        """
        assert isinstance(value, basestring), \
            "Invalid parameter 'value'. Should be of type string"

        assert len(value) == 2, \
            "Invalid parameter 'value': {value}. The character code should contain two characters".format(value=value)

        self.face = value[0]
        self.suit = value[1]

        assert self.face.upper() in self.FACE_VALUES, \
            "Invalid parameter 'value': {value}. Face value should be one of [{valid_fvs}], Given: {invalid_fv}".format(
                value=value, valid_fvs=', '.join(self.FACE_VALUES), invalid_fv=self.face)

        assert self.suit.upper() in self.SUIT_VALUES, \
            "Invalid parameter 'value': {value}. Suit value should be one of [{valid_svs}], Given: {invalid_sv}".format(
                value=value, valid_svs=', '.join(self.SUIT_VALUES), invalid_sv=self.suit)

    @property
    def is_face_card(self):
        """
        Property that returns True if the card is a Facecard (Jack, Queen, King or Ace) else False
        :return: <bool>
        """
        return self.face.isalpha() and not self.face.upper() == "T"

    @property
    def is_number_card(self):
        """
        Property that returns True if the card is a numbered card (2-10) else False
        :return: <bool>
        """
        return self.face.isdigit() or self.face.upper() == "T"

    @property
    def rank(self):
        """
        Property that returns the rank of cards as Integer
        :return: <int>
        """
        if self.is_face_card:
            return self.FACE_RANKS[self.face.upper()]

        return int(self.face) if self.face.isdigit() else 10

    def __eq__(self, other):
        assert isinstance(other, Card), "Invalid comparison of Card with {}".format(type(other).__name__)
        return self.face == other.face and self.suit == other.suit
