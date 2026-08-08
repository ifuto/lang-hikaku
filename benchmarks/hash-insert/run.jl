function main()
    N=1_000_000
    t=Dict{String,Int}()
    sizehint!(t,N)
    for i in 0:N-1
        t[string("k", lpad(string(i),7,'0'))]=i
    end
    println(N)
end
main()
