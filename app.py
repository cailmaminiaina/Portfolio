from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)


@app.route('/')
def index():
    projects = [
        {
            'title': 'Projet 1',
            'description': 'Un site web vitrine de tourisme pour notre agence de voyage en utilisant Python avec le framework Django. (Décembre 2022)',
            'image': 'project1.png',
            'url': 'https://laicriritravel.onrender.com'
        },
        {
            'title': 'Projet 2',
            'description': 'Un chatbot messenger basé sur Python et OpenAI "ChatBot 2.0". (Mars 2023)',
            'image': 'project2.png',
            'url': 'https://facebook.com/share/19VRFDWHMt'
        },
        {
            'title': 'Projet 3',
            'description': 'Un chatbot messenger pour les entreprises pour automatoier avec l´Intelligence Artificiel le service client. (Mémoire Licence - Novembre 2024)',
            'image': 'project3.jpg',
            'url': 'https://github.com/cailmaminiaina/AI-ChatBot-for-Companies'
        },
        {
            'title': 'Projet 4',
            'description': 'Mon portfolio en utilisant Python avec le framework Flask. (Décembre 2024)',
            'image': 'profile.png',
            'url': '/'
        }
    ]
    return render_template('index.html', projects=projects)

@app.route('/download-cv')
def download_cv():
    return send_from_directory(
        os.path.join(app.root_path, 'static/images'),
        'Mon CV.pdf',
        as_attachment=True
    )
if __name__ == '__main__':
    app.run(debug=True)
