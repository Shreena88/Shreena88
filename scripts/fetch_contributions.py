import os
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_and_save_contributions(username="Shreena88", output_json_path=None):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    print(f"Fetching contribution data from {url}...")
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch contributions page, HTTP status: {resp.status_code}")
        
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Map tooltips by 'for' ID
    tooltips = {}
    for tt in soup.find_all("tool-tip"):
        for_id = tt.get("for")
        if for_id:
            tooltips[for_id] = tt.text.strip()
            
    # Parse calendar day cells
    days_data = []
    day_elements = soup.find_all(["td", "rect"], class_=lambda c: c and "ContributionCalendar-day" in c)
    
    for el in day_elements:
        date_str = el.get("data-date")
        if not date_str:
            continue
            
        level = int(el.get("data-level", "0"))
        el_id = el.get("id")
        tooltip_txt = tooltips.get(el_id, "")
        
        # Extract contribution count from tooltip
        # e.g., "No contributions on...", "1 contribution on...", "6 contributions on..."
        count = 0
        if "No contributions" in tooltip_txt:
            count = 0
        else:
            match = re.search(r"(\d+)\s+contribution", tooltip_txt)
            if match:
                count = int(match.group(1))
            elif level > 0:
                count = level  # fallback if count string parsing fails
                
        days_data.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        
    # Sort chronologically
    days_data.sort(key=lambda d: d["date"])
    
    # Calculate statistics
    total_contributions = sum(d["count"] for d in days_data)
    
    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    for d in days_data:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak ending on the latest day in data
    curr = 0
    for d in reversed(days_data):
        if d["count"] > 0:
            curr += 1
        else:
            # If latest days have 0 contributions before ending, break
            if curr > 0 or d == days_data[-1]:
                break
    current_streak = curr
    
    # Best day
    best_day = {"date": "N/A", "count": 0}
    if days_data:
        max_d = max(days_data, key=lambda d: d["count"])
        best_day = {"date": max_d["date"], "count": max_d["count"]}
        
    output_payload = {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days_data
    }
    
    if output_json_path:
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(output_payload, f, indent=2)
        print(f"Saved contributions JSON to {output_json_path}")
        
    print(f"Total Contributions: {total_contributions}")
    print(f"Current Streak: {current_streak} days")
    print(f"Longest Streak: {longest_streak} days")
    print(f"Best Day: {best_day['date']} ({best_day['count']} contributions)")
    
    return output_payload

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file = os.path.join(base_dir, "data", "contributions.json")
    fetch_and_save_contributions("Shreena88", output_file)
