package main
import "fmt"
func main(){
    N:=1000000
    best:=1
    best_len:=0
    for i:=1;i<=N;i++{
        n:=int64(i)
        l:=0
        for n!=1{
            if n%2==0 { n/=2 } else { n=3*n+1 }
            l++
        }
        if l>best_len { best_len=l; best=i }
    }
    fmt.Println(best)
}
