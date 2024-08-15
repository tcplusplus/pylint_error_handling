from pylint.checkers import BaseChecker
import astroid

class ExceptionDocstringChecker(BaseChecker):
    name = 'exception-docstring-checker'
    priority = -1
    msgs = {
        'C9901': (
            'Exception %s is raised but not documented in the function docstring',
            'missing-exception-doc',
            'All exceptions raised in a function should be documented in the function docstring using the "Raises" section, unless they are caught and handled within the function.'
        ),
    }

    def visit_functiondef(self, node):
        """
        Check if the function raises any exceptions that are not documented in the docstring,
        but only if those exceptions are not handled within the function.
        """
        # Get the docstring of the function
        docstring = node.doc_node.value if node.doc_node else ""

        # Collect all exceptions that are raised and handled in the function
        raised_exceptions = self._collect_raised_exceptions(node)
        handled_exceptions = self._collect_handled_exceptions(node)

        # Identify exceptions that are raised but not handled
        unhandled_exceptions = raised_exceptions - handled_exceptions

        # Check if any unhandled exceptions are missing in the docstring
        for exc_type in unhandled_exceptions:
            if f':raises {exc_type}:' not in docstring:
                self.add_message('missing-exception-doc', node=node, args=(exc_type,))

    def _collect_raised_exceptions(self, node):
        """Collect all exceptions raised in the function."""
        raised_exceptions = set()

        for child in node.body:
            if isinstance(child, astroid.Raise):
                exc_type = self._get_exception_type(child)
                if exc_type:
                    raised_exceptions.add(exc_type)
            elif isinstance(child, astroid.If):
                # Recursively check within if-else blocks
                raised_exceptions.update(self._collect_raised_exceptions(child))

        return raised_exceptions

    def _collect_handled_exceptions(self, node):
        """Collect all exceptions that are caught by try-except blocks in the function."""
        handled_exceptions = set()

        for child in node.body:
            if isinstance(child, astroid.Try):
                for handler in child.handlers:
                    exc_type = self._get_exception_type(handler)
                    if exc_type:
                        handled_exceptions.add(exc_type)
            elif isinstance(child, astroid.If):
                # Recursively check within if-else blocks
                handled_exceptions.update(self._collect_handled_exceptions(child))

        return handled_exceptions

    def _get_exception_type(self, node):
        """Extract the exception type as a string from the node."""
        if isinstance(node, astroid.ExceptHandler):
            if node.type:
                return node.type.as_string()
        elif isinstance(node, astroid.Raise):
            if isinstance(node.exc, astroid.Call):
                return node.exc.func.as_string()
            elif isinstance(node.exc, astroid.Name):
                return node.exc.name
        return None

def register(linter):
    linter.register_checker(ExceptionDocstringChecker(linter))
