# League Standings Generator

This project generates HTML files displaying the latest league standings for two divisions: "Primera" and "Honor". The standings are extracted from PDF files containing matchday data.

## Usage

1. Place the PDF files containing the matchday data in the appropriate directories (`honor/` and `primera/`). You should have the following structure:

    ```
    honor
    ├── J1 - DH.pdf
    └── J2 - DH.pdf
    primera
    ├── J1 - PD.pdf
    └── J2 - PD.pdf
    ```


2. Run the [generator.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22%2FUsers%2Fapr%2Fprivate%2Fstandings%2Fgenerator.py%22%2C%22path%22%3A%22%2FUsers%2Fapr%2Fprivate%2Fstandings%2Fgenerator.py%22%2C%22scheme%22%3A%22file%22%7D%7D) script to generate the HTML files:

    ```
    python generator.py
    ```

3. The generated HTML files will be saved as `honor_standings_last.html` and `primera_standings_last.html` in the `output/` folder.


## Files

 * `generator.py`: Main script to extract data from PDFs and generate HTML files.
 * `script.js`: JavaScript file to handle the toggle view functionality in the generated HTML.
 * `style.css`: CSS file to style the generated HTML tables.
requirements.txt: List of required Python packages.
