import pdfplumber
import re
import os
from jinja2 import Environment, FileSystemLoader

HONOR = "honor"
PRIMERA = "primera"

def get_matchday_files(directory):
    """
    Returns a list of files in the given directory that match the matchday pattern.
    """
    return [f for f in os.listdir('src/resources/docs/' + directory) if re.match(r'J\d+ - .+\.pdf$', f)]

def extract_matchday_number(file_name):
    """
    Extracts the matchday number from the given file name.
    """
    match = re.search(r'J(\d+)', file_name)
    return int(match.group(1)) if match else None

def find_latest_day(directory):
    """
    Finds the latest matchday number in the given directory.
    """
    files = get_matchday_files(directory)
    if not files:
        return 0
    
    latest_day = max(extract_matchday_number(f) for f in files)
    return latest_day

def find_latest_pdf(directory):
    """
    Finds the latest PDF file in the given directory.
    """
    files = get_matchday_files(directory)
    if not files:
        return None
    
    latest_file = max(files, key=lambda f: extract_matchday_number(f))
    return f"{directory}/{latest_file}"

def find_badge_path(team_name):
    """
    Finds the badge path for the given team name, checking for _b suffix.
    
    Parameters:
    team_name (str): The name of the team.
    
    Returns:
    str: The path to the badge image file.
    """
    base_name = team_name.lower().replace(' ', '_')
    
    for extension in ['png', 'jpg']:
        badge_path = f"src/resources/img/{base_name}.{extension}"
        if os.path.exists(badge_path):
            return badge_path[4:]
        
        # If team name ends with _b, check the name without _b
        if base_name.endswith('_b') or base_name.endswith('_c') or base_name.endswith('_a'):
            base_name_no_b = base_name[:-2] 
            badge_path_no_b = f"src/resources/img/{base_name_no_b}.{extension}"
            if os.path.exists(badge_path_no_b):
                return badge_path_no_b[4:]
    
    return "resources/img/default_badge.png"

def extract_classification_data(pdf_path, division):
    """
    Extracts classification data from the given PDF file.

    Parameters:
    pdf_path (str): The path to the PDF file.
    division (str): The division name. Either 'honor' or 'primera'.

    Returns:
    list: A list of dictionaries with each team's classification data.
    """
    teams_data = []
    with pdfplumber.open('src/resources/docs/' + pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Regular expression pattern to capture team data in table format
                pattern = re.compile(
                    r"(\d+)\s+([A-ZÁÉÍÓÚÑ\s]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([-]?\d+)\s+(\d+)"
                )
                matches = pattern.findall(text)
                for match in matches:
                    pos, name, pj, pg, pp, jf, jc, tf, tc, diff, points = match
                    badge_path = find_badge_path(name.strip())
                    if name.endswith(' A'):
                        name = name[:-2]
                    descent_class = ""
                    if division == HONOR:
                        total_teams = len(matches)
                        descent_class = "descent" if int(pos) > total_teams - 2 else ""
                    teams_data.append({
                        "position": int(pos),
                        "name": name.strip(),
                        "pj": int(pj),
                        "pg": int(pg),
                        "pp": int(pp),
                        "jf": int(jf),
                        "jc": int(jc),
                        "tf": int(tf),
                        "tc": int(tc),
                        "diff": int(diff),
                        "points": int(points),
                        "badge_path": badge_path,
                        "descent_class": descent_class
                    })
    return teams_data

def generate_html(teams, division):
    """
    Generates an HTML file with the given teams data.
    """
    day = find_latest_day(division)
    env = Environment(loader=FileSystemLoader(searchpath="./src/templates"))
    template = env.get_template("template.html")

    html_content = template.render(teams=teams, division=division, day=day)

    output_file = f"src/{division}_standings.html"

    # Write output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

def process_division(division):
    """
    Process the given division to extract data and generate HTML.
    """
    try:
        pdf_path = find_latest_pdf(division)
        if not pdf_path:
            print(f"No PDF files found for division: {division}")
            return

        teams_data = extract_classification_data(pdf_path, division)
        generate_html(teams_data, division)
        print(f"Standing HTML generated as 'src/{division}_standings.html'")
    except Exception as e:
        print(f"Error processing division {division}: {e}")


# Main script
if __name__ == "__main__":
    print("Starting the league standings generator...")

    process_division(PRIMERA)
    process_division(HONOR)

    print("Finished generating league standings.")