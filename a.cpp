#include <iostream>

using namespace std;
bool check(int a, int b, int c){
    return a + b > c && a + c > b && b + c > a && a + b + c == 100;
}

signed main(){
    int count = 100, res =0;
    freopen("output.txt", "w", stdout);
    for (size_t i = 1; i <= count; i++)
    {
        for (size_t j = i; j <= count; j++)
        {
            for (size_t k = j; k <= count; k++)
            {
                if(check(i, j , k)){
                    cout << i << " " << j << " " << k << endl;
                    res++;
                }
            }
            
        }
        
    }

    cout << res;
    
}

