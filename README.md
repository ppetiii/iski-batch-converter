# iski-batch-converter

Convert iSki Tracker tracks to gpx files.

Usage:
1. Find your tracks on: https://iski.cc/en/community/tracks
2. Open a track and copy the ID from the URL (e.g. "123456" from "https://iski.cc/en/community/tracks/123456")
3. Open this URL with your track ID: https://delphi.iski.cc/api/tracks/123456/details?lang=en
4. Save the content to a .json file in the inputs folder
5. Repeat step 2-4 for each track you want to convert
6. Run converter.py
7. Your tracks will be in the outputs folder
