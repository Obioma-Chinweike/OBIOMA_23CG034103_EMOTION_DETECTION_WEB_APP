import sqlite3

# Connect to the database
conn = sqlite3.connect('predictions.db')
c = conn.cursor()

# Fetch all saved predictions
c.execute('SELECT id, username, image_name, emotion, timestamp FROM predictions')
rows = c.fetchall()

if rows:
    print("✅ Saved Predictions:\n")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Image: {row[2]}, Emotion: {row[3]}, Time: {row[4]}")
else:
    print("No predictions saved yet.")

conn.close()
