function powmod(a,b,m)
    res=1 % m
    a%=m
    while b>0
        if (b&1)==1
            res=(res*a)%m
        end
        a=(a*a)%m
        b>>=1
    end
    res
end
function main()
    x::UInt32=UInt32(12345)
    sum::Int64=0
    MOD=1000000007
    for _ in 1:1000000
        x = x*UInt32(1664525)+UInt32(1013904223)
        a = Int64(x % UInt32(100000) + 2)
        x = x*UInt32(1664525)+UInt32(1013904223)
        b = Int64(x % UInt32(1000) + 2)
        sum += powmod(a,b,MOD)
    end
    println(sum)
end
main()
