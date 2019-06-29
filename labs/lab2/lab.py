# NO IMPORTS ALLOWED!

import json

BACON_NUMBER = 4724


def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    """Return True if actors acted in the same film"""
    return any(id_1 == actor_id_1 and id_2 == actor_id_2
               or id_1 == actor_id_2 and id_2 == actor_id_1
               for id_1, id_2, _ in data)


def invert_dict(dict):
    """Create a new dictionary, where keys are dict.values and otherwise"""
    return {v: k for k, v in dict.items()}


def get_value(dict, key):
    """Return a dict value by the key"""
    return dict[key]


def get_actor_graph(data):
    """Create a graph of actors by acting together"""
    actor_graph = {}
    for id1, id2, _ in data:
        actor_graph.setdefault(id1, set()).add(id2)
        actor_graph.setdefault(id2, set()).add(id1)
    return actor_graph


def get_actors_with_bacon_number(data, n):
    """Return a set of actors with Bacon Number of n"""
    result = {BACON_NUMBER}
    closed = set()
    graph = get_actor_graph(data)
    for _ in range(n):
        closed |= result
        for i in result.copy():
            result |= graph[i]
        result -= closed
        if not result:
            break
    return result


def get_bacon_path(data, actor_id):
    """Return path from Bacon to actor"""
    graph = get_actor_graph(data)
    fringe = {BACON_NUMBER}
    next_fringe = set()
    paths = {BACON_NUMBER: [BACON_NUMBER]}
    if actor_id == BACON_NUMBER:
        return paths[BACON_NUMBER]
    while fringe:
        for node in fringe:
            children = graph[node]
            if actor_id in children:
                return paths[node] + [actor_id]
            for child in children:
                if child not in paths:
                    next_fringe.add(child)
                    paths[child] = paths[node] + [child]
        fringe = next_fringe
        next_fringe = set()


def get_path(data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")


if __name__ == '__main__':
    with open('resources/small.json') as f:
        smalldb = json.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    with open('resources/names.json') as f:
        names = json.load(f)
    ids = invert_dict(names)

    print(f"Jerome Savary's ID number is {names['Jerome Savary']}")
    print(f"{ids[1085707]} has the ID 1085707")

    print("Geena Davis and David Clennon acted together? It is",
          did_x_and_y_act_together(smalldb,
                                   get_value(names, "Geena Davis"),
                                   get_value(names, "David Clennon")))
    print("Christopher Showerman and Lew Knopp acted together? It is",
          did_x_and_y_act_together(smalldb,
                                   get_value(names, "Christopher Showerman"),
                                   get_value(names, "Lew Knopp")))

    with open('resources/large.json') as f:
        largedb = json.load(f)

    bacon_6 = ', '.join(get_value(ids, actor_id)
                        for actor_id in get_actors_with_bacon_number(largedb, 6))
    print(f"Actors with Bacon Number of 6 are: {bacon_6}")

    path_to_miller = [get_value(ids, actor_id)
                      for actor_id in get_bacon_path(largedb, get_value(names, "Rube Miller"))]
    print("Path from Kevin Bacon to Rube Miller is:", path_to_miller)