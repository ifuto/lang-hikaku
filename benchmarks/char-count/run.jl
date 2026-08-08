function main()
    a_cnt=5000000; d_cnt=2500000; sp_cnt=1500000; other=1000000
    s="a"^a_cnt * "0"^d_cnt * " "^sp_cnt * "!"^other
    alpha=0; digit=0; space=0
    for c in s
        if ('a'<=c<='z') || ('A'<=c<='Z')
            alpha+=1
        elseif '0'<=c<='9'
            digit+=1
        elseif c==' '
            space+=1
        end
    end
    println("$alpha $digit $space")
end
main()
