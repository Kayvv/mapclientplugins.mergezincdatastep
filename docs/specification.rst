.. _mcp-mergezincdata-specification:

Ports
-----

This plugin:

* **uses**:

  * *https://opencmiss.org/1.0/rdf-schema#file_location*
  * *https://opencmiss.org/1.0/rdf-schema#file_location*

and

* **provides**:

  * *https://opencmiss.org/1.0/rdf-schema#file_location*

The first **uses** port is the dominant Zinc data file.
Data will be merged onto markers obtained from this file.
The second **uses** port is the recessive Zinc data file.
Data from markers in this file will be made available for merging.