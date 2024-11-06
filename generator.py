import pdfplumber
import re
import os

HONOR = "honor"
PRIMERA = "primera"

def find_latest_day(directory):
    """
    Finds the latest matchday number in the given directory.
    """
    files = [f for f in os.listdir('resources/docs/' + directory) if re.match(rf'J\d+ - .+\.pdf$', f)]
    
    max_jornada = 0
    for file in files:
        match = re.search(r'J(\d+)', file)
        if match:
            jornada_num = int(match.group(1))
            if jornada_num > max_jornada:
                max_jornada = jornada_num
    return max_jornada               

def find_latest_pdf(directory):
    """
    Finds the latest PDF file in the given directory.
    """
    files = [f for f in os.listdir('resources/docs/' + directory) if re.match(rf'J\d+ - .+\.pdf$', f)]
    
    max_jornada = 0
    latest_file = None
    for file in files:
        match = re.search(r'J(\d+)', file)
        if match:
            jornada_num = int(match.group(1))
            if jornada_num > max_jornada:
                max_jornada = jornada_num
                latest_file = file
                
    return "{}/{}".format(directory, latest_file)

def extract_classification_data(pdf_path):
    """
    Extracts classification data from the latest matchday PDF.
    
    Parameters:
    pdf_path (str): Path to the PDF file containing the latest matchday data.
    
    Returns:
    list: A list of dictionaries with each team's classification data.
    """
    teams_data = []
    with pdfplumber.open('resources/docs/' + pdf_path) as pdf:
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
                        "points": int(points)
                    })
    return teams_data

def find_badge_path(team_name):
    """
    Finds the badge path for the given team name, checking for _b suffix.
    
    Parameters:
    team_name (str): The name of the team.
    
    Returns:
    str: The path to the badge image file.
    """
    base_name = team_name.lower().replace(' ', '_')
    
    # Check for both .png and .jpg files
    for extension in ['png', 'jpg']:
        # Try the base name first
        badge_path = f"resources/img/{base_name}.{extension}"
        if os.path.exists(badge_path):
            return badge_path
        
        # If team name ends with _b, check the name without _b
        if base_name.endswith('_b') or base_name.endswith('_c') or base_name.endswith('_a'):
            base_name_no_b = base_name[:-2] 
            badge_path_no_b = f"resources/img/{base_name_no_b}.{extension}"
            if os.path.exists(badge_path_no_b):
                return badge_path_no_b
    
    # Return a default placeholder image if no badge is found
    return "resources/img/default_badge.png"

def generate_html(teams_data, division):
    """
    Generates an HTML file with the league classification table.
    
    Parameters:
    teams_data (list): List of dictionaries with each team's classification data.
    output_file (str): Output HTML file name. Default is "standings_last.html".
    """
    day = find_latest_day(division)
    division_name = "División de Honor" if division == HONOR else "Primera División"
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clasificación Liga Frontenis Castilla y León</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Liga Regional de Frontenis Castilla y León</h2>
            <h1>Clasificación {division_name} | Jornada {day}</h1>
        </div>
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th></th>
                    <th>Equipo</th>
                    <th data-tooltip="Partidos Jugados">PJ</th>
                    <th data-tooltip="Partidos Ganados">PG</th>
                    <th data-tooltip="Partidos Perdidos">PP</th>
                    <th class="hidden" data-tooltip="Juegos a Favor">JF</th>
                    <th class="hidden" data-tooltip="Juegos en Contra">JC</th>
                    <th class="hidden" data-tooltip="Tantos a Favor">TF</th>
                    <th class="hidden" data-tooltip="Tantos en Contra"">TC</th>
                    <th class="hidden" data-tooltip="Diferencia de tantos">Dif</th>
                    <th>Puntos</th>
                </tr>
            </thead>
            <tbody>
    """

    # Total number of teams in the ranking table
    total_teams = len(teams_data)

    # Generate table rows based on extracted team data
    for team in teams_data:
        # Get the badge path for the team
        badge_path = find_badge_path(team['name'])
        
        # Check if the team is in a relegation position

        descent_class = ""
        if division == HONOR:
            descent_class = "descent" if team['position'] > total_teams - 2 else ""

        if team['name'].endswith(' A'):
            team['name'] = team['name'][:-2]

        # Generate the HTML content for the row
        html_content += f"""
            <tr class="{descent_class}">
                <td>{team['position']}</td>
                <td><img src="{badge_path}" alt="Escudo {team['name']}" width="30"></td>
                <td>{team['name']}</td>
                <td>{team['pj']}</td>
                <td>{team['pg']}</td>
                <td>{team['pp']}</td>
                <td class="hidden">{team['jf']}</td>
                <td class="hidden">{team['jc']}</td>
                <td class="hidden">{team['tf']}</td>
                <td class="hidden">{team['tc']}</td>
                <td class="hidden">{team['diff']}</td>
                <td>{team['points']}</td>
            </tr>
        """

    # Close HTML structure
    html_content += """
            </tbody>
        </table>
        <div class="toggle-container">
            <button id="toggleView">Ver Detalles</button>
        </div>
    </div>
    <script src="static/script.js"></script>
</body>
</html>
    """
    if division == PRIMERA:
        output_file = "output/primera_standings_last.html"
    elif division == HONOR:
        output_file = "output/honor_standings_last.html"

    # Write output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    path_primera = find_latest_pdf(PRIMERA)
    path_honor = find_latest_pdf(HONOR)

    primera_data = extract_classification_data(path_primera)
    generate_html(primera_data, PRIMERA)
    print("Standing HTML generated as 'primera_standings_last.html'")

    honor_data = extract_classification_data(path_honor)
    generate_html(honor_data, HONOR)
    print("Standing HTML generated as 'honor_standings_last.html'")