// first-class function with boolean parameters
(define chose
    (fun (func x y)
        (if (func #t #f) x y)))
(print-num (chose (fun (x y) (and x y)) 1 -1))
