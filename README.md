# MetaDIG-py - A python client package for assisting with running MetaDIG checks

MetaDIG-Py is a library that contains helper functions and classes to assist users with writing 
python checks for suites in [metadig-checks](https://github.com/NCEAS/metadig-checks).

## Contributors

- **Author**: Jeanette Clark, Dou Mok
- **License**: [Apache 2](http://opensource.org/licenses/Apache-2.0)
- [Package source code on GitHub](https://github.com/NCEAS/metadig-py)
- [**Submit Bugs and feature requests**](https://github.com/NCEAS/metadig-py/issues)
- Contact us: support@dataone.org
- [DataONE discussions](https://github.com/DataONEorg/dataone/discussions)

## Introduction

The MetaDIG-py client package contains python modules that users can call when writing checks
for their `metadig-checks`. By importing this package, users get access to all available helper
functions and classes, such as `object_store.py` which enables users to write checks that
efficiently retrieves data objects to work with.

## How do I import the `MetaDIG-py` library to my check?

In your python code, you can import a specific module or function like such:

```py
from metadig import read_sysmeta_element
```

Currently, we have the following modules and functions available:

```py
"StoreManager", # fn
"getType", # fn
"isResolvable", # fn
"isBlank", # fn
"toUnicode", # fn
"read_sysmeta_element", # fn
"find_eml_entity", # fn
"find_entity_index", # fn
"read_csv_with_metadata", # fn
"get_valid_csv", # fn
"run_check", # fn
"checks" # Module
```

## Installation

To install MetaDIG-py, run the following commands

```sh
$ mkvirtualenv -p python3.9 metadigpy // Create a virtual environment
(metadigpy) $ poetry install // Run poetry command to install dependencies
```
- Note: If you run into an issue with installing jep, it is likely due to a backwards
compatibility issue with `setuptools`. Try downgrading to the version 58.0.0:
  ```sh
  (metadigpy) $ pip install setuptools==58.0.0
  ```

To confirm that you have installed `MetaDIG-py` successfully, run `pytest`.
```sh
(metadigpy) $ pytest
```
- Tip: you may run `pytest` with the option `-s` (ex. `pytest -s`) to see print statements when running pytests. Not all pytests have print statements, but if you want to extend from what already exists, this may prove to be helpful!

### How to use the MetaDIG-py command line client

The MetaDIG-py command line client was created to help users test python checks without having to spin up the java engine `metadig-engine` and run a check through the dispatcher.

After you've installed `MetaDIG-py`, you will have access to the command `metadigpy`. Please see installation section above if you haven't installed `MetaDIG-py`. Below is what running a check looks like:

```sh
(metadigpy) $ metadigpy -runcheck -store_path=/path/to/hashstore -check_xml=/path/to/check_xml -metadata_doc=/path/to/metadata/doc -sysmeta_doc=/path/to/sysmeta
```

But before you can run a check, you must ensure that you have everything in place.

TODO: Discuss how you have to setup a hashstore
TODO: Discuss how you need to store the data object you're retrieving first
TODO: Add note about what each piece required is and how it all works together (ex. find_data_pids)
TODO: Add note about using pip installs for the libraries in the checks run

#### How does the MetaDIG-py client run a check with the arguments supplied?

TODO: Explain so it's easier for people to debug if they really have to


## License

```
Copyright [2022] [Regents of the University of California]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Acknowledgements

Work on this package was supported by:

- DataONE Network
- Arctic Data Center: NSF-PLR grant #2042102 to M. B. Jones, A. Budden, M. Schildhauer, and J.
  Dozier

Additional support was provided for collaboration by the National Center for Ecological Analysis and
Synthesis, a Center funded by the University of California, Santa Barbara, and the State of
California.

[![DataONE_footer](https://user-images.githubusercontent.com/6643222/162324180-b5cf0f5f-ae7a-4ca6-87c3-9733a2590634.png)](https://dataone.org)

[![nceas_footer](https://www.nceas.ucsb.edu/sites/default/files/2020-03/NCEAS-full%20logo-4C.png)](https://www.nceas.ucsb.edu)