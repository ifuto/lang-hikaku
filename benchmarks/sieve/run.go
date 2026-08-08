package main
import "fmt"
func main() {
    const N = 10000000
    s := make([]byte, N+1)
    for i := range s { s[i] = 1 }
    s[0] = 0; s[1] = 0
    for i := 2; i*i <= N; i++ {
        if s[i] == 1 {
            for j := i*i; j <= N; j += i {
                s[j] = 0
            }
        }
    }
    cnt := 0
    for _, v := range s { cnt += int(v) }
    fmt.Println(cnt)
}
