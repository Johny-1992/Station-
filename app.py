from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import pandas as pd
from fpdf import FPDF

# Pompes et becs avec carburants et prix par litre par défaut
POMPES = {
    "1a": {"carburant": "Essence", "prix": 3830},
    "1b": {"carburant": "Essence", "prix": 3830},
    "2a": {"carburant": "Essence", "prix": 3830},
    "2b": {"carburant": "Mazout", "prix": 3960},
    "3a": {"carburant": "Essence", "prix": 3200},
    "3b": {"carburant": "Mazout", "prix": 3960}
}

class StationAppleApp(App):
    def build(self):
        self.title = "STATION APPLE"
        self.inputs = {}
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Grille des pompes et becs
        grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for bec, info in POMPES.items():
            # Label bec
            grid.add_widget(Label(text=f"Bec {bec} ({info['carburant']})"))

            # Index début
            self.inputs[f"{bec}_start"] = TextInput(multiline=False, hint_text="Index début")
            grid.add_widget(self.inputs[f"{bec}_start"])

            # Index fin
            self.inputs[f"{bec}_end"] = TextInput(multiline=False, hint_text="Index fin")
            grid.add_widget(self.inputs[f"{bec}_end"])

        layout.add_widget(grid)

        # Prix par litre modifiable
        price_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        price_layout.bind(minimum_height=price_layout.setter('height'))
        self.price_inputs = {}
        for bec, info in POMPES.items():
            price_layout.add_widget(Label(text=f"{bec} prix/litre"))
            self.price_inputs[bec] = TextInput(text=str(info['prix']), multiline=False)
            price_layout.add_widget(self.price_inputs[bec])
        layout.add_widget(Label(text="Modifier les prix si nécessaire :"))
        layout.add_widget(price_layout)

        # Bouton calcul
        calc_btn = Button(text="Calculer ventes")
        calc_btn.bind(on_press=self.calculer_ventes)
        layout.add_widget(calc_btn)

        # Résultat
        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        return layout

    def calculer_ventes(self, instance):
        result_text = ""
        ventes_data = []

        for bec, info in POMPES.items():
            try:
                start = int(self.inputs[f"{bec}_start"].text)
                end = int(self.inputs[f"{bec}_end"].text)
                prix = float(self.price_inputs[bec].text)
                litres = end - start
                montant = litres * prix
                result_text += f"{bec} ({info['carburant']}) : {litres} L, Total {montant} FC\n"
                ventes_data.append({
                    "Bec": bec,
                    "Carburant": info['carburant'],
                    "Litres": litres,
                    "Prix/L": prix,
                    "Montant": montant
                })
            except ValueError:
                result_text += f"{bec} : Entrée invalide\n"

        self.result_label.text = result_text

        # Export PDF et Excel
        self.export_pdf(ventes_data)
        self.export_excel(ventes_data)

    def export_pdf(self, ventes):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport des ventes - STATION APPLE", ln=True, align="C")
        pdf.ln(10)
        for v in ventes:
            pdf.cell(200, 10, txt=f"{v['Bec']} ({v['Carburant']}) : {v['Litres']} L - {v['Montant']} FC", ln=True)
        pdf.output("ventes_station.pdf")

    def export_excel(self, ventes):
        df = pd.DataFrame(ventes)
        df.to_excel("ventes_station.xlsx", index=False)

if __name__ == "__main__":
    StationAppleApp().run()
