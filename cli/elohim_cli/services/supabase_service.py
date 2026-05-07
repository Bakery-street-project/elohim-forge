import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
# Initialize client only if valid credentials are provided
supabase: Client = create_client(url, key) if (url and key and url != "http://localhost:8000") else None

def log_battle(winner: str, logs: list):
    if supabase:
        supabase.table("battles").insert({"winner": winner, "logs": logs}).execute()
    else:
        print(f"MOCK LOG: Winner={winner}, Logs={len(logs)} entries.")

def get_all_battles():
    if supabase:
        return supabase.table("battles").select("winner").execute().data
    return []
