"""Test module for 'metadata' module"""

from metadig import StoreManager
from metadig import read_sysmeta_element
from metadig import find_eml_entity


def test_read_sysmeta_element(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'read_sysmeta_element' reads a given element as expected."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    _, sys = manager.get_object("test-pid")

    fid = read_sysmeta_element(sys, "formatId")
    assert fid == "text/csv"


def test_find_entity():
    """Test 'find_eml_entity' is able to find the expected entity."""
    doc = """<?xml version="1.0" encoding="UTF-8"?>
    <eml:eml xmlns:eml="https://eml.ecoinformatics.org/eml-2.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:stmml="http://www.xml-cml.org/schema/stmml-1.2" packageId="id" system="system" xsi:schemaLocation="https://eml.ecoinformatics.org/eml-2.2.0 https://eml.ecoinformatics.org/eml-2.2.0/eml.xsd">
      <dataset>
        <title>A Mimimal Valid EML Dataset</title>
        <creator>
          <individualName>
            <givenName>Jeanette</givenName>
            <surName>Clark</surName>
          </individualName>
        </creator>
        <contact>
          <individualName>
            <givenName>Jeanette</givenName>
            <surName>Clark</surName>
          </individualName>
        </contact> \n """

    dt = """<dataTable>
              <entityName>file.csv</entityName>
              <attributeList>
                <attribute>
                  <attributeName>length_1</attributeName>
                  <attributeDefinition>def1</attributeDefinition>
                  <measurementScale>
                    <ratio>
                      <unit>
                        <standardUnit>meter</standardUnit>
                      </unit>
                      <numericDomain>
                        <numberType>real</numberType>
                      </numericDomain>
                    </ratio>
                  </measurementScale>
                </attribute>
              </attributeList>
            </dataTable>
          </dataset>
        </eml:eml>
        """

    oe = """<otherEntity>
          <entityName>file.csv</entityName>
          <attributeList>
            <attribute>
              <attributeName>length_1</attributeName>
              <attributeDefinition>def1</attributeDefinition>
              <measurementScale>
                <ratio>
                  <unit>
                    <standardUnit>meter</standardUnit>
                  </unit>
                  <numericDomain>
                    <numberType>real</numberType>
                  </numericDomain>
                </ratio>
              </measurementScale>
            </attribute>
          </attributeList>
        </otherEntity>
      </dataset>
    </eml:eml>
    """

    oe2 = """<otherEntity>
          <id>identifier-123</id>
          <entityName>file</entityName>
          <attributeList>
            <attribute>
              <attributeName>length_1</attributeName>
              <attributeDefinition>def1</attributeDefinition>
              <measurementScale>
                <ratio>
                  <unit>
                    <standardUnit>meter</standardUnit>
                  </unit>
                  <numericDomain>
                    <numberType>real</numberType>
                  </numericDomain>
                </ratio>
              </measurementScale>
            </attribute>
          </attributeList>
        </otherEntity>
      </dataset>
    </eml:eml>
    """

    fname = "file.csv"
    identifier = "identifier-123"

    ent = find_eml_entity(doc + dt, identifier, fname)
    anames = ent.findall(".//attributeName")
    assert [elem.text for elem in anames] == ["length_1"]

    ent = find_eml_entity(doc + oe, identifier, fname)
    anames = ent.findall(".//attributeName")
    assert [elem.text for elem in anames] == ["length_1"]

    ent = find_eml_entity(doc + oe2, identifier, fname)
    anames = ent.findall(".//attributeName")
    assert [elem.text for elem in anames] == ["length_1"]
