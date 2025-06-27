
import os
import base64
import anthropic
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

    try:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_file.mimetype,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Jsi zkušený odborník na analýzu jídla a výživu. Tvým úkolem je analyzovat fotografii jídla a poskytnout detailní informace o něm. Zde je fotografie jídla, kterou budeš analyzovat: <fotografie_jidla> {{IMAGE}} </fotografie_jidla> Pečlivě si prohlédni všechny detaily zobrazené na fotografii. Zaměř se na ingredience, způsob přípravy, velikost porce a celkový vzhled jídla. Před poskytnutím konečné odpovědi proveď důkladnou analýzu v následujících krocích. 1. Popis jídla: - Popiš, co vidíš na fotografii, včetně textury, barvy a prezentace - Identifikuj hlavní ingredience - Odhadni způsob přípravy - Odhadni přesnou velikost porce 2. Kulturní kontext: - Zvaž možný původ jídla a jeho kulturní význam - Navrhni potenciální variace tohoto jídla 3. Návrh názvu: - Na základě pozorování navrhni vhodný český název pro toto jídlo - Ujisti se, že název je výstižný a popisný 4. Odhad kalorické hodnoty: - Zvaž viditelné ingredience a jejich přibližné množství - Vezmi v úvahu odhadnutou velikost porce - Odhadni přibližnou kalorickou hodnotu a zdůvodni svůj odhad 5. Základní informace: - Shrň klíčové informace o jídle (např. původ, typické použití, variace) 6. Zdravotní benefity: - Identifikuj potenciální pozitivní účinky jídla na zdraví - Zvaž nutriční hodnotu jednotlivých ingrediencí 7. Zdravotní rizika: - Zvaž možná zdravotní rizika spojená s konzumací tohoto jídla - Vezmi v úvahu alergeny, vysoký obsah tuku nebo cukru, apod. Na základě své analýzy nyní poskytni strukturovanou odpověď v následujícím formátu: Název jídla: [Navržený název jídla v češtině] Kalorická hodnota: [Odhadovaná kalorická hodnota jídla v češtině, včetně zdůvodnění odhadu] Poznámky: [Základní informace o jídle] Zdravotní benefity: [Seznam potenciálních pozitivních účinků na zdraví] Zdravotní rizika: [Seznam možných zdravotních rizik] Ujisti se, že tvá odpověď je v češtině a obsahuje všechny požadované sekce. Buď konkrétní a výstižný ve svých popisech a odhadech."
                        }
                    ],
                }
            ],
        )
        return jsonify({'analysis': message.content[0].text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
