package main
import "fmt"
func main(){
    N:=100000
    s:=""
    // naive concat to benchmark (not using builder)
    for i:=0;i<N;i++ { s+="a" }
    fmt.Println(len(s))
}
