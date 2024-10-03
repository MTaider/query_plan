# test_query_plan.py

import unittest
from query_plan import QueryPlan, Fetch, Field, Sequence  

class TestQueryPlan(unittest.TestCase):
    def test_query_plan_document(self):
        # Example of a test for the QueryPlan
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

        expected_output = """{
  QueryPlan {
    Sequence {
      Fetch(service: "SubgraphA") {
        updateInAOne: updateFooInA {
          id
          bar
        }
      }
      Fetch(service: "SubgraphB") {
        updateInBOne: updateFooInB {
          id
          baz
        }
      }
    }
    Fetch(service: "SubgraphA") {
      updateInATwo: updateFooInA {
        id
        bar
      }
    }
  }
}
"""
        self.assertEqual(query_plan.to_document(), expected_output)

if __name__ == "__main__":
    unittest.main()
