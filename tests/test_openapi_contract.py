import unittest
from pathlib import Path

import yaml


class OpenApiContractTest(unittest.TestCase):
    def test_user_responses_document_the_email_field(self):
        spec = yaml.safe_load(Path("api/openapi.yaml").read_text(encoding="utf-8"))

        def resolve(schema):
            if "$ref" not in schema:
                return schema
            node = spec
            for part in schema["$ref"].removeprefix("#/").split("/"):
                node = node[part]
            return node

        list_schema = spec["paths"]["/users"]["get"]["responses"]["200"]["content"][
            "application/json"
        ]["schema"]
        self.assertEqual(list_schema["type"], "array")
        user_schema = resolve(list_schema["items"])
        self.assertEqual(user_schema["properties"]["email"]["type"], "string")
        self.assertIn("email", user_schema["required"])

        one_schema = resolve(
            spec["paths"]["/users/{id}"]["get"]["responses"]["200"]["content"][
                "application/json"
            ]["schema"]
        )
        self.assertEqual(one_schema["properties"]["email"]["type"], "string")


if __name__ == "__main__":
    unittest.main()
