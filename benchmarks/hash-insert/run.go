package main
import "fmt"
func main() {
    const N = 1000000
    t := make(map[string]int, N)
    for i:=0; i<N; i++ {
        k := fmt.Sprintf("k%07d", i)
        t[k]=i
    }
    fmt.Println(N)
}
