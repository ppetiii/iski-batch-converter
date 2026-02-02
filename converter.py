import json
import datetime
import os

# =================CONFIGURATION =================
input_folder_name = 'inputs'
output_folder_name = 'outputs'
# ================================================

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(script_dir, input_folder_name)
output_dir = os.path.join(script_dir, output_folder_name)

# Create output folder if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output folder: {output_dir}")

# Check if input folder exists
if not os.path.exists(input_dir):
    print(f"ERROR: The folder '{input_folder_name}' does not exist.")
    print("Please create it and put your .json files inside.")
    exit()

# Get list of all json files
json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

if not json_files:
    print(f"No .json files found in '{input_folder_name}'!")
    exit()

print(f"Found {len(json_files)} files. Starting conversion...\n")

# Loop through every file
for filename in json_files:
    input_filepath = os.path.join(input_dir, filename)
    
    # Define output filename
    output_filename = os.path.splitext(filename)[0] + ".gpx"
    output_filepath = os.path.join(output_dir, output_filename)

    try:
        # READ JSON
        with open(input_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # CHECK DATA
        track_string = data.get("track", "")
        if not track_string:
            print(f"Skipping {filename}: No track data found inside.")
            continue

        # PREPARE GPX HEADER
        # We try to use the resort name + date for the internal track name
        resort = data.get('resort_name', 'Unknown Resort')
        start_date = data.get('startdate', '')
        track_id = data.get('track_id', filename)

        gpx_content = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<gpx version="1.1" creator="iSKI-Batch-Converter" xmlns="http://www.topografix.com/GPX/1/1">',
            '  <metadata>',
            f'    <name>{resort} - {start_date}</name>',
            f'    <time>{start_date}</time>',
            '  </metadata>',
            '  <trk>',
            f'    <name>iSKI {track_id} ({resort})</name>',
            '    <type>Skiing</type>',
            '    <trkseg>'
        ]

        # PARSE POINTS
        # Format: LON, LAT, ELE, TIMESTAMP, SPEED
        points = track_string.strip().split(" ")
        point_count = 0

        for p in points:
            parts = p.split(",")
            if len(parts) >= 4:
                lon, lat, ele = parts[0], parts[1], parts[2]
                ts_raw = float(parts[3])
                
                # Convert timestamp
                time_iso = datetime.datetime.fromtimestamp(ts_raw, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                
                gpx_content.append(f'      <trkpt lat="{lat}" lon="{lon}">')
                gpx_content.append(f'        <ele>{ele}</ele>')
                gpx_content.append(f'        <time>{time_iso}</time>')
                gpx_content.append('      </trkpt>')
                point_count += 1

        # CLOSE GPX
        gpx_content.append('    </trkseg>')
        gpx_content.append('  </trk>')
        gpx_content.append('</gpx>')

        # WRITE FILE
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(gpx_content))

        print(f"Converted {filename} -> {output_filename} ({point_count} points)")

    except json.JSONDecodeError:
        print(f"Error in {filename}: Invalid JSON format.")
    except Exception as e:
        print(f"Error in {filename}: {str(e)}")

print("\n---------------------------------------------------")
print(f"All done! Check the '{output_folder_name}' folder.")
print("---------------------------------------------------")