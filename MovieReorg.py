import os
import shutil
import re
from imdb import IMDb

def clean_movie_name(filename):
    """Extracts a probable movie name from the filename by removing common delimiters and file extensions."""
    name = re.sub(r'[\.\_\-]', ' ', filename)  # Replace common separators with spaces
    name = re.sub(r'\s+\d{4}\s+', ' ', name)  # Remove years (e.g., "1999")
    name = re.sub(r'\(.*?\)|\[.*?\]', '', name)  # Remove any text inside brackets or parentheses
    name = name.rsplit('.', 1)[0]  # Remove file extension
    return name.strip()

def extract_resolution(filename):
    """Extracts resolution from filename if present (e.g., 1080p, 720p, 4K, 2160p)."""
    match = re.search(r'(\d{3,4}p|4K)', filename, re.IGNORECASE)
    return match.group(1) if match else None

def get_movie_info(query):
    """Searches IMDb for a movie and returns the best match's title and year."""
    ia = IMDb()
    results = ia.search_movie(query)
    if results:
        movie = results[0]  # Best match
        ia.update(movie)  # Get full details
        return movie.get('title'), movie.get('year')
    return None, None

def organize_movies(directory):
    """Processes video files in the given directory and organizes them into folders."""
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv'}
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath) and any(filename.lower().endswith(ext) for ext in video_extensions):
            movie_name = clean_movie_name(filename)
            resolution = extract_resolution(filename)
            title, year = get_movie_info(movie_name)

            if title and year:
                folder_name = f"{title} ({year})"
                folder_path = os.path.join(directory, folder_name)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                resolution_str = f" {resolution}" if resolution else ""
                new_filename = f"{title} ({year}){resolution_str}{os.path.splitext(filename)[1]}"
                new_filepath = os.path.join(folder_path, new_filename)

                shutil.move(filepath, new_filepath)
                print(f"Moved: {filename} -> {new_filepath}")
            else:
                print(f"Skipped: {filename} (No IMDb match)")

if __name__ == "__main__":
    movie_directory = input("Enter the path to your movie folder: ").strip()
    if os.path.isdir(movie_directory):
        organize_movies(movie_directory)
    else:
        print("Invalid directory.")
