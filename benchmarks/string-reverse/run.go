package main
import "fmt"
func reverse(s []byte){
    for i,j:=0,len(s)-1; i<j; i,j=i+1,j-1 { s[i],s[j]=s[j],s[i] }
}
func main(){
    size:=10000000
    reps:=10
    b:=make([]byte, size)
    for i:=range b { b[i]='a' }
    var total int64=0
    for r:=0;r<reps;r++ { reverse(b); total+=int64(len(b)) }
    fmt.Println(total)
}
