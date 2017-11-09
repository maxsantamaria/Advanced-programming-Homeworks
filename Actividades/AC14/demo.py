from battleship import Battleship


battle = Battleship(boardsize=5, max_ships=5, loaded=True)

print(battle.p1.board)
print(battle.p2.board)


battle.attack('P2', 'c3')  # hit --> el enemigo tiene un ship en 'c3'.
print(battle.p2.attacks)

print(battle.view_from('P1'))
print(battle.view_from('P2'))

print(battle.game_over())