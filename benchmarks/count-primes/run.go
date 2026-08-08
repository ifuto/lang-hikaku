package main
import "fmt"
func isPrime(n int) bool{
    if n<2 {return false}
    if n%2==0 {return n==2}
    for d:=3; d*d<=n; d+=2 { if n%d==0 {return false} }
    return true
}
func main(){
    N:=300000
    cnt:=0
    for i:=2;i<=N;i++ { if isPrime(i) {cnt++} }
    fmt.Println(cnt)
}
