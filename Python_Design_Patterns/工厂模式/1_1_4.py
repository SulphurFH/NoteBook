# -*- coding: utf-8 -*-

import json
import xml.etree.ElementTree as etree


class FileFactory:
    class JSONConnector(object):
        def __init__(self, filepath):
            self.data = dict()
            with open(filepath, mode='r', encoding='utf-8') as f:
                self.data = json.load(f)

        @property
        def parsed_data(self):
            return self.data

    class XMLConnector(object):
        def __init__(self, filepath):
            self.tree = etree.parse(filepath)

        @property
        def parsed_data(self):
            return self.tree

    def connection_factory(self, filepath):
        if filepath.endswith('json'):
            connector = self.JSONConnector
        elif filepath.endswith('xml'):
            connector = self.XMLConnector
        else:
            raise ValueError('Cannot connect to {}'.format(filepath))
        return connector(filepath)

    def connect_to(self, filepath):
        factory = None
        try:
            factory = self.connection_factory(filepath)
        except ValueError as ve:
            print(ve)
        return factory


def main():
    file_factory = FileFactory()
    xml_factory = file_factory.connect_to('person.xml')
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(".//{}[{}='{}']".format('person', 'lastName', 'Liar'))
    print('found: {} persons'.format(len(liars)))
    for liar in liars:
        print('first name: {}'.format(liar.find('firstName').text))
        print('last name: {}'.format(liar.find('lastName').text))
        [print('phone number ({})'.format(p.attrib['type']), p.text) for p in liar.find('phoneNumbers')]
    print()

    json_factory = file_factory.connect_to('donut.json')
    json_data = json_factory.parsed_data
    print('found: {} donuts'.format(len(json_data)))
    for donut in json_data:
        print('name: {}'.format(donut['name']))
        print('price: ${}'.format(donut['ppu']))
        [print('topping: {} {}'.format(t['id'], t['type'])) for t in donut['topping']]


if __name__ == "__main__":
    main()
