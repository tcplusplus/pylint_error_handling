from pylint.checkers import BaseChecker
import astroid

class ExceptionDocstringChecker(BaseChecker):
    name = 'exception-docstring-checker'
    priority = -1
    msgs = {
        'C9901': (
            'Exception %s is raised but not documented in the function docstring',
            'missing-exception-doc',
            'All exceptions raised in a function, including those from called functions, should be documented in the function docstring using the "Raises" section, unless they are properly caught and handled within the function.'
        ),
    }

    def visit_functiondef(self, node):
        """
        Check if the function raises any exceptions that are not documented in the docstring,
        including those raised by called functions.
        """
        # Get the docstring of the function
        docstring = node.doc_node.value if node.doc_node else ""

        # Collect all exceptions that are raised and handled in the function
        raised_exceptions = self._collect_raised_exceptions(node)
        handled_exceptions = self._collect_handled_exceptions(node)

        # Identify exceptions that are raised but not handled
        unhandled_exceptions = raised_exceptions - handled_exceptions
        if 'Exception' in handled_exceptions:
            unhandled_exceptions = {}

        # Check if any unhandled exceptions are missing in the docstring
        for exc_type in unhandled_exceptions:
            if f':raises {exc_type}:' not in docstring:
                self.add_message('missing-exception-doc', node=node, args=(exc_type,))

    def _collect_raised_exceptions(self, node):
        """Collect all exceptions raised in the function, including those from called functions."""
        raised_exceptions = set()

        for child in node.body:
            if isinstance(child, astroid.Raise):
                exc_type = self._get_exception_type(child)
                if exc_type:
                    raised_exceptions.add(exc_type)
            elif isinstance(child, astroid.If):
                # Recursively check within if-else blocks
                raised_exceptions.update(self._collect_raised_exceptions(child))
            elif isinstance(child, astroid.Try):
                # Check for raised exceptions within try block
                raised_exceptions.update(self._collect_raised_exceptions(child))

                # Check exceptions raised by function calls within try block
                for stmt in child.body:
                    if isinstance(stmt, astroid.Expr) and isinstance(stmt.value, astroid.Call):
                        called_func = self._resolve_called_function(stmt.value)
                        if called_func:
                            called_exceptions = self._extract_exceptions_from_docstring(called_func)
                            raised_exceptions.update(called_exceptions)

            elif isinstance(child, astroid.Expr) and isinstance(child.value, astroid.Call):
                # Handle function calls and check their docstrings for raised exceptions
                called_func = self._resolve_called_function(child.value)
                if called_func:
                    called_exceptions = self._extract_exceptions_from_docstring(called_func)
                    raised_exceptions.update(called_exceptions)

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
                    else:
                        # If the exception handler catches a general Exception or no specific type
                        # Treat all exceptions as handled
                        handled_exceptions.update(self._collect_raised_exceptions(child))
                        return handled_exceptions

                # Recursively check within try block for handled exceptions
                handled_exceptions.update(self._collect_handled_exceptions(child))
            elif isinstance(child, astroid.If):
                # Recursively check within if-else blocks
                handled_exceptions.update(self._collect_handled_exceptions(child))

        return handled_exceptions

    def _get_exception_type(self, node):
        """Extract the exception type as a string from the node."""
        if isinstance(node, astroid.ExceptHandler):
            if node.type:
                print('node ' + node.type.as_string())
                return node.type.as_string()
            else:
                # This handles cases like `except Exception:` or `except:`
                return "Exception"
        elif isinstance(node, astroid.Raise):
            if isinstance(node.exc, astroid.Call):
                return node.exc.func.as_string()
            elif isinstance(node.exc, astroid.Name):
                return node.exc.name
        return None

    def _resolve_called_function(self, call_node):
        """Resolve the function node being called."""
        try:
            func_node = call_node.func.inferred()[0]
            if isinstance(func_node, astroid.FunctionDef):
                return func_node
        except astroid.InferenceError:
            return None
        return None

    def _extract_exceptions_from_docstring(self, func_node):
        """Extract exceptions listed in the docstring of the called function."""
        docstring = func_node.doc_node.value if func_node.doc_node else ""
        exceptions = set()
        for line in docstring.splitlines():
            if ":raises" in line:
                exception = line.split(":raises")[1].split(":")[0].strip()
                exceptions.add(exception)
        return exceptions

def register(linter):
    linter.register_checker(ExceptionDocstringChecker(linter))
