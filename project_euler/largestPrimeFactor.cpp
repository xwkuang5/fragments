#include <iostream>

long largestPrimeFactor(long number) {
    long A = number;
    long B = 2;
    long C = -1;

    while (A != 1) {
        if (A % B == 0) {
            A /= B;
            if (B > C) {
                C = B;
            }
            B = 2;
        } else {
            B += 1;
        }
    }

    return C;
}


int main() {
    std::cout << largestPrimeFactor(600851475143) << std::endl;
}
