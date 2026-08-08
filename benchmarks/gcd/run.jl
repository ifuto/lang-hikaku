function gcd(a,b)
    while b!=0
        a,b=b,a%b
    end
    a
end
function main()
    x::UInt32=UInt32(12345)
    mod::UInt32=UInt32(1000000000)
    sum::Int64=0
    for _ in 1:5000000
        x = x*UInt32(1664525) + UInt32(1013904223)
        a = Int64(x % mod + 1)
        x = x*UInt32(1664525) + UInt32(1013904223)
        b = Int64(x % mod + 1)
        sum += gcd(a,b)
    end
    println(sum)
end
main()
