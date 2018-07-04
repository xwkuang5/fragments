#ifndef SKIP_LIST_SKIP_NODE_H
#define SKIP_LIST_SKIP_NODE_H

template <class Key, class Obj>
class SkipList;
 
template <class Key, class Obj>
class SkipNode {
  public:
    SkipNode(Key* key, Obj* obj, int height);
    SkipNode(int height);
    ~SkipNode();
 
    Key* get_key() { return key_; }
    Obj* get_obj() { return obj_; }
    int get_height() { return node_height; }
    SkipNode** forward_nodes;
 
  private:
    int node_height;
    Key* key_;
    Obj* obj_;
};

template <class Key, class Obj>
SkipNode<Key, Obj>::SkipNode(Key* key, Obj* obj, int height) : key_(key), obj_(obj), node_height(height) {
  forward_nodes = new SkipNode*[node_height + 1]; 
  for (int i = 1; i <= height; i++) {
    forward_nodes[i] = nullptr;
  }
}

template <class Key, class Obj>
SkipNode<Key, Obj>::SkipNode(int height) : key_(nullptr), obj_(nullptr), node_height(height) {
  forward_nodes = new SkipNode*[node_height + 1]; 
  for (int i = 1; i <= height; i++) {
    forward_nodes[i] = nullptr;
  }
}

template <class Key, class Obj>
SkipNode<Key, Obj>::~SkipNode() {
  delete key_;
  delete obj_;
  delete [] forward_nodes;
}

#endif
