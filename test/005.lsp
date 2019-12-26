(define fact (
    fun (x)(
        if (= x 1) 1
        (* x (fact(- x 1)))
    )))
(print-num (fact 10))

