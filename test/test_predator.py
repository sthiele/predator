"""Testing of the main routine.

"""

from predator import graph_from_file, search_seeds, utils, EnumMode
from predator import quoted_data


def test_basic_EnumMode_API():
    for obj in EnumMode:
        assert getattr(EnumMode, obj.value.title()) is EnumMode(obj.value)
    assert EnumMode('enumeration').clingo_option == ''
    assert EnumMode('union').clingo_option == '--enum-mode brave'
    assert EnumMode('intersection').clingo_option == '--enum-mode cautious'

def test_simple_reaction():
    graph = quoted_data('reactant(a,r). product(p,r). reaction(r).')
    # utils.render_network(graph, 'todel.png')  # uncomment to help debugging
    seeds_sets = {frozenset('a')}
    assert seeds_sets == set(search_seeds(graph))
    seeds_sets = {frozenset('a'), frozenset('p')}
    assert seeds_sets == set(search_seeds(graph, targets='p'))


def test_double_reactant_reaction():
    graph = quoted_data('reactant((a;b),r). product(p,r). reaction(r).')
    # utils.render_network(graph, 'todel.png')  # uncomment to help debugging
    seeds_sets = {frozenset('ab')}
    assert seeds_sets == set(search_seeds(graph))
    seeds_sets = {frozenset('ab'), frozenset('p')}
    assert seeds_sets == set(search_seeds(graph, targets='p'))


def test_double_reactant_with_feedback_reaction():
    graph = quoted_data('reactant((a;b),r). product(p,r). reaction(r). reactant(p,r2). product(a,r2). reaction(r2).')
    # utils.render_network(graph, 'todel.png')  # uncomment to help debugging
    expected_seeds_sets = {frozenset('ab'), frozenset('pb')}
    assert expected_seeds_sets == set(search_seeds(graph))
    expected_seeds_sets = {frozenset('abp')}
    assert expected_seeds_sets == set(search_seeds(graph, enum_mode='union'))
    expected_seeds_sets = {frozenset('b')}
    assert expected_seeds_sets == set(search_seeds(graph, enum_mode='intersection'))


def test_local_minimization():
    "Is it sure that minimizing the amount of seeds/ingoings is the right way ?"
    graph = quoted_data('reactant(a,1). product((b;c),1). reaction(1).  reactant((b;c),2). product(a,2). reaction(2).  reactant(d,3). product(b,3). reaction(3).')
    utils.render_network(graph, 'todel.png')  # uncomment to help debugging
    expected_seeds_sets = {frozenset('a')}
    assert expected_seeds_sets == set(search_seeds(graph, targets='c', forbidden_seeds='c'))
    assert expected_seeds_sets == set(search_seeds(graph, targets='c', forbidden_seeds='c', compute_optimal_solutions=True))


def test_loop():
    graph = quoted_data('reactant(a,1). product(b,1). reaction(1).  reactant(b,2). product(a,2). reaction(2).')
    # utils.render_network(graph, 'todel.png')  # uncomment to help debugging
    assert {frozenset('a'), frozenset('b')} == set(search_seeds(graph))
    assert {frozenset('ab')} == set(search_seeds(graph, enum_mode='union'))
    assert {frozenset()} == set(search_seeds(graph, enum_mode='intersection'))


def test_and_or():
    graph = quoted_data('reactant("b","r2"). reactant("c","r3"). reactant("a","r1"). reactant("b","r1"). reactant("c","r1"). product("c","r2"). product("b","r3"). product("d","r1"). reaction("r2"). reaction("r3"). reaction("r1").')
    # utils.render_network(graph, 'todel.png')  # uncomment to help debugging
    assert {frozenset('ab'), frozenset('ac')} == set(search_seeds(graph))
    assert {frozenset('ab'), frozenset('ac'), frozenset('d')} == set(search_seeds(graph, targets='d'))
    assert {frozenset('ab'), frozenset('ac')} == set(search_seeds(graph, targets='d', forbidden_seeds='d'))
    assert {frozenset('abc')} == set(search_seeds(graph, enum_mode='union'))
    assert {frozenset('a')} == set(search_seeds(graph, enum_mode='intersection'))


def test_with_seeds_and_forbidden():
    graph = quoted_data('reactant((a;b),1). product((d;e),1). reaction(1).  reactant((b;c),2). product((e;f),2). reaction(2).')
    # utils.render_network(graph, 'todel.png')  # uncomment to help debugging
    assert not set(search_seeds(graph, start_seeds='a', forbidden_seeds='c'))
    expected_seeds_sets = {frozenset('abc')}
    assert expected_seeds_sets == set(search_seeds(graph, start_seeds='abc', forbidden_seeds='def'))
    assert expected_seeds_sets == set(search_seeds(graph, start_seeds='c', forbidden_seeds='d', targets='d'))
