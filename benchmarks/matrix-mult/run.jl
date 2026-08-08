function main()
    N=300
    x::UInt32=UInt32(12345)
    a=zeros(Int64,N,N)
    b=zeros(Int64,N,N)
    c=zeros(Int64,N,N)
    for i in 1:N
        for j in 1:N
            x = x*UInt32(1664525) + UInt32(1013904223)
            a[i,j]=Int64(x%UInt32(100))
        end
    end
    for i in 1:N
        for j in 1:N
            x = x*UInt32(1664525) + UInt32(1013904223)
            b[i,j]=Int64(x%UInt32(100))
        end
    end
    for i in 1:N
        for k in 1:N
            aik=a[i,k]
            for j in 1:N
                c[i,j]+=aik*b[k,j]
            end
        end
    end
    s=sum(c)
    println(s)
end
main()
