import json
from pathlib import Path
import dataclasses
import re
from pathlib import Path
from typing import OrderedDict, Any, List, Union, Dict, Optional, Set
import logging

from fhir.resources.R4B.bundle import Bundle


@dataclasses.dataclass
class SmartName:
    name: str
    cleaned_name: str
    snake_case_name: str


@dataclasses.dataclass
class FhirValueSetConcept:
    code: str
    display: Optional[str]
    cleaned_display: Optional[str]
    definition: Optional[str]
    source: str
    value_set_url: str


@dataclasses.dataclass
class FhirValueSet:
    id_: str
    name: str
    fhir_name: str
    name_snake_case: str
    cleaned_name: str
    concepts: List[FhirValueSetConcept]
    url: str
    value_set_url: str
    value_set_url_list: Set[str]
    documentation: List[str]
    source: str


@dataclasses.dataclass
class FhirCodeableType:
    codeable_type: str
    path: str
    codeable_type_url: str
    is_codeable_concept: bool = False


@dataclasses.dataclass
class FhirReferenceType:
    target_resources: List[str]
    path: str


@dataclasses.dataclass
class FhirProperty:
    name: str
    fhir_name: str
    javascript_clean_name: str
    type_: str
    cleaned_type: str
    type_snake_case: str
    optional: bool
    is_list: bool
    documentation: List[str]
    fhir_type: Optional[str]
    reference_target_resources: List[SmartName]
    reference_target_resources_names: List[str]
    is_back_bone_element: bool
    is_basic_type: bool
    codeable_type: Optional[SmartName]
    is_resource: bool = False
    is_extension: bool = False
    is_code: bool = False
    is_complex: bool = False
    name_suffix: Optional[str] = None
    is_v2_supported: bool = False


@dataclasses.dataclass
class FhirEntity:
    fhir_name: str
    cleaned_name: str
    name_snake_case: str
    properties: List[FhirProperty]
    documentation: List[str]
    type_: Optional[str]
    is_back_bone_element: bool
    base_type: Optional[str]
    base_type_list: List[str]
    source: str
    is_value_set: bool = False
    value_set_concepts: Optional[List[FhirValueSetConcept]] = None
    value_set_url: Optional[str] = None
    is_basic_type: bool = False
    value_set_url_list: Optional[Set[str]] = None
    is_resource: bool = False
    is_extension: bool = False
    properties_unique: Optional[List[FhirProperty]] = None

class FhirStructureDefinitionParser:
    def parse_resources(self) -> List[FhirEntity]:
        data_dir: Path = Path(__file__).parent.joinpath("./")
        fhir_entities: List[FhirEntity] = []

        # first read fhir-all.xsd to get a list of resources
        fhir_xsd_all_file: Path = (
            data_dir.joinpath("xsd")
            .joinpath("definitions.xml")
            .joinpath("profiles-resources.xml")
        )

        with open(fhir_xsd_all_file, "rb") as file:
            contents = file.read()
            bundle: Bundle = Bundle.parse_raw(contents, content_type="text/xml")
            json_bundle: Dict[str, Any] = json.loads(bundle.json())
            # print(json_bundle)
            structure_definitions: List[Dict[str, Any]] = [
                entry["resource"] for entry in json_bundle["entry"]
                if entry["resource"]["resourceType"] == "StructureDefinition"
            ]
            # print header
            print("id | path | cardinality | type | referenced_target_resources | value_set | binding_name")
            for structure_definition in structure_definitions:
                # print(structure_definition["id"])
                snapshot: Dict[str, Any] = structure_definition["snapshot"]
                if snapshot:
                    resource_name = structure_definition["name"]
                    resource_documentation: str = structure_definition["description"]
                    fhir_properties: List[FhirProperty] = []
                    for element in snapshot["element"]:
                        element_id = element.get('id')
                        element_path = element['path']
                        element_name = element_path.split(".")[-1]
                        cardinality: str = f'{element["min"]}..{element["max"]}' if element.get("min") != None else ""
                        element_type: str = element.get("type")[0].get("code") if element.get("type") else ""
                        if element_type == "":
                            # base resource
                            resource_documentation = element.get("definition") if element.get("definition") else ""
                            continue
                        target_profiles: Optional[List[str]] = None
                        if element.get("type"):
                            for type_ in element.get("type"):
                                if type_.get("targetProfile"):
                                    if not target_profiles:
                                        target_profiles = []
                                    if isinstance(type_.get("targetProfile"), list):
                                        target_profiles.extend([t.split("/")[-1] for t in type_.get("targetProfile")])
                                    else:
                                        target_profiles.append(type_.get("targetProfile").split("/")[-1])
                        referenced_target_resources: List[str] = target_profiles
                        value_set = element.get('valueSet') if element.get('valueSet') else ""
                        binding: Optional[Dict[str, Any]] = element.get('binding') if element.get('binding') else None
                        binding_name: Optional[str] = None
                        if binding and binding.get("extension"):
                            for extension in binding.get("extension"):
                                if extension.get("url") == "http://hl7.org/fhir/StructureDefinition/elementdefinition-bindingName":
                                    binding_name = extension.get("valueString")

                        documentation: str = element.get("definition") if element.get("definition") else ""
                        print(f"{element_id} | {element_path} | {cardinality} | {element_type} | {referenced_target_resources or ''} | {value_set} | {binding_name or ''} ")
                        property_: FhirProperty = FhirProperty(
                            name=element_name,
                            fhir_name=element_name,
                            javascript_clean_name=element_name,
                            type_=element_type,
                            cleaned_type=element_type,
                            type_snake_case=element_type,
                            optional=element.get("min") == 0,
                            is_list=element.get("max") == "*",
                            documentation=[documentation],
                            fhir_type=element_type,
                            reference_target_resources=[SmartName(name=r, cleaned_name=r, snake_case_name=r) for r in referenced_target_resources] if referenced_target_resources else [],
                            reference_target_resources_names=referenced_target_resources,
                            is_back_bone_element=element_type == "BackboneElement",
                            is_basic_type=False,
                            codeable_type=None,
                            is_resource=False,
                            is_extension=element_type == "Extension",
                            is_code=element_type == "code",
                            is_complex=element_type == "complex",
                            name_suffix=None,
                            is_v2_supported=False
                        )
                        fhir_properties.append(property_)

                    fhir_entity: FhirEntity = FhirEntity(
                        fhir_name=resource_name,
                        cleaned_name=resource_name,
                        name_snake_case=resource_name,
                        properties=fhir_properties,
                        documentation=[],
                        type_="Resource",
                        is_back_bone_element=False,
                        base_type=None,
                        base_type_list=[],
                        source="http://hl7.org/fhir/StructureDefinition/{}".format(resource_name),
                        is_value_set=False,
                        value_set_concepts=None,
                        value_set_url=None,
                        is_basic_type=False,
                        value_set_url_list=None,
                        is_resource=True,
                        is_extension=False,
                        properties_unique=None
                    )
                    fhir_entities.append(fhir_entity)
        return fhir_entities

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
        return fhir_entities
