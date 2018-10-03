#include <iostream>


class Graph {
public:
  Graph(int m) : num_vertex(m) {
    adj_matrix = new int *[m];

    for (int i = 0; i < m; i++) {
      // somehow the allocation of the second dimension does not follow the
      // first dimension
      adj_matrix[i] = new int[m];

      // std::fill is implemented using ++first and first != last
      std::fill(&adj_matrix[i][0], &adj_matrix[i][0] + m, 0);
    }
  }

  Graph(int m, int **adj_matrix) : num_vertex(m) {
    this->adj_matrix = new int *[m];

    for (int i = 0; i < m; i++) {
      this->adj_matrix[i] = new int[m];
      std::copy(&adj_matrix[i][0], &adj_matrix[i][0] + num_vertex,
                &this->adj_matrix[i][0]);
    }
  }

  Graph(const Graph &g) : num_vertex(g.num_vertex) {
    adj_matrix = new int *[num_vertex];

    for (int i = 0; i < num_vertex; i++) {
      adj_matrix[i] = new int[num_vertex];
      std::copy(&g.adj_matrix[i][0], &g.adj_matrix[i][0] + num_vertex,
                &adj_matrix[i][0]);
    }
  }

  ~Graph() {
    for (int i = 0; i < num_vertex; i++) {
      delete[] adj_matrix[i];
    }

    delete[] adj_matrix;
  }

  friend std::ostream &operator<<(std::ostream &stream, const Graph &g) {
    for (int i = 0; i < g.num_vertex; i++) {
      for (int j = 0; j < g.num_vertex; j++) {
        stream << g.adj_matrix[i][j] << " ";
      }
      stream << std::endl;
    }
    return stream;
  }

private:
  int num_vertex;
  int **adj_matrix;
};

int main() { Graph test(10); }
