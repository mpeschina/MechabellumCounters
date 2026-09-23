
S = 5 # unit wins, >95% HP left with nearly no damage
A = 4 # unit wins, 60-95% HP left
B = 3 # unit wins, 10-60% HP left
C = 2 # unit wins, <10% HP left
D = 1 # unit loose, Opponent is damaged
E = 0 # unit loose, Opponent >95% HP
unit_matrix = {
    "Crawler":      [C, C, E, B, A, E, E, B, D, A, S, E, E, D, A, B, A, E, B, E, A, A, D, E, E, B, E, D, E, E, C, B, A], 
# done above!
    "Fang":         [D, C, D, C, A, E, B, D, D, C, E, A, B, D, D, D, A, E, D, E, C, B, D, B, B, D, D, D, E, E, D],
    "Hound":        [A, A, C, D, D, D, E, C, D, D, B, E, E, D, C, D, D, E, D, D, D, C, D, E, E, D, E, D, D, D, D],
    "Void Eye":     [D, D, A, C, D, D, E, C, B, D, B, E, E, B, C, C, A, E, C, D, D, B, D, E, E, D, E, D, A, C, C],
    "Marksman":     [D, D, B, B, C, S, D, D, D, D, D, S, D, B, D, D, S, A, C, B, D, D, D, D, A, D, D, D, A, C, D],
    "Arclight":     [S, S, B, C, E, C, E, A, D, D, E, E, E, D, D, D, D, E, E, D, E, E, D, E, E, E, E, D, D, D, D],
    "Wasp":         [S, D, S, D, C, S, C, D, S, S, S, B, D, S, S, A, S, E, S, S, S, B, S, B, B, A, D, A, S, D, D],
    "Mustang":      [D, B, D, D, B, D, B, C, E, E, D, A, C, D, D, D, B, D, D, E, D, D, D, B, B, D, D, B, D, D, D],
    "Sledgehammer": [A, A, B, D, C, A, E, S, C, D, B, E, E, D, D, D, B, E, E, D, E, D, D, E, E, E, E, D, D, B, D],
    "Steelballs":   [D, D, B, B, B, A, E, A, B, C, A, E, E, B, C, A, E, E, D, B, C, B, D, E, E, D, E, B, B, A, C],
    "Stormcaller":  [D, S, D, D, B, S, E, C, D, D, C, E, E, B, B, E, S, E, S, A, B, A, E, E, E, D, E, C, D, A, D],
    "Phoenix":      [S, E, S, S, D, S, D, D, S, A, S, C, D, S, S, S, S, A, S, S, S, D, S, D, B, A, D, S, S, B, D],
    "Phantom Ray":  [A, D, S, S, C, S, C, D, S, S, S, C, C, S, S, S, S, A, S, S, S, D, S, D, C, A, D, S, S, B, D],
    "Tarantula":    [A, A, B, D, D, B, E, B, B, D, D, E, E, C, D, D, C, E, D, B, D, D, D, E, E, D, E, D, B, A, C],
    "Sabertooth":   [D, C, D, D, C, A, E, B, B, D, D, E, E, A, C, B, A, E, B, A, D, D, D, E, E, D, E, D, A, A, A],
    "Rhino":        [C, C, B, D, C, A, E, B, B, D, S, E, E, B, D, C, A, E, A, A, D, E, D, E, E, E, E, D, A, A, A],
    "Hacker": 		[D, E, C, D, E, B, E, D, D, S, E, E, E, D, D, D, C, E, D, D, E, D, D, E, E, E, E, D, A, A, D],
    "Wraith": 	    [S, B, S, S, D, S, S, B, S, A, S, D, D, A, A, A, S, C, A, A, A, E, A, D, D, A, D, A, S, D, D],
    "Scorpion":     [D, A, A, D, D, A, E, A, A, S, D, E, E, B, D, D, A, E, C, S, D, D, D, E, E, D, E, D, S, S, B],
    "Vulcan": 	    [S, S, A, B, D, B, E, S, B, D, D, E, E, D, D, D, C, E, D, C, D, D, D, E, E, D, E, D, A, B, D],
    "Fortress":     [D, D, C, C, B, S, E, C, A, D, D, E, E, A, C, A, S, E, B, A, C, E, D, E, E, D, E, D, S, A, A],
    "Melting Point":[D, D, D, D, C, A, D, C, B, D, D, B, B, A, B, S, S, S, A, S, S, C, B, A, B, B, B, B, A, A, A],
    "Sandworm":     [B, B, B, B, S, S, E, B, A, D, S, E, E, B, B, C, A, E, B, A, C, D, C, E, E, D, E, D, S, A, A],
    "Raiden":       [S, D, S, S, C, S, D, D, S, S, S, A, A, S, S, S, S, S, S, S, S, D, B, C, D, S, D, A, S, A, B],
    "Overlord":     [S, D, S, S, D, S, D, D, S, S, S, D, D, S, S, S, S, S, S, S, S, D, S, B, C, S, D, S, S, A, A],
    "War Factory":  [B, A, A, B, A, S, E, A, S, A, B, E, E, S, A, A, D, E, A, S, B, D, A, E, E, C, E, D, S, A, A],
    "Abyss":        [S, A, S, S, B, S, B, C, S, S, S, A, B, S, S, S, S, S, S, S, S, D, A, A, B, S, C, S, S, A, D],
    "Mountain":     [C, A, A, B, B, S, E, B, A, D, D, E, E, A, B, B, D, E, B, A, B, D, B, E, E, B, D, C, S, A, C],
    "Fire Badger":  [S, S, B, D, D, B, E, A, C, D, A, E, E, D, D, D, D, E, E, D, E, D, D, E, E, E, E, E, C, B, D],
    "Typhoon":      [A, S, B, D, D, C, S, B, D, D, D, D, D, B, D, E, D, C, E, D, D, D, D, D, D, D, D, C, D, C, D],
    "Farseer":      [C, A, A, D, C, A, A, B, B, D, D, C, C, D, D, D, B, A, D, B, D, D, D, D, D, D, C, D, B, C, C],
    "Vortex":       [C, A, A, D, C, A, A, B, B, D, D, C, C, D, D, D, B, A, D, B, D, D, D, D, D, D, C, D, B, C, C],
    "Centurion":    [C, A, A, D, C, A, A, B, B, D, D, C, C, D, D, D, B, A, D, B, D, D, D, D, D, D, C, D, B, C, C],
}

