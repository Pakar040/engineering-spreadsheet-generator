"""
XML Element Parsers Module.

This module contains custom parsing strategies for specific XML elements.
Each class provides a method to recursively parse XML elements and their
children, returning the data in a structured dictionary format.
"""

from xml_parser import ParsingStrategy


class AttributeParsingStrategy(ParsingStrategy):
    """
    Custom parsing strategy for XML elements with a focus on attributes.
    """
    def recursive_parse(self, element):
        """
        Recursively parse an XML element, focusing on its attributes.

        The method extracts the attributes from the XML element, with the
        'NAME' attribute serving as the primary key. It then constructs a
        dictionary representation of these attributes. Subsequent child
        elements are processed recursively using the same logic.
        """
        child_elements = {}
        for child in element:
            name = child.attrib.get('NAME')
            data = child.text
            child_elements[name] = data
        return {element.tag: child_elements}
