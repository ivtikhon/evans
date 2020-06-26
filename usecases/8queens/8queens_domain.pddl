(define (domain EIGHTQUEENS)
    (:requirements :adl)
    (:types queen cell)
    (:predicates
        (queen_placed ?q - queen ?c - cell)
        (path_exists ?from ?to - cell)
    )
    (:action place_queen
        :parameters (?q - queen ?c - cell)
        :precondition (and 
            (not (queen_placed ?q ?c))
            (not 
                (exists (and
                            (?c1 - cell)
                            (?q1 - queen)
                        )
                        (and
                                (path_exists ?c ?c1)
                                (queen_placed ?q1 ?c1)
                        )
                    )
                )
            )
        :effect (queen_placed ?q ?c)
    )
)
