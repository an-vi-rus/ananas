from collections import Counter




def holdem(cards: list):
    ranks = Counter([x // 4 for x in cards]).most_common()
    ranks.sort(key=lambda item: (item[1], item[0]), reverse=True)
    suits = Counter([x % 4 for x in cards]).most_common()
    straights = ({12,11,10,9,8}, {11,10,9,8,7}, {10,9,8,7,6}, {9,8,7,6,5}, {8,7,6,5,4},{7,6,5,4,3},{6,5,4,3,2},{5,4,3,2,1},{4,3,2,1,0},{3,2,1,0,12})
    
    if suits[0][1] >= 5:
        suit = suits[0][0]
        suit_cards = {x // 4 for x in cards if x % 4 == suit}
        for i in range(len(straights)):
            if straights[i] <= suit_cards: return (8, (12 - i,))
        result = list(suit_cards)
        result.sort(reverse=True)
        return (5, (*result[0:5],))
    
    result = [item[0] for item in ranks]

    if len(result) >= 5:
        s = set(result)
        for i in range(len(straights)):
            if straights[i] <= s: return (4, (12 - i,))

    if ranks[0][1] == 4: return (7, (result[0], max(result[1:])))

    if ranks[0][1] == 3:
        if ranks[1][1] > 1: return (6, (*result[0:2],))
        return (3, (*result[0:3],))
    
    if ranks[0][1] == 1: return (0, (*result[0:5],))

    if ranks[1][1] == 1: return (1, (*result[0:4],))
    
    return (2, (*result[0:2], max(result[2:])))
