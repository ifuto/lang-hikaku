package main
import "fmt"
func main() {
    const N = 300
    var x uint32 = 12345
    var a [300][300]int64
    var b [300][300]int64
    var c [300][300]int64
    for i:=0;i<N;i++ {
        for j:=0;j<N;j++ {
            x = x*1664525 + 1013904223
            a[i][j] = int64(x % 100)
        }
    }
    for i:=0;i<N;i++ {
        for j:=0;j<N;j++ {
            x = x*1664525 + 1013904223
            b[i][j] = int64(x % 100)
        }
    }
    for i:=0;i<N;i++ {
        for k:=0;k<N;k++ {
            aik := a[i][k]
            for j:=0;j<N;j++ {
                c[i][j] += aik * b[k][j]
            }
        }
    }
    var s int64 = 0
    for i:=0;i<N;i++ { for j:=0;j<N;j++ { s+=c[i][j] } }
    fmt.Println(s)
}
