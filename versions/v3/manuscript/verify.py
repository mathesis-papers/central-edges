import json
from fractions import Fraction
from itertools import combinations, permutations, product
from math import factorial


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pairs(order):
    return list(combinations(range(order), 2))


def table(order, labels):
    distances = [[Fraction(0) for column in range(order)] for row in range(order)]
    require(set(labels) == set(pairs(order)), 'all unordered pairs specified')
    for (left, right), length in labels.items():
        require(length > 0, 'strictly positive off-diagonal distances')
        distances[left][right] = distances[right][left] = Fraction(length)
    return distances


def is_metric(distances):
    order = len(distances)
    return all(
        distances[left][right] == distances[right][left]
        and distances[left][right] >= 0
        and ((distances[left][right] == 0) == (left == right))
        for left in range(order) for right in range(order)
    ) and all(
        distances[left][right] <= distances[left][middle] + distances[middle][right]
        for left in range(order) for right in range(order) for middle in range(order)
    )


def is_ultrametric(distances):
    order = len(distances)
    return is_metric(distances) and all(
        distances[left][right] <= max(distances[left][middle], distances[middle][right])
        for left in range(order) for right in range(order) for middle in range(order)
    )


def center(distances):
    return set.intersection(*(set(row) for row in distances))


def central_edges(distances):
    values = center(distances)
    return {edge for edge in pairs(len(distances)) if distances[edge[0]][edge[1]] in values}


def covers(order, edges):
    return {vertex for edge in edges for vertex in edge} == set(range(order))


def verify_central_classes(distances):
    order = len(distances)
    classes = []
    for length in center(distances) - {0}:
        edges = {edge for edge in pairs(order) if distances[edge[0]][edge[1]] == length}
        require(covers(order, edges), 'each central class covers every vertex')
        require(len(edges) >= (order + 1) // 2, 'incidence lower bound')
        require(all(edges.isdisjoint(previous) for previous in classes), 'classes disjoint')
        classes.append(edges)
    require(sum(map(len, classes)) == len(central_edges(distances)), 'central graph decomposition')


def condition_i(distances, first_part, second_part, first_root, second_root):
    order = len(distances)
    require(first_part.isdisjoint(second_part), 'partition disjoint')
    require(first_part | second_part == set(range(order)), 'partition exhaustive')
    require(min(len(first_part), len(second_part)) == 2, 'smaller part has size two')
    diameter = max(map(max, distances))
    diameter_edges = {edge for edge in pairs(order) if distances[edge[0]][edge[1]] == diameter}
    cross_edges = {tuple(sorted((left, right))) for left in first_part for right in second_part}
    stars = {
        tuple(sorted((root, vertex)))
        for part, root in [(first_part, first_root), (second_part, second_root)]
        for vertex in part if vertex != root
    }
    return diameter_edges == cross_edges and central_edges(distances) == cross_edges | stars


def four_point_check():
    half = Fraction(1, 2)
    ultrametric = [[0, 1, half, 1], [1, 0, 1, half], [half, 1, 0, 1], [1, half, 1, 0]]
    positions = [0, 4, 5, 9]
    real_metric = [[abs(left - right) for right in positions] for left in positions]
    require(is_ultrametric(ultrametric), 'four-point ultrametric')
    require(center(ultrametric) == {0, half, 1}, 'four-point ultrametric center')
    require(condition_i(ultrametric, {0, 2}, {1, 3}, 0, 1), 'four-point condition (i)')
    require(len(central_edges(ultrametric)) == 6, 'six ultrametric central edges')
    require(is_metric(real_metric) and not is_ultrametric(real_metric), 'real comparator')
    require(center(real_metric) == {0, 4, 5}, 'real comparator center')
    require(central_edges(real_metric) == {(0, 1), (0, 2), (1, 3), (2, 3)}, 'four real central edges')
    return {'ultrametric_center': ['0', '1/2', '1'], 'ultrametric_edges': 6,
            'real_metric_center': [0, 4, 5], 'real_metric_edges': 4, 'condition_i': True}


def prescribed_ultrametric(order):
    labels = {}
    for left, right in pairs(order):
        if left < 2 <= right:
            length = 2
        elif (left, right) == (0, 1) or left == 2:
            length = 1
        else:
            length = Fraction(1, 2)
        labels[left, right] = length
    return table(order, labels)


def optimal_metric(order):
    cycle = [tuple(sorted((vertex, (vertex + 1) % order))) for vertex in range(order)]
    first = set(cycle[::2])
    second = set(cycle[1::2])
    if order % 2:
        second.add((0, 2))
    require(first.isdisjoint(second), 'disjoint cycle covers')
    require(covers(order, first) and covers(order, second), 'cycle covers span')
    require(len(first) == len(second) == (order + 1) // 2, 'minimum cycle covers')
    remaining = [edge for edge in pairs(order) if edge not in first | second]
    labels = {edge: 4 for edge in first} | {edge: 5 for edge in second}
    labels.update({edge: 6 + Fraction(index + 1, len(remaining) + 1)
                   for index, edge in enumerate(remaining)})
    return table(order, labels)


def optimal_ultrametric(order):
    components = [[0, 1]]
    next_vertex = 2
    if order % 2:
        components.append([2, 3, 4])
        next_vertex = 5
    components.extend([vertex, vertex + 1] for vertex in range(next_vertex, order, 2))
    component_of = {vertex: index for index, component in enumerate(components) for vertex in component}
    labels = {}
    for left, right in pairs(order):
        if left < 2 <= right:
            length = 2
        elif component_of[left] != component_of[right]:
            length = Fraction(3, 2)
        elif order % 2 and (left, right) == (3, 4):
            length = Fraction(1, 2)
        else:
            length = 1
        labels[left, right] = length
    return table(order, labels)


def one_factorization(order):
    require(order >= 2 and order % 2 == 0, 'even order for perfect matchings')
    modulus = order - 1
    matchings = []
    for round_index in range(modulus):
        matching = {(round_index, modulus)}
        matching.update(tuple(sorted(((round_index + offset) % modulus,
                                     (round_index - offset) % modulus)))
                        for offset in range(1, order // 2))
        require(covers(order, matching) and len(matching) == order // 2, 'perfect matching')
        require(all(matching.isdisjoint(previous) for previous in matchings), 'matching partition disjoint')
        matchings.append(matching)
    require(set().union(*matchings) == set(pairs(order)), 'matching partition exhaustive')
    return matchings


def minimum_order_metric(center_size):
    if center_size == 1:
        return [[Fraction(0)]]
    order = center_size + center_size % 2
    matchings = one_factorization(order)
    labels = {edge: 1 + Fraction(index, 4 * order)
              for index, matching in enumerate(matchings[:center_size - 1]) for edge in matching}
    remaining = [edge for edge in pairs(order) if edge not in labels]
    labels.update({edge: Fraction(3, 2) + Fraction(index + 1, 4 * order)
                   for index, edge in enumerate(remaining)})
    return table(order, labels)


def finite_families():
    results = []
    for order in range(4, 33):
        prescribed = prescribed_ultrametric(order)
        metric = optimal_metric(order)
        ultrametric = optimal_ultrametric(order)
        require(is_ultrametric(prescribed), 'condition-(i) family ultrametric')
        require(condition_i(prescribed, {0, 1}, set(range(2, order)), 0, 2), 'condition-(i) family')
        require(center(prescribed) == {0, 1, 2}, 'condition-(i) family center')
        require(len(central_edges(prescribed)) == 3 * order - 6, 'condition-(i) edge count')
        require(is_metric(metric), 'optimal metric family')
        require(center(metric) == {0, 4, 5}, 'optimal metric center')
        require(len(central_edges(metric)) == 2 * ((order + 1) // 2), 'optimal metric edge count')
        require(is_ultrametric(ultrametric), 'optimal ultrametric family')
        require(center(ultrametric) == {0, 1, 2}, 'optimal ultrametric center')
        require(len(central_edges(ultrametric)) == 2 * order - 4 + (order + 1) // 2,
                'optimal ultrametric edge count')
        for distances in [prescribed, metric, ultrametric]:
            verify_central_classes(distances)
        results.append({'order': order, 'condition_i_edges': len(central_edges(prescribed)),
                        'metric_minimum': len(central_edges(metric)),
                        'ultrametric_minimum': len(central_edges(ultrametric))})
    return results


def finite_minimum_orders():
    results = []
    for center_size in range(1, 25):
        distances = minimum_order_metric(center_size)
        require(is_metric(distances), 'minimum-order metric')
        require(len(center(distances)) == center_size, 'exact center size')
        require(len(distances) == (1 if center_size == 1 else center_size + center_size % 2),
                'minimum-order construction size')
        verify_central_classes(distances)
        if center_size % 2 == 0:
            require(len(central_edges(distances)) == center_size * (center_size - 1) // 2,
                    'complete central graph for even center size')
        results.append({'center_size': center_size, 'order': len(distances)})
    return results


def minimum_covers(order):
    if order % 2 == 0:
        return one_factorization(order)
    matchings = [{edge for edge in matching if order not in edge}
                 for matching in one_factorization(order + 1)]
    reserved = matchings[0] | matchings[1]
    adjacency = {vertex: sorted(other for edge in reserved if vertex in edge
                                for other in edge if other != vertex)
                 for vertex in range(order)}
    outgoing = {}
    visited = set()
    previous, current = None, 0
    while current != 1:
        following = next(vertex for vertex in adjacency[current] if vertex != previous)
        if current != 0:
            outgoing[current] = tuple(sorted((current, following)))
        visited.add(current)
        previous, current = current, following
    visited.add(1)
    while len(visited) < order:
        previous, current = None, min(set(range(order)) - visited)
        while current not in visited:
            following = next(vertex for vertex in adjacency[current] if vertex != previous)
            outgoing[current] = tuple(sorted((current, following)))
            visited.add(current)
            previous, current = current, following
    require(set(outgoing) == set(range(2, order)), 'one outgoing edge per missing vertex')
    require(len(set(outgoing.values())) == order - 2, 'outgoing edges are distinct')
    result = [matchings[vertex] | {outgoing[vertex]} for vertex in range(2, order)]
    for index, cover in enumerate(result):
        require(covers(order, cover), 'minimum cover spans')
        require(len(cover) == (order + 1) // 2, 'minimum cover size')
        require(all(cover.isdisjoint(other) for other in result[:index]), 'minimum covers disjoint')
    return result


def all_center_sizes():
    results = []
    for order in range(3, 21):
        cover_family = minimum_covers(order)
        rows = []
        for center_size in range(1, order + 1 - order % 2):
            labels = {edge: 1 + Fraction(index, 4 * order)
                      for index, cover in enumerate(cover_family[:center_size - 1])
                      for edge in cover}
            remaining = [edge for edge in pairs(order) if edge not in labels]
            labels.update({edge: Fraction(3, 2) + Fraction(index + 1, 4 * order * order)
                           for index, edge in enumerate(remaining)})
            distances = table(order, labels)
            require(is_metric(distances), 'all-center construction is a metric')
            require(len(center(distances)) == center_size, 'all-center exact cardinality')
            edge_count = len(central_edges(distances))
            require(edge_count == (center_size - 1) * ((order + 1) // 2),
                    'all-center sharp edge count')
            verify_central_classes(distances)
            rows.append({'center_size': center_size, 'central_edges': edge_count})
        results.append({'order': order, 'cases': rows})
    return results


def word_metric(branching):
    words = list(product(*(range(count) for count in branching)))
    return [[0 if left == right else len(branching) - next(
        index for index, (first, second) in enumerate(zip(left, right)) if first != second)
             for right in words] for left in words]


def count_isometries(distances):
    order = len(distances)
    edge_list = pairs(order)
    count = 0
    first_orbit = set()
    for permutation in permutations(range(order)):
        if all(distances[left][right] == distances[permutation[left]][permutation[right]]
               for left, right in edge_list):
            count += 1
            first_orbit.add(permutation[0])
    require(first_orbit == set(range(order)), 'isometry action transitive')
    return count


def tree_corollaries():
    binary = []
    for height in range(6):
        distances = word_metric([2] * height)
        require(is_ultrametric(distances), 'binary word ultrametric')
        require(center(distances) == set(range(height + 1)), 'binary center')
        for row in distances:
            require(row.count(0) == 1, 'singleton zero sphere')
            for level in range(1, height + 1):
                require(row.count(level) == 2 ** (level - 1), 'binary sphere counts')
        expected_group_order = 2 ** (2 ** height - 1)
        item = {'height': height, 'order': len(distances),
                'group_order_formula': expected_group_order,
                'sphere_counts': [1] + [2 ** (level - 1) for level in range(1, height + 1)]}
        if height <= 3:
            actual = count_isometries(distances)
            require(actual == expected_group_order, 'binary isometry group enumeration')
            item['enumerated_isometries'] = actual
        binary.append(item)
    regular = []
    for branching in [[3], [4], [2, 3], [3, 2], [2, 2, 2]]:
        distances = word_metric(branching)
        require(is_ultrametric(distances), 'regular word ultrametric')
        expected = 1
        nodes = 1
        for count in branching:
            expected *= factorial(count) ** nodes
            nodes *= count
        actual = count_isometries(distances)
        require(actual == expected, 'regular isometry group enumeration')
        require(actual >= 2 ** (len(distances) - 1), 'homogeneous group lower bound')
        require((actual == 2 ** (len(distances) - 1)) == all(count == 2 for count in branching),
                'homogeneous equality criterion')
        counts = [distances[0].count(level) for level in range(len(branching) + 1)]
        require(all([row.count(level) for level in range(len(branching) + 1)] == counts
                    for row in distances), 'uniform regular sphere counts')
        partial = 1
        for count in counts[1:]:
            require((partial + count) % partial == 0, 'sphere partial-sum divisibility')
            partial += count
        regular.append({'branching': branching, 'order': len(distances),
                        'enumerated_isometries': actual, 'sphere_counts': counts})
    return {'binary': binary, 'regular': regular}


def exhaustive_small_tables():
    results = []
    for order in range(2, 5):
        edges = pairs(order)
        metrics = ultrametrics = three_central_metrics = 0
        for lengths in product(range(1, 4), repeat=len(edges)):
            distances = table(order, dict(zip(edges, lengths)))
            if not is_metric(distances):
                continue
            metrics += 1
            verify_central_classes(distances)
            if len(center(distances)) == order:
                require(order % 2 == 0, 'maximal center requires even order')
            ultra = is_ultrametric(distances)
            ultrametrics += int(ultra)
            if len(center(distances)) == 3:
                three_central_metrics += 1
                require(order >= 4, 'three-central minimum order')
                if ultra:
                    require(len(central_edges(distances)) >= 2 * order - 4 + (order + 1) // 2,
                            'ultrametric lower bound in exhaustive tables')
        results.append({'order': order, 'metric_tables': metrics, 'ultrametric_tables': ultrametrics,
                        'three_central_metric_tables': three_central_metrics})
    return results


def main():
    result = {'arithmetic': 'exact integers and rational fractions',
              'four_point': four_point_check(),
              'central_edge_families': finite_families(),
              'minimum_orders': finite_minimum_orders(),
              'all_center_sizes': all_center_sizes(),
              'tree_corollaries': tree_corollaries(),
              'exhaustive_tables': exhaustive_small_tables(),
              'status': 'ALL_CHECKS_OK'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
