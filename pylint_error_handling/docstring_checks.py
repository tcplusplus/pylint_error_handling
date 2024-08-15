from pylint.checkers import BaseChecker
import astroid

class ExceptionDocstringChecker(BaseChecker):

    name = 'exception-docstring-checker'
    priority = -1
    msgs = {
        'C9901': (
            'Exception %s is raised but not documented in the function docstring',
            'missing-exception-doc',
            'All exceptions raised in a function should be documented in the function docstring using the "Raises" section.'
        ),
    }

    def visit_raise(self, node):
        # Haal de functie op waarin de exception wordt geraised
        func_node = node.frame()
        if func_node is None or not hasattr(func_node, 'doc_node'):
            return

        # Haal de docstring van de functie op
        docstring = func_node.doc_node.value if func_node.doc_node else ""

        # Haal de exception klasse op die wordt geraised
        exc_type = None
        if isinstance(node.exc, astroid.Call):
            exc_type = node.exc.func.as_string()
        elif isinstance(node.exc, astroid.Name):
            exc_type = node.exc.name

        if exc_type and f':raises {exc_type}:' not in docstring:
            self.add_message('missing-exception-doc', node=node, args=(exc_type,))

def register(linter):
    linter.register_checker(ExceptionDocstringChecker(linter))
