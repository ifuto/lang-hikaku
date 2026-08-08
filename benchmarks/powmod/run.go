package main
import "fmt"
func powmod(a,b,m int64) int64{
    res:=int64(1 % m)
    a%=m
    for b>0 {
        if b&1==1 { res=(res*a)%m }
        a=(a*a)%m
        b>>=1
    }
    return res
}
func main(){
    var x uint32 = 12345
    var sum int64 = 0
    const MOD int64 = 1000000007
    for i:=0;i<1000000;i++{
        x = x*1664525 + 1013904223
        a:=int64(x%100000+2)
        x = x*1664525 + 1013904223
        b:=int64(x%1000+2)
        sum+=powmod(a,b,MOD)
    }
    fmt.Println(sum)
}
