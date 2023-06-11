from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/contributors', methods=['GET'])
def contributors():
    return render_template('contributors.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/result', methods=['POST'])
def result():
    username = request.form['user-org']
    repo = request.form['repo']
    inp = request.form['inp']

    iurl = f'https://github.com/{username}/{repo}'
    all_url = f'{iurl}/issues'
    gfi_url = f'{iurl}/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22'
    doc_url = f'{iurl}/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation'

    if inp == '1':
        res_gfi = requests.get(gfi_url)
        soup_gfi = BeautifulSoup(res_gfi.text, 'html.parser')
        issues = soup_gfi.find_all('a', {'class': 'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'})
        issue_data = []
        for issue in issues:
            issue_number = issue['href'].split('/')[-1]
            issue_data.append({'number': issue_number, 'title': issue.text.strip(), 'link': f'{iurl}/issues/{issue_number}'})
        return render_template('result.html', issues=issue_data)

    elif inp == '2':
        res_doc = requests.get(doc_url)
        soup_doc = BeautifulSoup(res_doc.text, 'html.parser')
        issues = soup_doc.find_all('a', {'class': 'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'})
        issue_data = []
        for issue in issues:
            issue_number = issue['href'].split('/')[-1]
            issue_data.append({'number': issue_number, 'title': issue.text.strip(), 'link': f'{iurl}/issues/{issue_number}'})
        return render_template('result.html', issues=issue_data)

    elif inp == '3':
        page = 1
        all_issues = []
        while True:
            url = f'{all_url}?page={page}'
            res_all = requests.get(url)
            soup_all = BeautifulSoup(res_all.text, 'html.parser')
            issues = soup_all.find_all('a', {'class': 'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'})
            if not issues:
                break
            for issue in issues:
                issue_number = issue['href'].split('/')[-1]
                all_issues.append({'number': issue_number, 'title': issue.text.strip(), 'link': f'{iurl}/issues/{issue_number}'})
            page += 1
        return render_template('result.html', issues=all_issues)

    else:
        return "Type the correct number."


if __name__ == '__main__':
    app.run(debug=True)
