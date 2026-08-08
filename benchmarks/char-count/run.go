package main
import "fmt"
func main(){
    a_cnt:=5000000; d_cnt:=2500000; sp_cnt:=1500000; other:=1000000
    b:=make([]byte,0,10000000)
    for i:=0;i<a_cnt;i++{ b=append(b,'a') }
    for i:=0;i<d_cnt;i++{ b=append(b,'0') }
    for i:=0;i<sp_cnt;i++{ b=append(b,' ') }
    for i:=0;i<other;i++{ b=append(b,'!') }
    var alpha,digit,space int64
    for _,c:=range b{
        if (c>='a'&&c<='z')||(c>='A'&&c<='Z'){ alpha++ }
        else if c>='0'&&c<='9'{ digit++ }
        else if c==' '{ space++ }
    }
    fmt.Printf("%d %d %d\n", alpha, digit, space)
}
