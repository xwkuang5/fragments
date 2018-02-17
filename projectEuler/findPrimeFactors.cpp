#include <iostream>
#include <vector>
#include <math.h>

std::vector<int> findPrimeFactors(long num) {
    std::vector<int> ret = std::vector<int>();
    // step 1 - Find all even factors
    while (num % 2 == 0) {
        ret.push_back(2);
        num /= 2;
    }
    // step 2 - Find all odd factors
    // we do this by incrementally finding the least prime factor
    int sqrt_num = int(sqrt(num));
    int i = 3;
    while (true) {
        if (i > sqrt(num)) {
            break;
        }

        while (num % i == 0) {
            ret.push_back(i);
            num /= i;
        }

        // each odd prime number must be 2-number away otherwise one of them will be even
        i += 2;
    }

    // step 3 - if input number is a prime number greater than 2
    if (num > 2) {
        ret.push_back(num);
    }

    return ret;
}

int main() {
    std::vector<int> ret = findPrimeFactors(600851475143);

    for (int i = 0; i < ret.size(); i++) {
        std::cout << ret[i] << " ";
    }

    std::cout << std::endl;
}
