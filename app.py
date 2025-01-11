from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Riot API Key (Geçerli API Anahtarınızı buraya ekleyin)
RIOT_API_KEY = "RGAPI-759a30f4-318d-44fe-91b7-e3fabd5bc9e9"

@app.route('/<summoner>/<tag>/<region>/rank', methods=['GET'])
def get_rank(summoner, tag, region):
    try:
        # Sihirdar adı ve etiketini birleştir
        summoner_name = f"{summoner}/{tag}"
        region = region.lower()

        # Riot API'den Sihirdar bilgilerini al
        summoner_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        summoner_response = requests.get(summoner_url, headers=headers)

        if summoner_response.status_code != 200:
            return jsonify({"error": "Summoner not found or API error."}), 404

        summoner_data = summoner_response.json()
        summoner_id = summoner_data.get("id")

        # Rank bilgilerini al
        rank_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        rank_response = requests.get(rank_url, headers=headers)

        if rank_response.status_code != 200:
            return jsonify({"error": "Rank data not found or API error."}), 404

        rank_data = rank_response.json()
        if not rank_data:
            return jsonify({"rank": "Unranked"}), 200

        # SoloQ bilgilerini döndür
        for entry in rank_data:
            if entry['queueType'] == "RANKED_SOLO_5x5":
                return jsonify({
                    "tier": entry.get("tier"),
                    "rank": entry.get("rank"),
                    "lp": entry.get("leaguePoints")
                }), 200

        return jsonify({"rank": "SoloQ not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<summoner>/<tag>/<region>/elo', methods=['GET'])
def get_elo(summoner, tag, region):
    try:
        # Sihirdar adı ve etiketini birleştir
        summoner_name = f"{summoner}/{tag}"
        region = region.lower()

        # Riot API'den Sihirdar bilgilerini al
        summoner_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        summoner_response = requests.get(summoner_url, headers=headers)

        if summoner_response.status_code != 200:
            return jsonify({"error": "Summoner not found or API error."}), 404

        summoner_data = summoner_response.json()
        summoner_id = summoner_data.get("id")

        # Rank bilgilerini al
        rank_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        rank_response = requests.get(rank_url, headers=headers)

        if rank_response.status_code != 200:
            return jsonify({"error": "Rank data not found or API error."}), 404

        rank_data = rank_response.json()
        if not rank_data:
            return jsonify({"elo": "Unranked"}), 200

        # SoloQ bilgilerini döndür
        for entry in rank_data:
            if entry['queueType'] == "RANKED_SOLO_5x5":
                return jsonify({
                    "tier": entry.get("tier"),
                    "rank": entry.get("rank"),
                    "lp": entry.get("leaguePoints")
                }), 200

        return jsonify({"elo": "SoloQ not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<summoner>/<tag>/<region>/score', methods=['GET'])
def get_score(summoner, tag, region):
    try:
        # Sihirdar adı ve etiketini birleştir
        summoner_name = f"{summoner}/{tag}"
        region = region.lower()

        # Riot API'den Sihirdar bilgilerini al
        summoner_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        summoner_response = requests.get(summoner_url, headers=headers)

        if summoner_response.status_code != 200:
            return jsonify({"error": "Summoner not found or API error."}), 404

        summoner_data = summoner_response.json()
        summoner_id = summoner_data.get("id")

        # Rank bilgilerini al
        rank_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        rank_response = requests.get(rank_url, headers=headers)

        if rank_response.status_code != 200:
            return jsonify({"error": "Rank data not found or API error."}), 404

        rank_data = rank_response.json()
        if not rank_data:
            return jsonify({"score": "Unranked"}), 200

        # SoloQ bilgilerini döndür
        for entry in rank_data:
            if entry['queueType'] == "RANKED_SOLO_5x5":
                return jsonify({
                    "score": entry.get("leaguePoints")
                }), 200

        return jsonify({"score": "SoloQ not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ana sayfa mesajı
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Riot API Flask App is running! Access rank, elo, and score endpoints."
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
