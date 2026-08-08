package main
import "fmt"
func gcd(a,b int64) int64{ for b!=0 { a,b=b,a%b }; return a }
func main(){
    var x uint32 = 12345
    var mod uint32 = 1000000000
    var sum int64 = 0
    for i:=0;i<5000000;i++{
        x = x*1664525 + 1013904223
        a:=int64(x % mod + 1)
        x = x*1664525 + 1013904223
        b:=int64(x % mod + 1)
        sum+=gcd(a,b)
    }
    fmt.Println(sum)
}
