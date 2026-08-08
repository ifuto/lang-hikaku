function main()
    N = 10_000_000
    s = trues(N+1)  # s[1]=0, s[2]=1...
    s[1]=false; s[2]=false
    limit = isqrt(N)
    for i in 2:limit
        if s[i+1] # because Julia 1-indexed: s index i+1 = number i
            j = i*i
            while j <= N
                s[j+1]=false
                j+=i
            end
        end
    end
    cnt = count(s)
    println(cnt)
end
main()
