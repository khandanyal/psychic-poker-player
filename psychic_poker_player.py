if __name__ == "__main__":
    from models import HandProcessor

    cards = raw_input(
        "Please specify 10 cards separated with a space.\nEach card is represented as a two-character code.\n"
        "The first character is the face-value (A=Ace, 2-9, T=10, J=Jack, Q=Queen, K=King) \nand the second character "
        "is the suit (C=Clubs, D=Diamonds, H=Hearts, S=Spades):\n>>")

    hand_processor = HandProcessor(cards)
    print "**Hand**: {hand_cards} **Deck**: {deck_cards} **Best hand**: {best_hand}".format(
        hand_cards=' '.join(cards.split()[:5]), deck_cards=' '.join(cards.split()[-5:]),
        best_hand=hand_processor.best_hand_possible())
