## Data processing code for the CBP website.

## Known bugs:
- The database that the website is built on currently has outdated values for Alaska. Due to inconsistent naming conventions, the values in the CBP data don't match with the GeoJSON file. This has been fixed in the make_readable function written in the website_util file, but the values in the database need to be updated. 
