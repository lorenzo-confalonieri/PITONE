from flask import Flask, render_template, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

pokemon_data = pd.read_csv('pokemon (1).csv')
punti_utente = 100
collezione = []

probabilita_rarita = ['Comune'] * 70 + ['Non Comune'] * 20 + ['Rara'] * 9 + ['Ultra Rara'] * 1

def apri_pacchetto():
    pacchetto = []
    punti_guadagnati = 0
    i = 0
    while i < 5:
        rarita_scelta = random.choice(probabilita_rarita)
        carte_disponibili = pokemon_data[pokemon_data['Rarità'] == rarita_scelta]
        if len(carte_disponibili) > 0:
            carta = carte_disponibili.iloc[random.randint(0, len(carte_disponibili) - 1)]
            pacchetto.append(carta.to_dict())
            if rarita_scelta == 'Comune':
                punti_guadagnati += 1
            elif rarita_scelta == 'Non Comune':
                punti_guadagnati += 10
            elif rarita_scelta == 'Rara':
                punti_guadagnati += 30
            elif rarita_scelta == 'Ultra Rara':
                punti_guadagnati += 104
            i += 1
    return pacchetto, punti_guadagnati

def salva_collezione_su_file():
    collezione_df = pd.DataFrame(collezione)
    collezione_df.to_csv('collezione.csv', index=False)

def carica_collezione_da_file():
    global collezione
    try:
        collezione = pd.read_csv('collezione.csv').to_dict(orient='records')
    except FileNotFoundError:
        collezione = []

carica_collezione_da_file()

@app.route('/')
def home():
    return render_template('index.html', punti_utente=punti_utente, collezione=collezione)

@app.route('/apri_pacchetto', methods=['POST'])
def apri_pacchetto_route():
    global punti_utente, collezione
    if punti_utente >= 10:
        punti_utente -= 10
        pacchetto, punti_guadagnati = apri_pacchetto()
        collezione.extend(pacchetto)
        salva_collezione_su_file()
        punti_utente += punti_guadagnati
    return redirect(url_for('home'))

@app.route('/mostra_collezione', methods=['GET'])
def mostra_collezione_route():
    return render_template('collezione.html', collezione=collezione)

@app.route('/mostra_punti', methods=['GET'])
def mostra_punti_route():
    return render_template('punti.html', punti_utente=punti_utente)

if __name__ == '__main__':
    app.run(debug=True)