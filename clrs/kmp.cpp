#include <iostream>
#include <vector>
#include <string>

std::vector<int> longest_prefix_suffix(const std::string& pattern) {
    int i, len;
    std::vector<int> lps = std::vector<int>(pattern.size());
    std::fill_n(lps.begin(), lps.size(), 0);

    // length of the longest previous prefix and suffix
    len = 0;
    i = 1;

    while (i < pattern.size()) {
        // comparison always starts from 0
        if (pattern[i] == pattern[len]) {
            len += 1;
            lps[i] = len;
            i += 1;
        } else {
            if (len == 0) {
                // previous length = 0 and current character does not match
                // increment i (implicitly set lps[i] to 0)
                i += 1;
            } else {
                // previous length != 0 and current character does not match
                // decrease length (do not update i) and see if there's a match
                len = lps[len-1];
            }
        }
    }

    return lps;
}

int main() {
    std::string test_pattern = "abab";
    std::vector<int> result = longest_prefix_suffix(test_pattern);
    for (std::vector<int>::iterator it = result.begin(); it != result.end(); it++) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
}