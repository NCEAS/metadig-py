import pytest
from metadig import run_check
import os
import subprocess
import json
import sys

@pytest.fixture
def sample_check_file():
    test_data_directory = os.path.join(os.path.dirname(__file__), 'testdata')
    return os.path.join(test_data_directory, 'data.table-text-delimited.glimpse.xml')

@pytest.fixture
def sample_metadata_file():
    test_data_directory = os.path.join(os.path.dirname(__file__), 'testdata')
    return os.path.join(test_data_directory, 'doi:10.18739_A2QJ78081.xml')


def test_run_check(sample_check_file, sample_metadata_file):
    result = run_check(sample_check_file, sample_metadata_file)

    variables = {'var1': 10}

    wrapped_code = f"""
import json
locals().update({json.dumps(variables)})
def call():
    print(var1)
"""


    # Run the code directly in a subprocess
    result = subprocess.run(
        [sys.executable, "-c", wrapped_code + '\ncall()'],
        capture_output=True,
        text=True,
        check=True
    )
    
    print(result.stdout)


    assert result is not None, "Expected a result from the embedded code."