
S = 5 # unit wins, >95% HP left with nearly no damage
A = 4 # unit wins, 60-95% HP left
B = 3 # unit wins, 10-60% HP left
C = 2 # unit wins, <10% HP left
D = 1 # unit loose, Opponent is damaged
E = 0 # unit loose, Opponent >95% HP
unit_matrix = {
    "Crawler":      [C, C, E, B, S, B, E, E, B, D, A, E, S, E, E, D, A, B, A, E, C, B, E, A, E, A, A, D, E, E, B, E, D], 
    "Fang":         [D, C, A, C, A, B, S, A, D, E, B, E, E, A, A, D, B, B, A, D, D, D, E, B, E, C, S, D, A, A, D, D, D], 
    "Hound":        [A, A, C, E, C, E, D, E, B, D, D, D, C, E, E, D, D, D, D, E, D, D, D, D, E, D, B, D, E, E, D, E, D],
    "Void Eye":     [D, D, S, C, D, D, B, E, B, B, B, S, B, E, E, B, B, A, S, E, D, B, A, D, D, D, B, D, E, E, D, E, D],
    "Marksman":     [E, D, B, C, C, D, A, E, E, D, D, D, B, S, D, D, D, D, S, S, D, D, C, C, B, D, D, E, E, D, D, E, D],
    "Vortex":       [D, D, S, B, B, C, A, E, A, A, E, S, B, E, E, A, D, D, S, E, B, E, S, D, A, D, D, D, E, E, E, E, D],
    "Arclight":     [S, S, B, D, D, D, C, E, S, D, D, C, E, E, E, D, E, D, D, E, D, E, D, D, D, E, E, E, E, E, E, E, E],
    "Wasp":         [S, D, S, S, B, S, S, C, D, S, S, S, S, A, D, S, S, S, S, E, B, S, E, D, S, S, S, S, A, A, S, D, S],
    "Mustang":      [D, C, D, D, A, E, E, B, C, E, E, D, C, A, B, D, D, D, A, D, D, D, D, D, E, D, B, D, A, A, D, D, D],
    "Sledgehammer": [B, A, A, D, B, D, A, E, S, C, D, B, C, E, E, D, D, D, B, E, D, E, B, D, D, D, D, E, E, E, D, E, D],
    "Steelballs":   [D, D, B, D, B, B, B, E, B, A, C, A, S, E, E, A, B, A, E, E, B, D, A, A, B, B, A, A, E, E, E, E, D],
    "Fire Badger":  [S, S, B, D, E, E, C, E, S, D, E, C, B, E, E, D, E, D, A, E, D, E, D, A, D, E, D, E, E, E, E, E, E],
# done above!     ##### matrix below is broken, only use to overwrite!
    "Stormcaller  ": [E, S, D, D, D, D, S, E, D, D, E, D, C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    "Phoenix      ": [S, D, S, S, E, S, S, D, D, S, S, S, _, C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    "Phantom Ray  ": [S, D, S, S, _, S, S, _, D, S, S, S, _, _, C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    "Tarantula    ": [_, _, _, D, _, D, _, E, _, _, D, _, _, _, _, C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    "Sabertooth   ": [D, D, _, D, _, _, S, E, _, _, D, S, _, _, _, _, C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    "Rhino        ": [D, D, _, D, _, _, _, E, _, _, D, _, _, _, _, _, _, C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    "Hacker       ": [D, D, _, E, E, E, _, E, D, D, S, D, _, _, _, _, _, _, C, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    "Wraith       ": [S, _, S, S, E, S, S, S, _, S, S, S, _, _, _, _, _, _, _, C, _, _, _, _, _, _, _, _, _, _, _, _, _],
    "Farseer      ": [D, _, _, _, _, D, _, D, _, _, D, _, _, _, _, _, _, _, _, _, C, _, _, _, _, _, _, _, _, _, _, _, _],
    "Scorpion     ": [D, _, _, D, _, S, S, E, _, S, _, S, _, _, _, _, _, _, _, _, _, C, _, _, _, _, _, _, _, _, _, _, _],
    "Typhoon      ": [S, S, _, D, D, E, _, S, _, D, D, _, _, _, _, _, _, _, _, _, _, _, C, _, _, _, _, _, _, _, _, _, _],
    "Centurion    ": [D, D, _, _, D, _, _, _, _, _, D, D, _, _, _, _, _, _, _, _, _, _, _, C, _, _, _, _, _, _, _, _, _],
    "Vulcan       ": [S, S, S, _, D, D, _, E, S, _, D, _, _, _, _, _, _, _, _, _, _, _, _, _, C, _, _, _, _, _, _, _, _],
    "Fortress     ": [D, D, _, _, _, _, S, E, _, _, D, S, _, _, _, _, _, _, _, _, _, _, _, _, _, C, _, _, _, _, _, _, _],
    "Melting Point": [D, E, D, D, _, _, S, E, D, _, D, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, C, _, _, _, _, _, _],
    "Sandworm     ": [_, _, _, _, S, _, S, E, _, S, D, S, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, C, _, _, _, _, _],
    "Raiden       ": [S, D, S, S, S, S, S, D, D, S, S, S, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, C, _, _, _, _],
    "Overlord     ": [S, D, S, S, _, S, S, D, D, S, S, S, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, C, _, _, _],
    "War Factory  ": [D, _, _, _, _, S, S, E, _, _, S, S, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, C, _, _],
    "Abyss        ": [S, _, S, S, S, S, S, _, _, S, S, S, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, C, _],
    "Mountain     ": [_, _, _, _, _, _, S, E, _, _, _, S, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, C],
}



