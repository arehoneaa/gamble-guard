from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Function to normalize the URL
def normalize_url(url):
    # Remove 'www.' if it exists
    if url.startswith("https://www."):
        url = url.replace("https://www.", "https://")
    elif url.startswith("http://www."):
        url = url.replace("http://www.", "http://")
    
    # Remove trailing slash
    url = url.rstrip("/")
    
    print(f"Normalized URL: {url}")  # Debugging: print the normalized URL
    return url


# Function to check the verification of a site
def check_site_verification(url):
    # Normalize the URL before checking the database
    url = normalize_url(url)
    
    conn = sqlite3.connect('gambling_sites.db')  # Connect to SQLite DB
    cursor = conn.cursor()

    # Check if the site is in the illegal_sites table
    cursor.execute("SELECT * FROM illegal_sites WHERE url = ?", (url,))
    unverified_site = cursor.fetchone()

    if unverified_site:
        conn.close()
        return False, None

    # Check if the site is in the legal_sites table
    cursor.execute("SELECT * FROM legal_sites WHERE url = ?", (url,))
    verified_site = cursor.fetchone()

    print(f"Verified site from DB: {verified_site}")  # Debugging
    conn.close()

    if verified_site:
        return True, {
            "name": verified_site[2],
            "license": verified_site[3],
            "license_expiry": verified_site[4]
        }

    return False, None


@app.route('/')
def home():
    # Fetch the recommended gambling sites from the database
    conn = sqlite3.connect('gambling_sites.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, url FROM legal_sites")
    recommended_sites = cursor.fetchall()
    conn.close()

    return render_template('index.html', recommended_sites=recommended_sites)

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    url = data.get('url')
    is_verified, site_details = check_site_verification(url)
    
    if is_verified:
        response = {
            'verified': True,
            'name': site_details['name'],
            'license': site_details['license'],
            'license_expiry': site_details['license_expiry'],
            'country_of_origin': 'South Africa',
            'trustworthiness_score': 95
        }
    else:
        response = {
            'verified': False,
            'country_of_origin': 'Unknown',
            'trustworthiness_score': 10
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
