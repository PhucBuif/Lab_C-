#include <cmath>
#include <iostream>
#include <string>
using namespace std;
int x = 0, y = 0;
float d = 0;
int s = 0, l = 0, n = 0;
string way;
bool primality, squared;
void where( string way)
{
    for ( int i = l - 1; i >= 0; i--){
        if ( way[i] > 60){
            if ( way[i] == 'U') { y = y + s;}
            else if ( way[i] == 'D') { y = y - s;}
            else if ( way[i] == 'R') { x = x + s;}
            else if ( way[i] == 'L') { x = x - s;}
            s = 0;
            n = 0;
        }
        else {
            n += 1;
            s = s + (way[i] - 48)*pow( 10, n-1);
        };
    };
    d = round( sqrt( x*x + y*y));
}
bool isPrime (int d)
{
    if ( d == 2) primality = true;
    for ( int i = 2; i < d; i++){
        if ( d%i == 0){
            break;
        };
        primality = true;
    };
    
}
bool isSquared (int d)
{
    if ( sqrt( d) == (int)sqrt( d) )
    squared = true;
}
int main()
{
    cin >> way;
    l = way.length();
    where( way);
    cout << "Khoang cach xe da di chuyen tu vi tri ban dau toi diem hien tai: "
        << d << '\n';
    isSquared( d);
    isPrime( d);
    if ( primality) {
        cout << "So " << d << " la so nguyen to\n";
    }
    else if ( squared) {
        cout << "So " << d << " la so chinh phuong\n";
    }
    return 0;
}
