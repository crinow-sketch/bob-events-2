import json, urllib.request

SB_URL = "https://cbdjoydzoiysvcleybpq.supabase.co/rest/v1/music_events"
SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNiZGpveWR6b2l5c3ZjbGV5YnBxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2ODI1MzIsImV4cCI6MjA5NDI1ODUzMn0.WajecLt1M_b1cHCyZ9j-p6CUX-Z9z-pcG3ISE8I1Fe0"

games = [
    {"id":"bills-w1","name":"Bills at Texans","date":"2026-09-13","dow":"Sunday","time_range":"1pm","notes":"Week 1 | Away - NRG Stadium"},
    {"id":"bills-w2","name":"Bills vs Lions","date":"2026-09-17","dow":"Thursday","time_range":"8:15pm","notes":"Week 2 | HOME OPENER - Highmark Stadium | Thursday Night Football"},
    {"id":"bills-w3","name":"Bills vs Chargers","date":"2026-09-27","dow":"Sunday","time_range":"1pm","notes":"Week 3 | Home - Highmark Stadium"},
    {"id":"bills-w4","name":"Bills vs Patriots","date":"2026-10-04","dow":"Sunday","time_range":"1pm","notes":"Week 4 | Home - Highmark Stadium | AFC East"},
    {"id":"bills-w5","name":"Bills at Rams","date":"2026-10-12","dow":"Monday","time_range":"8:15pm","notes":"Week 5 | Away - SoFi Stadium | Monday Night Football"},
    {"id":"bills-w6","name":"Bills at Raiders","date":"2026-10-18","dow":"Sunday","time_range":"4:25pm","notes":"Week 6 | Away - Allegiant Stadium"},
    {"id":"bills-w8","name":"Bills vs Ravens","date":"2026-11-01","dow":"Sunday","time_range":"1pm","notes":"Week 8 | Home - Highmark Stadium"},
    {"id":"bills-w9","name":"Bills at Vikings","date":"2026-11-09","dow":"Monday","time_range":"8:15pm","notes":"Week 9 | Away - U.S. Bank Stadium | Monday Night Football"},
    {"id":"bills-w10","name":"Bills at Jets","date":"2026-11-15","dow":"Sunday","time_range":"1pm","notes":"Week 10 | Away - MetLife Stadium | AFC East"},
    {"id":"bills-w11","name":"Bills vs Dolphins","date":"2026-11-22","dow":"Sunday","time_range":"1pm","notes":"Week 11 | Home - Highmark Stadium | AFC East"},
    {"id":"bills-w12","name":"Bills vs Chiefs","date":"2026-11-26","dow":"Thursday","time_range":"8:20pm","notes":"Week 12 | Home - Highmark Stadium | THANKSGIVING primetime"},
    {"id":"bills-w13","name":"Bills at Patriots","date":"2026-12-06","dow":"Sunday","time_range":"4:25pm","notes":"Week 13 | Away - Gillette Stadium | AFC East"},
    {"id":"bills-w14","name":"Bills at Packers","date":"2026-12-13","dow":"Sunday","time_range":"8:20pm","notes":"Week 14 | Away - Lambeau Field | Sunday Night Football"},
    {"id":"bills-w15","name":"Bills vs Bears","date":"2026-12-19","dow":"Saturday","time_range":"8:20pm","notes":"Week 15 | Home - Highmark Stadium | Saturday primetime"},
    {"id":"bills-w16","name":"Bills at Broncos","date":"2026-12-25","dow":"Friday","time_range":"4:30pm","notes":"Week 16 | Away - Empower Field | CHRISTMAS DAY"},
    {"id":"bills-w17","name":"Bills at Dolphins","date":"2027-01-03","dow":"Sunday","time_range":"1pm","notes":"Week 17 | Away - Hard Rock Stadium | AFC East"},
    {"id":"bills-w18","name":"Bills vs Jets","date":"2027-01-10","dow":"Sunday","time_range":"TBD","notes":"Week 18 | Home - Highmark Stadium | AFC East | Date/time TBD"},
]

for g in games:
    data = json.dumps(g).encode()
    req = urllib.request.Request(SB_URL, data=data, method="POST")
    req.add_header("apikey", SB_KEY)
    req.add_header("Authorization", "Bearer " + SB_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Prefer", "return=minimal")
    try:
        urllib.request.urlopen(req)
        print(f"OK: {g['id']} - {g['name']}")
    except Exception as e:
        print(f"Error {g['id']}: {e}")

print(f"\nInserted {len(games)} Buffalo Bills games")
