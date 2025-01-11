from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

RIOT_API_KEY = "RGAPI-759a30f4-318d-44fe-91b7-e3fabd5bc9e9"

@app.route('/<summoner_name>/<tag>/<region>/rank', methods=['GET'])
def get_rank(summoner_name, tag, region):
    try:
        summoner_name = summoner_name.replace(' ', '%20')  # Boşlukları düzelt
        full_name = f"{summoner_name}/{tag}"  # İsim ve tag birleştir
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

        # Rank bilgilerini JSON olarak döndür
        rank_info = rank_data[0]  # İlk sıralama verisini al (Solo/Duo genelde ilk sırada)
        return jsonify({
            "summoner": full_name,
            "tier": rank_info.get("tier"),
            "rank": rank_info.get("rank"),
            "lp": rank_info.get("leaguePoints")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
