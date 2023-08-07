"""
XMLParser module for parsing XML files using various parsing strategies.

This module contains the XMLParser class which provides functionalities to
navigate and extract data from XML files. It also defines the ParsingStrategy
interface for creating custom parsing strategies.
"""

import xml.etree.ElementTree as ET
import re
from abc import ABC, abstractmethod
from typing import Dict, Tuple, List


# ParsingStrategy interface
class ParsingStrategy(ABC):
    """
    Abstract base class defining the interface for XML parsing strategies.

    This interface is designed to be implemented by classes that provide
    custom parsing logic for specific XML tags. The defined methods dictate
    how XML elements should be parsed and converted into a desired data structure.
    """
    @abstractmethod
    def recursive_parse(self, element) -> None:
        # Implement logic to recursively parse the element and its children
        pass


class XMLParser:
    """
    Parser for navigating and extracting data from XML files using customizable parsing strategies.

    The XMLParser provides methods to navigate through an XML tree,
    set parsing strategies for specific XML tags, and extract data
    from the XML structure into a desired format.
    """
    def __init__(self, file_path, parsing_strategies=None):
        self.file_path = file_path
        self.tree = ET.parse(self.file_path)
        self.root = self.tree.getroot()
        self.current_element = self.root
        self.current_path = [self.root.tag]
        self.data = {}
        self.parsing_strategies = parsing_strategies or {}

    def set_strategy(self, parsing_strategies: Dict) -> None:
        self.parsing_strategies = parsing_strategies

    def get_current_info(self) -> Tuple[str]:
        return self.current_element.tag, self.current_element.attrib.get('NAME'), self.current_element.text

    def get_current_path(self) -> str:
        return '/'.join(self.current_path)

    def get_child_info(self) -> List[Tuple[str]]:
        return [(child.tag, child.attrib.get('NAME'), child.text) for child in self.current_element]

    def get_data(self) -> Dict:
        return self.data

    def print_current_info(self) -> None:
        print(f"Current Element: {self.get_current_info()}")
        print(f"Current Path: {self.get_current_path()}")

    def print_child_options(self) -> None:
        child_info = self.get_child_info()
        for i, info in enumerate(child_info, start=1):
            print(f"Child Element {i}: {info}")

    def go_to_child(self, child_info, occurrence=0) -> None:
        """
        Navigate to a specified child element of the current XML element.

        This method uses the provided child_info to determine which child element to navigate to.
        If the child_info contains a tag and 'NAME' attribute (e.g., "tag[NAME]"),
        it navigates to the child with the specified tag and 'NAME' attribute.
        If only a tag is provided, it navigates to the child with the specified tag.

        The occurrence parameter determines which occurrence of the child to navigate to,
        in case there are multiple children with the same tag and 'NAME' attribute.
        """
        match = re.match(r'(.*)\[(.*)]', child_info)  # split info into tag and 'NAME' attribute
        if match:
            tag, name = match.groups()
            children_with_info = [child for child in self.current_element
                                  if child.tag == tag and child.attrib.get('NAME') == name]
        else:
            tag = child_info
            children_with_info = [child for child in self.current_element if child.tag == tag]
        if occurrence < len(children_with_info):
            self.current_element = children_with_info[occurrence]
            self.current_path.append(child_info)
        else:
            raise ValueError(f"No child with tag {tag} at occurrence {occurrence} found.")

    def go_to_parent(self) -> None:
        """
        Navigate up one level to the parent element of the current XML element.

        This method updates the current navigational position within the XML
        tree, moving from the current element to its parent. If the current
        element is already the root, the method will have no effect.
        """
        if self.current_element == self.root:
            raise ValueError("Already at root, cannot go to parent.")
        for parent in self.root.iter():
            if self.current_element in list(parent):
                self.current_element = parent
                self.current_path.pop()
                return

    def add_to_data(self, path, key=None):
        """
        Extract data from a specific XML path and add it to the internal data dictionary.

        This method navigates to the specified XML path, extracts the data, and
        stores it in the internal `data` dictionary. The key used for storing
        the data is derived from the 'NAME' attribute of the XML element, but
        this can be overridden with a custom key if provided.
        """
        elements = path.split('/')[1:]  # skip the first element, as it's the root
        current_element = self.root
        for element in elements:
            match = re.match(r'(.*)\[(.*)]', element)  # split element into tag and 'NAME' attribute
            if match:
                tag, name = match.groups()
                for child in current_element:
                    if child.tag == tag and child.attrib.get('NAME') == name:
                        current_element = child
                        break
                else:
                    raise ValueError(f"Element {element} not found in path.")
            else:
                tag = element
                current_element = current_element.find(tag)
                if current_element is None:
                    raise ValueError(f"Element {element} not found in path.")
        key = key if key is not None else current_element.attrib.get('NAME')
        value = current_element.text
        self.data[key] = value

    def recursive_parse(self, element):
        """
        Recursively parse an XML element using the assigned parsing strategies.

        This method traverses the XML tree starting from the provided element,
        applying any defined parsing strategies for specific XML tags. If no
        strategy is defined for a particular tag, a default parsing logic is used.
        """
        strategy = self.parsing_strategies.get(element.tag)
        if strategy is not None:
            return strategy.recursive_parse(element)
        else:
            # Default recursion
            child_element_tags = [child.tag for child in element]
            if len(child_element_tags) != len(set(child_element_tags)):  # Array of dictionaries
                child_elements = []
                for child in element:
                    child_info = self.recursive_parse(child)
                    (name, data) = list(child_info.items())[0]
                    child_elements.append({'name': name, 'data': data})
                if element.attrib.get('NAME') is None:
                    return {element.tag: child_elements}
                else:
                    return {element.attrib.get('NAME'): child_elements}
            else:  # Dictionary full of custom key value pairs
                child_elements = {}
                for child in element:
                    child_info = self.recursive_parse(child)
                    (name, data) = list(child_info.items())[0]
                    child_elements[name] = data
                if element.attrib.get('NAME') is None:
                    return {element.tag: child_elements}
                else:
                    return {element.attrib.get('NAME'): child_elements}

    def parse(self) -> dict:
        """
        Parse the entire XML document using the assigned parsing strategies.

        This method acts as a wrapper around the recursive_parse method,
        starting the parsing process from the root of the XML document.
        """
        return self.recursive_parse(self.root)
