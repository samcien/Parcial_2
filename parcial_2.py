from flask import Flask, render_template
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/consume')
def consume():
    return render_template('data.html', data=get_panama_vaccination_data())


def get_panama_vaccination_data():
    tree = ET.parse('templates/API_SH.IMM.MEAS_DS2_en_xml_v2_5381695.xml')
    root = tree.getroot()
    panama_data = []
    for data in root.findall("data"):
        for record in data.findall("record"):
            for field in record.findall("field"):
                if field.get("key") == "PAN":
                    panama_data.append({
                        "Country_or_Area": record.find("field[@name='Country or Area']").text,
                        "Item": record.find("field[@name='Item']").text,
                        "Year": record.find("field[@name='Year']").text,
                        "Value": record.find("field[@name='Value']").text
                    })
    return panama_data


if __name__ == '__main__':
    app.run(debug=True)