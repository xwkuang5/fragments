#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <stack>
#include <queue>

using namespace std;

class Node {
private:
    int *board;
    int blank_pos;
    Node *parent;

public:
    Node(int *board) : parent(NULL) {
        this->board = new int[9];
        for (int i = 0; i < 9; i++) {
            if (board[i] == 0) {
                blank_pos = i;
            }
            this->board[i] = board[i];
        }
    }

    Node(Node *node) : parent(node) {
        this->board = new int[9];
        for (int i = 0; i < 9; i++) {
            this->board[i] = node->board[i];
        }
        this->blank_pos = node->blank_pos;
    }

    ~Node() {
        delete [] board;
    }

    const string get_name() const {
        string ret = "";

        for (int i = 0; i < 9; i++) {
            ret = ret + to_string(this->board[i]);
        }

        return ret;
    }

    friend Node* move_left(Node *node) {
        int blank_pos = node->blank_pos;
        if (blank_pos == 0 || blank_pos == 3 || blank_pos == 6) {
            return NULL;
        }

        Node *ret = new Node(node);
        ret->board[blank_pos] = node->board[blank_pos - 1];
        ret->board[blank_pos - 1] = node->board[blank_pos];
        ret->blank_pos -= 1;
        return ret;
    }

    friend Node* move_right(Node *node) {
        int blank_pos = node->blank_pos;
        if (blank_pos == 2 || blank_pos == 5 || blank_pos == 8) {
            return NULL;
        }
        Node *ret = new Node(node); // parent already set
        ret->board[blank_pos] = node->board[blank_pos + 1];
        ret->board[blank_pos + 1] = node->board[blank_pos];
        ret->blank_pos += 1;
        return ret;
    }

    friend Node* move_up(Node *node) {
        int blank_pos = node->blank_pos;
        if (blank_pos == 0 || blank_pos == 1 || blank_pos == 2) {
            return NULL;
        }

        Node *ret = new Node(node); // parent already set
        ret->board[blank_pos] = node->board[blank_pos - 3];
        ret->board[blank_pos - 3] = node->board[blank_pos];
        ret->blank_pos -= 3;
        return ret;
    }

    friend Node* move_down(Node *node) {
        int blank_pos = node->blank_pos;
        if (blank_pos == 6 || blank_pos == 7 || blank_pos == 8) {
            return NULL;
        }

        Node *ret = new Node(node); // parent already set
        ret->board[blank_pos] = node->board[blank_pos + 3];
        ret->board[blank_pos + 3] = node->board[blank_pos];
        ret->blank_pos += 3;
        return ret;
    }

    friend vector<Node*> expand_node(Node *node, set<string>& closed_list) {
        vector<Node*> ret;

        Node *tmp = move_left(node);
        if (tmp != NULL) {
            if (closed_list.find(tmp->get_name()) == closed_list.end()) {
                ret.push_back(tmp);
            } else {
                delete tmp;
            }
        }

        tmp = move_right(node);
        if (tmp != NULL) {
            if (closed_list.find(tmp->get_name()) == closed_list.end()) {
                ret.push_back(tmp);
            } else {
                delete tmp;
            }
        }

        tmp = move_up(node);
        if (tmp != NULL) {
            if (closed_list.find(tmp->get_name()) == closed_list.end()) {
                ret.push_back(tmp);
            } else {
                delete tmp;
            }
        }

        tmp = move_down(node);
        if (tmp != NULL) {
            if (closed_list.find(tmp->get_name()) == closed_list.end()) {
                ret.push_back(tmp);
            } else {
                delete tmp;
            }
        }

        return ret;
    }

    friend bool goal_node(Node *node) {
        if (node->blank_pos == 0) {
            for (int i = 1; i < 9; i++) {
                if (node->board[i] != i) {
                    return false;
                }
            }
            return true;
        }

        if (node->blank_pos == 8) {
            for (int i = 0; i < 8; i++) {
                if (node->board[i] != i + 1) {
                    return false;
                }
            }
            return true;
        }
        return false;
    }

    friend void display(Node *node) {
        std::cout << "-------" << std::endl;
        for (int i = 0; i < 3; i++) {
            string tmp = "|";
            for (int j = i*3; j < (i+1)*3; j++) {
                tmp = tmp + to_string(node->board[j]) + "|";
            }
            std::cout << tmp << std::endl;
        }
    }

    friend Node** get_goal_path(Node *node, int &size) {
        int count = 0;
        Node *cur = node;
        while (cur != NULL) { count++; cur = cur->parent; }
        Node **ret = new Node*[count];
        size = count;
        cur = node;
        while (cur != NULL) {
            ret[--count] = cur;
            cur = cur->parent;
        }

        return ret;
    }
};

Node* depth_first_search(Node *start_state) {
    stack<Node*> fringe;
    set<string> closed_list;

    fringe.push(start_state);

    while (!fringe.empty()) {
        Node *current = fringe.top();
        std::cout << current->get_name() << std::endl;
        fringe.pop();
        if (goal_node(current)) {
            // release fringe
            return current;
        }
        closed_list.insert(current->get_name());
        const vector<Node*>& children = expand_node(current, closed_list);
        for (int i = 0; i < children.size(); i++) {
            fringe.push(children[i]);
        }
    }

    return NULL;
}

Node* breadth_first_search(Node *start_state) {
    queue<Node*> fringe;
    set<string> closed_list;

    fringe.push(start_state);

    while (!fringe.empty()) {
        Node *current = fringe.front();
        std::cout << current->get_name() << std::endl;
        fringe.pop();
        if (goal_node(current)) {
            // release fringe
            return current;
        }
        closed_list.insert(current->get_name());
        const vector<Node*>& children = expand_node(current, closed_list);
        for (int i = 0; i < children.size(); i++) {
            fringe.push(children[i]);
        }
    }

    return NULL;
}

int main() {
    int init[] = {1, 2, 3, 0, 4, 5, 6, 7, 8};
    Node *start_node = new Node(init);
    Node *goal_node = depth_first_search(start_node);

    int size;
    Node **ret = get_goal_path(goal_node, size);
    for (int i = 0; i < size; i++) {
        display(ret[i]);
    }
    std::cout << size << std::endl;
    return 0;
}