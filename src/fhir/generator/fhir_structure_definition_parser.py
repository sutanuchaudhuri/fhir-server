import json
from pathlib import Path


class FhirStructureDefinitionParser:
    def parse_resources(self) -> None:
        data_dir: Path = Path(__file__).parent.joinpath("./")
        fhir_entities: List[FhirEntity] = []

        # first read fhir-all.xsd to get a list of resources
        fhir_xsd_all_file: Path = (
            data_dir.joinpath("json")
            .joinpath("definitions.json")
            .joinpath("profiles-resources.json")
        )

        with open(fhir_xsd_all_file, "rb") as file:
            contents = file.read()
            json_bundle: Dict[str, Any] = json.loads(contents)
            # print(json_bundle)
            structure_definitions: List[Dict[str, Any]] = [
                entry["resource"] for entry in json_bundle["entry"]
                if entry["resource"]["resourceType"] == "StructureDefinition"
            ]
            # print header
            print("id | path | cardinality | type | referenced_type | value_set | binding_name")
            for structure_definition in structure_definitions:
                # print(structure_definition["id"])
                snapshot: Dict[str, Any] = structure_definition["snapshot"]
                if snapshot:
                    for element in snapshot["element"]:
                        element_id = element['id']
                        element_path = element['path']
                        cardinality: str = f'{element["min"]}..{element["max"]}' if element.get("min") != None else ""
                        element_type: str = element.get("type")[0].get("code") if element.get("type") else ""
                        target_profiles: Optional[List[str]] = None
                        if element.get("type"):
                            for type_ in element.get("type"):
                                if type_.get("targetProfile"):
                                    if not target_profiles:
                                        target_profiles = []
                                    target_profiles.append(type_.get("targetProfile").split("/")[-1])
                        referenced_type: List[str] = target_profiles
                        value_set = element.get('valueSet') if element.get('valueSet') else ""
                        binding: Optional[Dict[str, Any]] = element.get('binding') if element.get('binding') else None
                        binding_name: Optional[str] = None
                        if binding and binding.get("extension"):
                            for extension in binding.get("extension"):
                                if extension.get("url") == "http://hl7.org/fhir/StructureDefinition/elementdefinition-bindingName":
                                    binding_name = extension.get("valueString")

                        print(f"{element_id} | {element_path} | {cardinality} | {element_type} | {referenced_type or ''} | {value_set} | {binding_name or ''} ")

    def parse_non_resources(self) -> None:
        data_dir: Path = Path(__file__).parent.joinpath("./")
        fhir_entities: List[FhirEntity] = []

        # first read fhir-all.xsd to get a list of resources
        fhir_xsd_all_file: Path = (
            data_dir.joinpath("json")
            .joinpath("definitions.json")
            .joinpath("profiles-types.json")
        )

        with open(fhir_xsd_all_file, "rb") as file:
            contents = file.read()
            json_bundle: Dict[str, Any] = json.loads(contents)
            # print(json_bundle)
            structure_definitions: List[Dict[str, Any]] = [
                entry["resource"] for entry in json_bundle["entry"]
                if entry["resource"]["resourceType"] == "StructureDefinition"
            ]
            # print header
            print("id | path | cardinality | type | referenced_type | value_set | binding_name")
            for structure_definition in structure_definitions:
                # print(structure_definition["id"])
                snapshot: Dict[str, Any] = structure_definition["snapshot"]
                if snapshot:
                    for element in snapshot["element"]:
                        element_id = element['id']
                        element_path = element['path']
                        cardinality: str = f'{element["min"]}..{element["max"]}' if element.get("min") != None else ""
                        element_type: str = element.get("type")[0].get("code") if element.get("type") else ""
                        target_profiles: Optional[List[str]] = None
                        if element.get("type"):
                            for type_ in element.get("type"):
                                if type_.get("targetProfile"):
                                    if not target_profiles:
                                        target_profiles = []
                                    target_profiles.append(type_.get("targetProfile").split("/")[-1])
                        referenced_type: List[str] = target_profiles
                        value_set = element.get('valueSet') if element.get('valueSet') else ""
                        binding: Optional[Dict[str, Any]] = element.get('binding') if element.get('binding') else None
                        binding_name: Optional[str] = None
                        if binding and binding.get("extension"):
                            for extension in binding.get("extension"):
                                if extension.get("url") == "http://hl7.org/fhir/StructureDefinition/elementdefinition-bindingName":
                                    binding_name = extension.get("valueString")

                        print(f"{element_id} | {element_path} | {cardinality} | {element_type} | {referenced_type or ''} | {value_set} | {binding_name or ''} ")
