"""Test module for 'metadata' module"""

from metadig import metadata
from metadig import StoreManager


def test_read_sysmeta_element(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'read_sysmeta_element' reads a given element as expected."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    _, sys = manager.get_object("test-pid")

    fid = metadata.read_sysmeta_element(sys, "formatId")
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

    ent = metadata.find_eml_entity(doc + dt, identifier, fname)
    anames = ent.findall(".//attributeName")
    assert [elem.text for elem in anames] == ["length_1"]

    ent = metadata.find_eml_entity(doc + oe, identifier, fname)
    anames = ent.findall(".//attributeName")
    assert [elem.text for elem in anames] == ["length_1"]

    ent = metadata.find_eml_entity(doc + oe2, identifier, fname)
    anames = ent.findall(".//attributeName")
    assert [elem.text for elem in anames] == ["length_1"]


def test_read_csv_with_metadata(storemanager_props, init_hashstore_with_test_data):
    """Test that a text delimited document can be read."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    # the_arctic_plant_aboveground_biomass_synthesis_dataset.csv
    pid = "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    _, error = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    assert error is None


def test_read_csv_with_metadata_3_rows_to_skip(
    storemanager_props, init_hashstore_with_test_data
):
    """Test that a text delimited document can be read where header line is not the first row."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    # the_arctic_plant_aboveground_biomass_synthesis_dataset.csv
    pid = "test-pid-3skip"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode("utf-8", errors="replace")
    field_delimiter = ","
    header_line = 4

    df, error = metadata.read_csv_with_metadata(d_read, field_delimiter, header_line)
    expected_columns = [
        "Year",
        "Site",
        "Species",
        "Nest_lat",
        "Nest_lon",
        "Date",
        "Num_indiv",
        "Nest_contents",
        "Notes",
    ]

    assert (
        list(df.columns) == expected_columns
    ), f"Unexpected column names: {list(df.columns)}"
    assert error is None


def test_find_duplicate_columns_none(storemanager_props, init_hashstore_with_test_data):
    """Test that a text delimited document can be read."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    # the_arctic_plant_aboveground_biomass_synthesis_dataset.csv
    pid = "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    dupes = metadata.find_duplicate_columns(df)
    assert len(dupes) == 0


def test_find_duplicate_columns_found(storemanager_props, init_hashstore_with_test_data):
    """Test that a text delimited document can be read."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    # the_arctic_plant_aboveground_biomass_synthesis_dataset.csv
    pid = "test-pid-4dupcols"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    dupes = metadata.find_duplicate_columns(df)
    print(dupes)
