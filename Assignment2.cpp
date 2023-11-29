#include <cmath>
#include <iostream>
#include <string>
using namespace std;
int x = 0, y = 0;
int distance = 0;
int s = 0, l = 0, n = 0;
string way;
bool primality, squared;
int where( string way)
{
    for ( int i = l - 1; i >= 0; i--){
        if ( way[i] > 60){
            s = 0;
            n = 0;
            if ( way[i] == 'U') { y = y + s;};
            else if ( way[i] == 'D') { y = y - s;};
            else if ( way[i] == 'R') { x = x + s;};
            else if ( way[i] == 'L') { x = x - s;};
        }
        else {
            n += 1;
            s = s + (way[i] - 48)*pow( 10, n-1);
        };
    };
    distance = sqrt( x*x + y*y);
    




    distance

}
bool isPrime(int n)
{
    /*TODO: add your code here*/
    
}
bool isSquared(int n)
{
    /*TODO: add your code here*/
    
}
int main()
{
    cin >> way;
    l = way.length();
    where( way);

    cout << "Khoang cach xe da di chuyen tu vi tri ban dau toi diem hien tai: "
        << distance << '\n';
    if (primality) {
        cout << "So " << distance << " la so nguyen to\n";
    }
    if (squared) {
        cout << "So " << distance << " la so chinh phuong\n";
    }
    return 0;
}
