(define (domain EIGHTQUEENS)
    (:requirements :adl)
    (:types queen cell)
    (:predicates
        (queen_placed ?q - queen)
        (cell_occupied ?c - cell)
        (path_exists ?from ?to - cell)
    )
    (:action place_queen
        :parameters (?q - queen ?c - cell)
        :precondition (and 
            (not (queen_placed ?q))
            (not (cell_occupied ?c))
            (not 
                (exists (?c1 - cell)(and
                        (path_exists ?c ?c1)
                        (cell_occupied ?c1)
                    )
                )
            )
        )
        :effect (and
            (queen_placed ?q)
            (cell_occupied ?c)
        )
    )
)
