import graphviz as gv
import functools
graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            print(*n[1])
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            print(*e[1])
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    return graph


import inspect
import _ast

classes = []
hierarchy_unions = []

for name, obj in inspect.getmembers(_ast):
    if inspect.isclass(obj):
      current_class = obj.__mro__[0].__name__
      superclass = obj.__mro__[1].__name__
      if current_class in ['AST', 'object'] or superclass == 'object':
          continue
      classes.append(current_class)
      hierarchy_unions.append((superclass, current_class))
              
graph_style = {
    'graph': {
        'label': 'AsT Nodes',
        'fontsize': '12',
        'size' : "2400,3000",
        'ratio':'compress'
    }
}
        

ast_graph = add_edges(
    add_nodes(digraph(), classes),
    hierarchy_unions
)

new_ast_graph = apply_styles(ast_graph, graph_style)
new_ast_graph.render('ast_nodes')