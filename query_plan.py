
class QueryPlan:
    def __init__(self, operations):
        """Initialise the plan with a list of operations"""
        self.operations = operations

    def to_document(self):
        """Creates an executable document from the query plan"""
        doc_string = "{\n  QueryPlan {\n"
        for op in self.operations:
            doc_string += self._render_operation(op, indent=2)  # Using indentation for structure
        doc_string += "  }\n}\n"
        return doc_string

    def _render_operation(self, operation, indent):
        """Private function for rendering operations (Fetch, Sequence)"""
        result = ""
        padding = " " * indent
        
        if isinstance(operation, Sequence):
            # Renderings for sequences
            result += f"{padding}Sequence {{\n"
            for sub_op in operation.operations:
                result += self._render_operation(sub_op, indent + 2)
            result += f"{padding}}}\n"
        
        elif isinstance(operation, Fetch):
            # Rendering for Fetch operations
            result += f'{padding}Fetch(service: "{operation.service}") {{\n'
            for field in operation.selection_set:
                result += self._render_field(field, indent + 2)
            result += f"{padding}}}\n"
        
        return result

    def _render_field(self, field, indent):
        """Field rendering (Field)"""
        indent_str = " " * indent
        
        field_str = f"{indent_str}{field.alias + ': ' if field.alias else ''}{field.name} {{\n"
        for subfield in field.subfields:
            field_str += self._render_field(subfield, indent + 2)  # Recursion for sub-fields
        field_str += f"{indent_str}}}\n"
        return field_str


class Sequence:
    def __init__(self, operations):
        """List of operations in the sequence"""
        self.operations = operations


class Fetch:
    def __init__(self, service, selection_set):
        """The service and fields selected for Fetch"""
        self.service = service
        self.selection_set = selection_set


class Field:
    def __init__(self, name, alias=None, subfields=None):
        """Field name, optional alias and optional subfields"""
        self.name = name
        self.alias = alias
        # By default, sub-fields are an empty list if they are not supplied
        self.subfields = subfields if subfields else []


# Example of using QueryPlan to generate a document
if __name__ == "__main__":
    # Defining the plan with a sequence of operations and fetches
    query_plan = QueryPlan([
        Sequence([
            Fetch("SubgraphA", [
                Field("updateFooInA", alias="updateInAOne", subfields=[
                    Field("id"),
                    Field("bar")
                ])
            ]),
            Fetch("SubgraphB", [
                Field("updateFooInB", alias="updateInBOne", subfields=[
                    Field("id"),
                    Field("baz")
                ])
            ])
        ]),
        Fetch("SubgraphA", [
            Field("updateFooInA", alias="updateInATwo", subfields=[
                Field("id"),
                Field("bar")
            ])
        ])
    ])

    # Displaying the generated document
    print(query_plan.to_document())
