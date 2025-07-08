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

def test_find_entity_diff_fname():
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

    dt = """<dataTable id="identifier-123">
              <entityName>my cool file</entityName>
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
    # can find by identifier
    fname = "file.csv"
    identifier = "identifier:123"

    ent = metadata.find_eml_entity(doc + dt, identifier, fname)
    assert ent is not None
    
    # can find by filename
    fname = ["my cool file"]
    identifier = "fakeid"

    ent = metadata.find_eml_entity(doc + dt, identifier, fname)
    assert ent is not None



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


def test_find_duplicate_column_content_none(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'find_duplicate_column_content' returns an empty list when there
    are no duplicate column content."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    pid = "test-pid"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    dupes = metadata.find_duplicate_column_content(df)
    assert len(dupes) == 0


def test_find_duplicate_column_content_found(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'find_duplicate_column_content' returns returns a list of tuples when
    duplicate columns are found."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    pid = "test-pid-dupcols-names"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    dupes = metadata.find_duplicate_column_content(df)
    assert len(dupes) == 2


def test_find_duplicate_column_names_none(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'find_duplicate_column_name' returns an empty list when there
    are no duplicate column names."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    pid = "test-pid"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    dupes_col_names, _ = metadata.find_duplicate_column_names(df)
    assert len(dupes_col_names) == 0


def test_find_duplicate_column_names_found(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'find_duplicate_column_name' returns a list of tuples when duplicate
    column names are found."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    pid = "test-pid-4dupcols"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    dupes_col_names, contains_period = metadata.find_duplicate_column_names(df)
    assert len(dupes_col_names) == 2
    assert contains_period


def test_find_duplicate_rows_none(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'find_duplicate_rows' returns None when no duplicate rows are found."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    pid = "test-pid"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    dupe_rows_found = metadata.find_duplicate_rows(df)
    assert dupe_rows_found is None


def test_find_duplicate_rows_found(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'find_duplicate_rows' does not return None when no duplicate rows
    are found."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    pid = "test-pid-duprows"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    dupe_rows_found = metadata.find_duplicate_rows(df)
    assert dupe_rows_found is not None


def test_find_number_of_columns(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'find_number_of_columns' counts columns successfully."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    pid = "test-pid"
    obj, _ = manager.get_object(pid)

    d_read = obj.read().decode('utf-8', errors = 'replace')
    field_delimiter = ","
    skiprows = 0

    df, _ = metadata.read_csv_with_metadata(d_read, field_delimiter, skiprows)
    num_of_cols = metadata.find_number_of_columns(df)
    assert num_of_cols == 9


def test_detect_text_encoding_ascii(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'detect_text_encoding' reads the bytes as ascii."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)

    pid = "test-pid"
    obj, _ = manager.get_object(pid)
    bytes_read = obj.read()

    enc_type, msg = metadata.detect_text_encoding(bytes_read)
    assert enc_type == "ascii"
    assert msg is None


def test_detect_text_encoding_utf8(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'detect_text_encoding' reads the bytes as expected."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    pid = "test-pid-3skip"
    obj, _ = manager.get_object(pid)
    bytes_read = obj.read()

    enc_type, msg = metadata.detect_text_encoding(bytes_read)
    assert enc_type == "Windows-1252"
    assert msg is None


def test_detect_text_encoding_other(storemanager_props, init_hashstore_with_test_data):
    """Confirm that 'detect_text_encoding' reads the bytes as expected."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    pid = "test-pid-utf-8-decode-errors"
    obj, _ = manager.get_object(pid)
    bytes_read = obj.read()

    enc_type, msg = metadata.detect_text_encoding(bytes_read)
    assert enc_type == "ISO-8859-1"
    assert msg is None


def test_escape_for_markdown():
    """Confirm that special characters are escaped"""
    string_to_escape = "American_Black_Duck_x_Mallard_.hybrid."
    escaped_string = metadata.escape_for_markdown(string_to_escape)
    assert escaped_string == r"American\_Black\_Duck\_x\_Mallard\_\.hybrid\."


def test_find_entity_index_fname():
    fname = "data.csv"
    pid = "urn:uuid:1234"
    entity_names = ["other.csv", "data.csv", "final.csv"]
    ids = ["urn-uuid-9999", "urn-uuid-1234", "urn-uuid-8888"]

    result = metadata.find_entity_index(fname, pid, entity_names, ids)
    assert result == 1


def test_find_entity_index_single_pid():
    fname = "data.csv"
    pid = "urn:uuid:1234"
    entity_names = ["other.csv" "final.csv"]
    ids = "urn-uuid-1234"

    result = metadata.find_entity_index(fname, pid, entity_names, ids)
    assert result == 0


def test_find_entity_index_multi_pid():
    fname = "data.csv"
    pid = "urn:uuid:5678"
    entity_names = ["other.csv" "final.csv"]
    ids = ["urn-uuid-1234", "urn-uuid-5678"]

    result = metadata.find_entity_index(fname, pid, entity_names, ids)
    assert result == 1
