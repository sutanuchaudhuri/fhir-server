import json
from pprint import pprint

from fhir_structure_definition_parser import FhirStructureDefinitionParser


def test_generator() -> None:
    print()
    # fhir_entities = FhirXmlSchemaParser.generate_classes()
    fhir_entities = FhirStructureDefinitionParser().parse_account()

    # json_entities = json.dumps([e.__dict__ for e in fhir_entities], indent=4)
    # fhir_entities = FhirStructureDefinitionParser().parse_non_resources()

    # now print the result
    for fhir_entity in fhir_entities:
        pprint(fhir_entity)
