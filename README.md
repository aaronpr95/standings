# Frontenis League Standings Generator

This project generates HTML files displaying the latest frontenis league standings for two divisions: "Primera" and "Honor". The standings are extracted from PDF files containing matchday data.

See: https://aaronpr95.github.io/standings/ 

## Usage

1. Place the PDF files containing the matchday data in the appropriate directories (`honor/` and `primera/`). You should have the following structure:

    ```
    src/resources/docs
    ├── honor
    │   ├── J1 - DH.pdf
    │   └── J2 - DH.pdf
    └── primera
        ├── J1 - PD.pdf
        └── J2 - PD.pdf
    ```


2. GitHub actinos will generate a new version.


## Files

 * `generator.py`: Main script to extract data from PDFs and generate HTML files.
