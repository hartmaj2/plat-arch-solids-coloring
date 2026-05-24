// orbits.cpp
//
// C++ port of Code/claude_rel_aut_classes_direct.py.
//
// Counts the number of proper q-colorings of a graph G modulo
// Aut(G) x S_q.
//
// Pipeline (same as the Python version):
//   1. Read the graph from a JSON file (only the "edges" array is used).
//   2. Compute Aut(G) by backtracking with Weisfeiler-Lehman vertex
//      invariants.
//   3. Enumerate every color-canonical SURJECTIVE proper q-coloring by
//      DFS over a greedy vertex order (collapses the S_q action).
//   4. Reduce the resulting set of colorings under Aut(G) by mapping
//      each one to its lex-smallest color-canonical image (parallel
//      with OpenMP if available).
//
// No external libraries are required. A tiny hand-written JSON parser
// extracts the "edges" array; everything else is plain C++17.

#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>
#include <thread>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using std::vector;
using std::string;
using std::cout;
using std::cerr;
using Clock = std::chrono::steady_clock;

static double seconds_since(Clock::time_point t0) {
    using namespace std::chrono;
    return duration_cast<duration<double>>(Clock::now() - t0).count();
}

// ---------------- Graph ----------------

struct Graph {
    int n = 0;
    vector<vector<int>> adj;          // adjacency lists
    vector<vector<uint64_t>> bits;    // adjacency bitsets
    int words = 0;

    void init(int n_) {
        n = n_;
        words = (n + 63) / 64;
        adj.assign(n, {});
        bits.assign(n, vector<uint64_t>(words, 0));
    }

    void add_edge(int u, int v) {
        if (u == v) return;
        if (has_edge(u, v)) return;
        adj[u].push_back(v);
        adj[v].push_back(u);
        bits[u][v / 64] |= 1ULL << (v % 64);
        bits[v][u / 64] |= 1ULL << (u % 64);
    }

    bool has_edge(int u, int v) const {
        return (bits[u][v / 64] >> (v % 64)) & 1ULL;
    }
};

// ---------------- JSON edge parser ----------------

// Extracts the value of the "edges" key, which is expected to be an
// array of two-element integer arrays, e.g. [[0,1],[0,2],...].
// Robust enough for the JSON files in Code/JsonGraphs.
static vector<std::pair<int, int>> parse_edges_json(const string &path) {
    std::ifstream f(path);
    if (!f) {
        cerr << "cannot open: " << path << "\n";
        std::exit(1);
    }
    std::stringstream ss;
    ss << f.rdbuf();
    string s = ss.str();

    size_t p = s.find("\"edges\"");
    if (p == string::npos) {
        cerr << "no \"edges\" key in " << path << "\n";
        std::exit(1);
    }
    p = s.find('[', p);
    if (p == string::npos) {
        cerr << "no edges array in " << path << "\n";
        std::exit(1);
    }

    vector<std::pair<int, int>> edges;
    int depth = 0;
    int buf[2];
    int buf_idx = 0;
    string num;
    auto flush_num = [&]() {
        if (!num.empty()) {
            if (buf_idx < 2) buf[buf_idx] = std::stoi(num);
            buf_idx++;
            num.clear();
        }
    };
    for (size_t i = p; i < s.size(); ++i) {
        char c = s[i];
        if (c == '[') {
            depth++;
            if (depth == 2) buf_idx = 0;
        } else if (c == ']') {
            flush_num();
            if (depth == 2 && buf_idx == 2) {
                edges.emplace_back(buf[0], buf[1]);
            }
            depth--;
            if (depth == 0) break;
        } else if (c == ',') {
            flush_num();
        } else if ((c >= '0' && c <= '9') || c == '-') {
            num.push_back(c);
        }
        // whitespace and other chars ignored
    }
    return edges;
}

static Graph build_graph(const vector<std::pair<int, int>> &edges) {
    int maxv = -1;
    for (auto &e : edges) maxv = std::max({maxv, e.first, e.second});
    Graph g;
    g.init(maxv + 1);
    for (auto &e : edges) g.add_edge(e.first, e.second);
    return g;
}

// ---------------- Automorphism group ----------------

// Iterated Weisfeiler-Lehman color refinement; returns a color per
// vertex. Vertices in the same Aut(G)-orbit always share a color.
static vector<int> wl_colors(const Graph &g) {
    int n = g.n;
    vector<int> col(n);
    for (int v = 0; v < n; ++v) col[v] = (int)g.adj[v].size();
    while (true) {
        vector<std::pair<int, vector<int>>> sig(n);
        for (int v = 0; v < n; ++v) {
            vector<int> nb;
            nb.reserve(g.adj[v].size());
            for (int u : g.adj[v]) nb.push_back(col[u]);
            std::sort(nb.begin(), nb.end());
            sig[v] = {col[v], std::move(nb)};
        }
        vector<int> order(n);
        for (int i = 0; i < n; ++i) order[i] = i;
        std::sort(order.begin(), order.end(),
                  [&](int a, int b) { return sig[a] < sig[b]; });
        vector<int> new_col(n);
        int k = 0;
        for (int i = 0; i < n; ++i) {
            if (i > 0 && sig[order[i]] != sig[order[i - 1]]) ++k;
            new_col[order[i]] = k;
        }
        if (new_col == col) break;
        col = std::move(new_col);
    }
    return col;
}

// Enumerate all automorphisms of g (as permutations of {0,...,n-1},
// each represented as an array a where a[i] is the image of i).
static vector<vector<int>> find_automorphisms(const Graph &g) {
    int n = g.n;
    vector<int> col = wl_colors(g);

    // group candidate images by color
    std::unordered_map<int, vector<int>> by_color;
    for (int v = 0; v < n; ++v) by_color[col[v]].push_back(v);

    // Source ordering: greedy, maximize prior-placed neighbors so that
    // subsequent branches are tightly constrained.
    vector<int> order;
    order.reserve(n);
    vector<int> placed(n, 0);
    vector<int> nb_placed(n, 0);

    auto color_size = [&](int v) {
        return (int)by_color[col[v]].size();
    };

    {
        // start at the vertex with the smallest color class, ties by
        // highest degree, ties by smallest label.
        int best = 0;
        std::tuple<int, int, int> best_key{-color_size(0), (int)g.adj[0].size(), -0};
        for (int v = 1; v < n; ++v) {
            std::tuple<int, int, int> key{-color_size(v), (int)g.adj[v].size(), -v};
            if (key > best_key) { best_key = key; best = v; }
        }
        order.push_back(best);
        placed[best] = 1;
        for (int u : g.adj[best]) ++nb_placed[u];
    }
    while ((int)order.size() < n) {
        int best = -1;
        std::tuple<int, int, int, int> best_key{};
        for (int v = 0; v < n; ++v) {
            if (placed[v]) continue;
            std::tuple<int, int, int, int> key{
                nb_placed[v], -color_size(v), (int)g.adj[v].size(), -v};
            if (best < 0 || key > best_key) { best_key = key; best = v; }
        }
        order.push_back(best);
        placed[best] = 1;
        for (int u : g.adj[best]) if (!placed[u]) ++nb_placed[u];
    }

    vector<vector<int>> auts;
    vector<int> img(n, -1);
    vector<int> used(n, 0);

    // bitsets accelerating consistency checks: bitset of currently
    // mapped source vertices, and of their images.
    int words = g.words;
    vector<uint64_t> src_bits(words, 0);
    vector<uint64_t> dst_bits(words, 0);

    std::function<void(int)> dfs = [&](int k) {
        if (k == n) {
            auts.push_back(img);
            return;
        }
        int u = order[k];
        int uc = col[u];
        // For an automorphism img,
        //   (adj_bits[u] & src_bits)    mapped via img    must equal
        //   (adj_bits[v] & dst_bits)
        // We test it explicitly: for every prior source w, edge(u,w)
        // must match edge(v, img[w]). Using bitsets:
        //   popcount(adj_bits[v] & dst_bits) ==
        //   popcount(adj_bits[u] & src_bits)
        // is a fast necessary condition.
        int u_prior_nbrs = 0;
        for (int w_word = 0; w_word < words; ++w_word) {
            u_prior_nbrs += __builtin_popcountll(g.bits[u][w_word] & src_bits[w_word]);
        }

        for (int v : by_color[uc]) {
            if (used[v]) continue;
            int v_prior_nbrs = 0;
            for (int w_word = 0; w_word < words; ++w_word) {
                v_prior_nbrs += __builtin_popcountll(g.bits[v][w_word] & dst_bits[w_word]);
            }
            if (v_prior_nbrs != u_prior_nbrs) continue;

            // Full per-vertex check.
            bool ok = true;
            for (int j = 0; j < k; ++j) {
                int w = order[j];
                if (g.has_edge(u, w) != g.has_edge(v, img[w])) { ok = false; break; }
            }
            if (!ok) continue;

            img[u] = v;
            used[v] = 1;
            src_bits[u / 64] |= 1ULL << (u % 64);
            dst_bits[v / 64] |= 1ULL << (v % 64);

            dfs(k + 1);

            src_bits[u / 64] &= ~(1ULL << (u % 64));
            dst_bits[v / 64] &= ~(1ULL << (v % 64));
            used[v] = 0;
            img[u] = -1;
        }
    };
    dfs(0);
    return auts;
}

// ---------------- DFS enumeration of color-canonical colorings ----------------

// Greedy DFS vertex order, same idea as the Python `_choose_vertex_order`.
static vector<int> choose_vertex_order(const Graph &g) {
    int n = g.n;
    vector<int> deg(n);
    for (int v = 0; v < n; ++v) deg[v] = (int)g.adj[v].size();
    vector<int> placed(n, 0);
    vector<int> nb_placed(n, 0);
    vector<int> order;
    order.reserve(n);

    int first = 0;
    {
        std::tuple<int, int> best_key{deg[0], -0};
        for (int v = 1; v < n; ++v) {
            std::tuple<int, int> key{deg[v], -v};
            if (key > best_key) { best_key = key; first = v; }
        }
    }
    order.push_back(first);
    placed[first] = 1;
    for (int u : g.adj[first]) ++nb_placed[u];

    while ((int)order.size() < n) {
        int best = -1;
        std::tuple<int, int, int> best_key{};
        for (int v = 0; v < n; ++v) {
            if (placed[v]) continue;
            std::tuple<int, int, int> key{nb_placed[v], deg[v], -v};
            if (best < 0 || key > best_key) { best_key = key; best = v; }
        }
        order.push_back(best);
        placed[best] = 1;
        for (int u : g.adj[best]) if (!placed[u]) ++nb_placed[u];
    }
    return order;
}

// Enumerate every color-canonical SURJECTIVE proper q-coloring,
// storing the results flat: out has size #colorings * n. The i-th
// vertex of the k-th coloring is at out[k*n + i] (indexed by original
// vertex labels, so it is directly comparable with permutations).
static void enumerate_canonical_colorings(const Graph &g, int q,
                                          vector<int8_t> &out) {
    out.clear();
    int n = g.n;
    if (n == 0) {
        return;
    }
    if (q < 1) return;

    vector<int> order = choose_vertex_order(g);
    vector<int> pos(n, 0);
    for (int k = 0; k < n; ++k) pos[order[k]] = k;

    // prior_nbrs[k] = list of positions j < k with order[j] ~ order[k]
    vector<vector<int>> prior_nbrs(n);
    for (int k = 0; k < n; ++k) {
        int v = order[k];
        for (int u : g.adj[v]) {
            if (pos[u] < k) prior_nbrs[k].push_back(pos[u]);
        }
    }

    vector<int8_t> by_pos(n, 0);
    vector<int8_t> arr(n, 0);

    std::function<void(int, int)> dfs = [&](int k, int max_used) {
        if (k == n) {
            if (max_used == q - 1) {
                for (int kk = 0; kk < n; ++kk) arr[order[kk]] = by_pos[kk];
                size_t off = out.size();
                out.resize(off + n);
                std::memcpy(out.data() + off, arr.data(), n);
            }
            return;
        }
        int remaining = n - k;
        int needed = (q - 1) - max_used;
        if (needed > remaining) return;

        uint64_t used_mask = 0;
        for (int j : prior_nbrs[k]) used_mask |= 1ULL << by_pos[j];

        int limit = max_used + 1;
        if (limit > q - 1) limit = q - 1;
        for (int c = 0; c <= limit; ++c) {
            if (used_mask & (1ULL << c)) continue;
            by_pos[k] = (int8_t)c;
            int new_max = c > max_used ? c : max_used;
            dfs(k + 1, new_max);
        }
    };
    dfs(0, -1);
}

// ---------------- Orbit reduction ----------------

// Compute the lex-smallest color-canonical image of `coloring` under
// `auts`, write it to `best`. Uses prefix comparison to skip work.
static inline void canon_rep(const int8_t *coloring,
                             int n, int q,
                             const vector<vector<int>> &auts,
                             int8_t *best,
                             int8_t *tmp,
                             int8_t *mapping) {
    bool have_best = false;
    for (const auto &sigma_v : auts) {
        const int *sigma = sigma_v.data();
        std::fill(mapping, mapping + q, (int8_t)-1);
        int nxt = 0;
        bool better = !have_best;  // first permutation always wins
        bool decided = false;
        for (int i = 0; i < n; ++i) {
            int8_t c = coloring[sigma[i]];
            int8_t m = mapping[(int)c];
            if (m < 0) {
                mapping[(int)c] = (int8_t)nxt;
                m = (int8_t)nxt;
                ++nxt;
            }
            tmp[i] = m;
            if (have_best && !decided) {
                if (m < best[i]) { better = true; decided = true; }
                else if (m > best[i]) { better = false; decided = true; break; }
            }
        }
        if (better) {
            std::memcpy(best, tmp, n);
            have_best = true;
        }
    }
}

// Reduce `colorings` (flat, n per row) under `auts` and return the
// number of distinct orbit representatives. Parallel via OpenMP.
static size_t count_orbits(const vector<int8_t> &colorings,
                           int n, int q,
                           const vector<vector<int>> &auts) {
    size_t ncols = n == 0 ? 0 : colorings.size() / (size_t)n;
    if (ncols == 0) return 0;

    int nthreads = 1;
#ifdef _OPENMP
    nthreads = omp_get_max_threads();
#endif
    vector<std::unordered_set<string>> local(nthreads);

#pragma omp parallel
    {
        int tid = 0;
#ifdef _OPENMP
        tid = omp_get_thread_num();
#endif
        vector<int8_t> tmp(n), best(n);
        vector<int8_t> mapping(q, -1);
        auto &S = local[tid];

#pragma omp for schedule(static)
        for (long long idx = 0; idx < (long long)ncols; ++idx) {
            const int8_t *c = colorings.data() + (size_t)idx * n;
            canon_rep(c, n, q, auts, best.data(), tmp.data(), mapping.data());
            S.emplace(string((const char *)best.data(), n));
        }
    }

    std::unordered_set<string> all;
    for (auto &S : local) {
        for (auto &s : S) all.insert(std::move(const_cast<string &>(s)));
        S.clear();
    }
    return all.size();
}

// ---------------- High-level API ----------------

struct Stats {
    size_t num_auts = 0;
    size_t num_canonical = 0;
    size_t num_orbits = 0;
    double t_auts = 0;
    double t_enum = 0;
    double t_orbits = 0;
    double t_total = 0;
};

static Stats compute_num_orbits_direct(const Graph &g, int q, bool verbose) {
    Stats st;
    auto t0 = Clock::now();

    auto t1 = Clock::now();
    auto auts = find_automorphisms(g);
    st.t_auts = seconds_since(t1);
    st.num_auts = auts.size();

    auto t2 = Clock::now();
    vector<int8_t> colorings;
    enumerate_canonical_colorings(g, q, colorings);
    st.t_enum = seconds_since(t2);
    st.num_canonical = g.n == 0 ? 0 : colorings.size() / (size_t)g.n;

    if (verbose) {
        std::printf("automorphisms:                   %10zu  (%.3fs)\n",
                    st.num_auts, st.t_auts);
        std::printf("color-canonical proper colorings:%10zu  (%.3fs)\n",
                    st.num_canonical, st.t_enum);
        std::fflush(stdout);
    }

    auto t3 = Clock::now();
    st.num_orbits = count_orbits(colorings, g.n, q, auts);
    st.t_orbits = seconds_since(t3);

    st.t_total = seconds_since(t0);

    if (verbose) {
        std::printf("orbit representatives:           %10zu  (%.3fs)\n",
                    st.num_orbits, st.t_orbits);
        std::printf("total:                                       %.3fs\n",
                    st.t_total);
        std::fflush(stdout);
    }
    return st;
}

// ---------------- CLI ----------------

namespace fs = std::filesystem;

static fs::path find_solid_json(const string &solid_name) {
    // Search a few likely roots: cwd, parent (CCode/..) and a few
    // common relative paths.
    vector<fs::path> roots = {
        fs::current_path(),
        fs::current_path() / "..",
        fs::current_path() / ".." / "Code",
        fs::current_path() / "Code",
    };
    for (const auto &root : roots) {
        for (const char *sub :
             {"Code/JsonGraphs/Platonic", "Code/JsonGraphs/Archimedean",
              "JsonGraphs/Platonic", "JsonGraphs/Archimedean"}) {
            fs::path p = root / sub / (solid_name + ".json");
            std::error_code ec;
            if (fs::exists(p, ec)) return fs::canonical(p, ec);
        }
    }
    return {};
}

static void usage(const char *prog) {
    cerr << "Usage:\n"
         << "  " << prog << " <path-to-json> <q>\n"
         << "  " << prog << " --solid <name> <q>\n"
         << "  " << prog << " --test                 (Platonic batch, q=2..8)\n";
}

static int run_single(const string &json_path, int q) {
    auto edges = parse_edges_json(json_path);
    Graph g = build_graph(edges);
    cout << "graph: " << json_path << "  (n=" << g.n
         << ", m=" << edges.size() << ")\n";
    cout << "q = " << q << "\n";
    Stats st = compute_num_orbits_direct(g, q, /*verbose=*/true);
    cout << "num_classes = " << st.num_orbits << "\n";
    cout << "wall time   = " << st.t_total << "s\n";
    return 0;
}

static int run_test() {
    const vector<string> solids = {"tetrahedron", "octahedron", "cube", "icosahedron"};
    const vector<int> qs = {2, 3, 4, 5, 6, 7, 8};

    struct Row { string solid; int q; size_t classes; double t; };
    vector<Row> rows;

    for (const auto &name : solids) {
        fs::path p = find_solid_json(name);
        if (p.empty()) {
            cerr << "cannot find JSON for " << name << " - run from CCode/ or the workspace root\n";
            return 1;
        }
        auto edges = parse_edges_json(p.string());
        Graph g = build_graph(edges);
        for (int q : qs) {
            cout << "--- " << name << ", q=" << q << " ---\n";
            auto t0 = Clock::now();
            Stats st = compute_num_orbits_direct(g, q, /*verbose=*/true);
            double elapsed = seconds_since(t0);
            cout << name << " q=" << q << ": num_classes=" << st.num_orbits
                 << ", time=" << elapsed << "s\n\n";
            rows.push_back({name, q, st.num_orbits, elapsed});
        }
    }

    const char *out_file = "test_rel_aut_classes_direct_cpp.txt";
    std::ofstream f(out_file);
    f << std::string(60, '-') << "TEST RESULTS" << std::string(60, '-') << "\n";
    f << "solids: ";
    for (size_t i = 0; i < solids.size(); ++i) f << solids[i] << (i + 1 < solids.size() ? ", " : "");
    f << "\n";
    f << "q values: 2..8\n\n";
    char header[256];
    std::snprintf(header, sizeof(header), "%-14s%4s%16s%14s",
                  "solid", "q", "num_classes", "time (s)");
    f << header << "\n";
    f << std::string(std::strlen(header), '-') << "\n";
    string last;
    for (auto &r : rows) {
        if (!last.empty() && last != r.solid) f << "\n";
        char line[256];
        std::snprintf(line, sizeof(line), "%-14s%4d%16zu%14.3f",
                      r.solid.c_str(), r.q, r.classes, r.t);
        f << line << "\n";
        last = r.solid;
    }
    cout << "wrote " << out_file << "\n";
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { usage(argv[0]); return 1; }
    string a1 = argv[1];
    if (a1 == "--test") return run_test();
    if (a1 == "--solid") {
        if (argc < 4) { usage(argv[0]); return 1; }
        string name = argv[2];
        int q = std::atoi(argv[3]);
        fs::path p = find_solid_json(name);
        if (p.empty()) {
            cerr << "cannot find JSON for " << name << "\n";
            return 1;
        }
        return run_single(p.string(), q);
    }
    if (argc < 3) { usage(argv[0]); return 1; }
    return run_single(a1, std::atoi(argv[2]));
}
