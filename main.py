from xml_element_parsers import AttributeParsingStrategy
from xml_parser import XMLParser


def main():
    # Initialize the main parser with the parsing strategies
    parsing_strategies = {"ATTRIBUTES": AttributeParsingStrategy()}
    parser = XMLParser(
        'G:\\Shared drives\\2023 Booker Engineering\\CLIENTS\\TRACK UTILITIES\\Butte\\O-Calc\\Deliverable\\H1006 - 25670\\PPLX Files for automation\\Permit 3\\25-5-Existing.pplx',
        parsing_strategies)

    # Use the parser to recursively parse the root element
    parsed_data = parser.parse()

    print(parsed_data)


if __name__ == '__main__':
    main()
