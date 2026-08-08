package main
import "fmt"
func main(){
    var n int64 = 1000000000
    var s int64 = 0
    for i := int64(0); i < n; i++ { s+=i }
    fmt.Println(s)
}
