from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Riot API Key
RIOT_API_KEY = "RGAPI-759a30f4-318d-44fe-91b7-e3fabd5bc9e9"

@app.route('/<summoner>/<tag>/<region>/elo', methods=['GET'])
def get_elo(summoner, tag, region):
    try:
        # Sihirdar bilgilerini al
        summoner_name = f"{summoner}/{tag}"
        region = region.lower()

        # Sihirdar bilgilerini sorgula
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

        # Rank bilgilerini döndür
        rank_info = rank_data[0]
        return jsonify({
            "tier": rank_info.get("tier"),
            "rank": rank_info.get("rank"),
            "lp": rank_info.get("leaguePoints")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/<summoner>/<tag>/<region>/skor', methods=['GET'])
def get_daily_scores(summoner, tag, region):
    try:
        # Sihirdar bilgilerini al
        region = region.lower()
        summoner_name = f"{summoner}/{tag}"

        # Sihirdar bilgilerini sorgula
        summoner_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        summoner_response = requests.get(summoner_url, headers=headers)

        if summoner_response.status_code != 200:
            return jsonify({"error": "Summoner not found or API error."}), 404

        summoner_data = summoner_response.json()
        summoner_id = summoner_data.get("id")

        # Maç geçmişini al
        match_url = f"https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{summoner_id}"
        match_response = requests.get(match_url, headers=headers)

        if match_response.status_code != 200:
            return jsonify({"error": "Match data not found or API error."}), 404

        match_data = match_response.json()
        wins = sum(1 for match in match_data["matches"] if match["win"])
        losses = sum(1 for match in match_data["matches"] if not match["win"])

        # Kazanma/Kaybetme oranlarını döndür
        return jsonify({
            "wins": wins,
            "losses": losses
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # API'yi dış dünyaya açarak çalıştırıyoruz
    app.run(host="0.0.0.0", port=5000, debug=False)
