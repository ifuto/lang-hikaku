function main()
    N=100000
    s=""
    for _ in 1:N
        s *= "a"
    end
    println(length(s))
end
main()
