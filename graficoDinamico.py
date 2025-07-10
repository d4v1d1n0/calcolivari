# Definizione delle variabili richieste
giorni_utili = 0  # Sostituisci 0 con il valore corretto o una lista, se necessario
x_labels = []     # Sostituisci con la lista delle etichette dei giorni
ore_A = []        # Sostituisci con la lista delle ore per Persona A
ore_B_default = [] # Sostituisci con la lista di default per Persona B

dash_code_v2 = f'''
from dash import Dash, dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

app = Dash(__name__)
server = app.server

giorni_utili = {giorni_utili}
x_labels = {x_labels}
ore_A = {ore_A}
totale_target = sum(ore_A)

# Inizializzazione ore_B come lista di default
ore_B_default = {ore_B_default}

app.layout = html.Div([
    html.H1("Analisi distribuzione ore di lavoro - UNITS Racing Team"),
    html.Div(id="input-container", children=[
        html.Div([
            html.Label(x_labels[i]),
            dcc.Input(id=f"input-{{i}}", type="number", value=ore_B_default[i], step=0.1, min=0, style={{"width": "80px"}})
        ], style={{"display": "inline-block", "margin": "5px"}})
        for i in range(len(x_labels))
    ]),
    html.Div(id="total-output", style={{"marginTop": "20px", "fontWeight": "bold"}}),
    dcc.Graph(id="grafico")
])

@app.callback(
    [Output(f"input-{{i}}", "value") for i in range(len(x_labels))] +
    [Output("grafico", "figure"),
     Output("total-output", "children")],
    [Input(f"input-{{i}}", "value") for i in range(len(x_labels))],
    prevent_initial_call=False
)
def aggiorna_ore(*inputs):
    ore_B = list(inputs)
    changed = ctx.triggered_id

    if changed:
        index_changed = int(changed.split("-")[1])
        ore_modificate = ore_B.copy()
        ore_modificate[index_changed] = inputs[index_changed]
        somma_attuale = sum(ore_modificate)

        if somma_attuale > totale_target:
            surplus = somma_attuale - totale_target
            altri_indici = [i for i in range(len(ore_modificate)) if i != index_changed and ore_modificate[i] > 0]
            somma_altri = sum(ore_modificate[i] for i in altri_indici)

            for i in altri_indici:
                proporzione = ore_modificate[i] / somma_altri if somma_altri != 0 else 1 / len(altri_indici)
                ore_modificate[i] = max(0, ore_modificate[i] - surplus * proporzione)

        ore_B = ore_modificate

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_labels, y=ore_A,
        mode='lines+markers',
        name='Persona A (costante)',
        line=dict(color='green', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=x_labels, y=ore_B,
        mode='lines+markers',
        name='Persona B (bilanciata)',
        line=dict(color='orange', width=3, dash='dash')
    ))

    fig.update_layout(
        title="Confronto tra Persona A (fissa) e Persona B (dinamica)",
        xaxis_title="Giorni di agosto (lavorativi)",
        yaxis_title="Ore di lavoro giornaliere",
        hovermode="x unified",
        template="plotly_white",
        height=600
    )

    total_text = f"Totale ore Persona B: {{sum(ore_B):.2f}} h su {{totale_target}} h"

    return ore_B + [fig, total_text]

if __name__ == "__main__":
    app.run(debug=True)
'''

# Scrivo il file aggiornato
file_path_v2 = "app_fsae_bilanciamento_dinamico.py"
with open(file_path_v2, "w") as f:
    f.write(dash_code_v2)

file_path_v2