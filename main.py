from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
import pickle
import numpy as np
import pandas as pd  # For DataFrame

class CNGPdMApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.model = self.load_model()
        self.features = self.load_features()
        
        self.add_widget(Label(text="CNG PdM: Engine Fault Predictor", size_hint_y=0.1))
        
        self.overheat = Slider(min=0, max=1, value=0, step=1)
        self.add_widget(Label(text="Overheat? (0=No, 1=Yes)"))
        self.add_widget(self.overheat)
        
        self.knock = Slider(min=0, max=1, value=0, step=1)
        self.add_widget(Label(text="Knock? (0=No, 1=Yes)"))
        self.add_widget(self.knock)
        
        self.shutdown = Slider(min=0, max=1, value=0, step=1)
        self.add_widget(Label(text="Shutdown? (0=No, 1=Yes)"))
        self.add_widget(self.shutdown)
        
        self.emission = Slider(min=0, max=1, value=0, step=1)
        self.add_widget(Label(text="Emission Smell? (0=No, 1=Yes)"))
        self.add_widget(self.emission)
        
        self.poor_accel = Slider(min=0, max=1, value=0, step=1)
        self.add_widget(Label(text="Poor Acceleration? (0=No, 1=Yes)"))
        self.add_widget(self.poor_accel)
        
        self.diff_start = Slider(min=0, max=1, value=0, step=1)
        self.add_widget(Label(text="Difficult Start? (0=No, 1=Yes)"))
        self.add_widget(self.diff_start)
        
        terrain_btn = Button(text="Terrain: 0 - City roads")
        terrain_btn.bind(on_press=self.set_terrain)
        self.add_widget(terrain_btn)
        self.terrain_val = 0
        
        self.idling = Slider(min=0, max=1, value=0, step=1)
        self.add_widget(Label(text="Frequent Idling? (0=No, 1=Yes)"))
        self.add_widget(self.idling)
        
        self.used = Slider(min=0, max=1, value=0, step=1)
        self.add_widget(Label(text="Used Conversion? (0=No, 1=Yes)"))
        self.add_widget(self.used)
        
        predict_btn = Button(text="Predict Risk")
        predict_btn.bind(on_press=self.predict)
        self.add_widget(predict_btn)
        
        self.result = Label(text="")
        self.add_widget(self.result)
    
    def load_model(self):
        with open('rf_model_refined.pkl', 'rb') as f:
            return pickle.load(f)
    
    def load_features(self):
        with open('features_refined.txt', 'r') as f:
            return eval(f.read())
    
    def set_terrain(self, instance):
        dropdown = DropDown()
        terrains = ["0 - City roads", "1 - Rough terrain", "2 - Highways", "3 - Hilly terrain", "4 - City & hilly"]
        for i, t in enumerate(terrains):
            btn = Button(text=t, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn, val=i: self.update_terrain(val))
            dropdown.add_widget(btn)
        dropdown.open(instance)
    
    def update_terrain(self, val):
        self.terrain_val = val
        self.terrain_btn.text = f"Terrain: {val} - {['City roads', 'Rough terrain', 'Highways', 'Hilly terrain', 'City & hilly'][val]}"
    
    def predict(self, instance):
        inputs = {feat: np.mean(self.model.feature_importances_) for feat in self.features}
        inputs['has_overheat'] = self.overheat.value
        inputs['has_knock'] = self.knock.value
        inputs['has_shutdown'] = self.shutdown.value
        inputs['has_emission_smell'] = self.emission.value
        inputs['has_poor_accel'] = self.poor_accel.value
        inputs['has_difficult_start'] = self.diff_start.value
        inputs['Terrain'] = self.terrain_val
        inputs['Idling'] = self.idling.value
        inputs['Used?'] = self.used.value
        input_df = pd.DataFrame([inputs], columns=self.features)
        
        prob = self.model.predict_proba(input_df)[0][1]
        risk = f"{prob:.1%} Fault Risk"
        prominent = []
        if self.overheat.value: prominent.append("overheat")
        if self.knock.value: prominent.append("knock")
        if self.shutdown.value: prominent.append("shutdown")
        if self.emission.value: prominent.append("emission smell")
        if self.poor_accel.value: prominent.append("poor acceleration")
        if self.diff_start.value: prominent.append("difficult start")
        
        if prob > 0.5:
            if prominent:
                if "overheat" in prominent and "knock" in prominent:
                    rec = "Check valves and cooling system for thermal wear."
                elif "emission smell" in prominent or "poor acceleration" in prominent:
                    rec = "Inspect injectors/regulators for fouling or leaks."
                elif "difficult start" in prominent or "shutdown" in prominent:
                    rec = "Examine spark plugs/ignition for dry gas issues."
                else:
                    rec = "Schedule general CNG retrofit inspection."
                alert = f"🚨 High Risk: {rec} in <1000km."
            else:
                alert = "🚨 High Risk: Schedule general valve/spark check in <1000km (CNG wear)."
        else:
            alert = "✅ Low Risk: Monitor weekly."
        self.result.text = f"{risk}\n{alert}"

class MainApp(App):
    def build(self):
        return CNGPdMApp()

if __name__ == '__main__':
    MainApp().run()