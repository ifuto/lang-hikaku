function main()
    size=10_000_000
    reps=10
    s="a"^size
    total=0
    for _ in 1:reps
        s=reverse(s)
        total+=length(s)
    end
    println(total)
end
main()
