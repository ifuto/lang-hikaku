function main()
    N=1000000
    best=1
    best_len=0
    for i in 1:N
        n=i
        len=0
        while n!=1
            n = n%2==0 ? n÷2 : 3*n+1
            len+=1
        end
        if len>best_len
            best_len=len
            best=i
        end
    end
    println(best)
end
main()
