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
"StoreManager",
"getType",
"isResolvable",
"isBlank",
"toUnicode",
"read_sysmeta_element",
"find_eml_entity",
```

## Installation

To install MetaDIG-py, run the following commands

```sh
$ mkvirtualenv -p python3.9 metadigpy // Create a virtual environment
(metadigpy) $ poetry install // Run command to install dependencies
(metadigpy) $ pytest // Restart your IDE if you are having issues executing this command
```
- Note, if you run into an issue with installing jep, it is likely due to a backwards
compatibility issue with `setuptools`. Try downgrading to the version 58.0.0:
```sh
(metadigpy) $ pip install setuptools==58.0.0
```

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