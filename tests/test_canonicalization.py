from tucan.canonicalization import canonicalize_molecule
from tucan.serialization import serialize_molecule
from tucan.graph_utils import permute_molecule
import networkx as nx
import random
import pytest


def test_permutation(m):
    # Enforce permutation for graphs with at least 2 edges that aren't fully connected (i.e., complete).
    if m.number_of_edges() <= 1:
        pytest.skip("Skipping graph with less than two edges.")
    if nx.density(m) == 1:
        pytest.skip("Skipping fully connected graph.")
    permutation_seed = 0.42
    m_permu = permute_molecule(m, random_seed=permutation_seed)
    assert m.edges != m_permu.edges


def _print_graph(m: nx.Graph):
    [print(n) for n in list(m.nodes(data=True))]
    [print(n) for n in list(m.edges(data=True))]


def test_invariance(m: nx.Graph, n_runs=10, random_seed=random.random()):
    """Eindeutigkeit."""
    print("\nOriginal Graph:")
    _print_graph(m)

    m_canon = canonicalize_molecule(m.copy())
    m_serialized = serialize_molecule(m_canon)
    random.seed(random_seed)

    print("\nCanonicalized Graph:")
    _print_graph(m_canon)

    for _ in range(n_runs):
        permutation_seed = random.random()
        m_permu = permute_molecule(m.copy(), random_seed=permutation_seed)

        print("\nPermuted Graph:")
        _print_graph(m_permu)

        m_permu_canon = canonicalize_molecule(m_permu.copy())

        print("\nPermuted-and-Canonicalized Graph:")
        _print_graph(m_permu_canon)

        m_permu_serialized = serialize_molecule(m_permu_canon)
        assert m_serialized == m_permu_serialized


def test_bijection():
    """Eineindeutigkeit."""
    serializations = set()
    for f in pytest.testset:
        m = pytest.filereader(f)
        m_serialized = serialize_molecule(canonicalize_molecule(m))
        assert m_serialized not in serializations, f"duplicate: {f.stem}"
        serializations.add(m_serialized)
