function is_prime(n)
    n<2 && return false
    n%2==0 && return n==2
    d=3
    while d*d<=n
        n%d==0 && return false
        d+=2
    end
    true
end
function main()
    N=300000
    cnt=0
    for i in 2:N
        if is_prime(i)
            cnt+=1
        end
    end
    println(cnt)
end
main()
