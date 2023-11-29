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
    d = sqrt( x*x + y*y);
}
int main (){
    cin >> way;
    l = way.length();
    where( way);
    cout << d;
}   


