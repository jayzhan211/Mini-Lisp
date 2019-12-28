// first-class function
(define add-x
    (fun (x)
        (fun (y) (* x y))))
(define f (add-x 5))
(print-num (f 3))
