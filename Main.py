from flask import Flask, render_template, jsonify, request,json

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/article', methods=['GET'])
def get_articles():
	file = json.load(open("articles.json"))
	articles = file["articles"]
	titles = []
	for title in articles:
		titles.append(title['title'])
	return render_template('browse.html', titles = titles)
	
	
@app.route('/addarticle', methods=['GET', 'POST'])
def add_article():
	return render_template('addarticle.html')
	
@app.route('/article/<articleTitle>', methods=['GET'])
def article_page(articleTitle):
	file = json.load(open('articles.json'))
	article = [item for item in file["articles"]
             if item["title"] == articleTitle]
	return render_template('articlepage.html', article=article)
	
@app.route('/done', methods=['POST'])
def done():
	article =  {
			'title': request.form['title'],
			'author': request.form['author'],
			'content': request.form['content'],
		}
	json_file = open("articles.json")
	data = json.load(json_file)
	data["articles"].append(article)
	json_file.close()
	
	newfile = open("articles.json", 'w')
	newfile.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
	newfile.close()
	return render_template('done.html')
	
@app.route('/edit/<name>', methods=['GET'])
def edit_article(name):
	file = json.load(open('articles.json'))
	article = [item for item in file["articles"]
             if item["title"] == name]
	return render_template('changearticle.html', article=article)
	
@app.route('/editdone/<title>', methods=['POST'])
def edit_done(title):
    with open('articles.json', 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            for articles in value:
                if(articles['title']== title):
                    data_dict = {
                    "title": request.form['title'],
                    "author": request.form['author'],
                    "content": request.form['content'],
                    }
                    data["articles"].append(data_dict)

                    for i in range(len(data["articles"])):
                        if data["articles"][i]["title"] == title:
                            data["articles"].pop(i)
                            break

    writing_file = open('articles.json', 'w')
    writing_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    writing_file.close()
    return render_template('donediting.html')
@app.route('/articleapi/<article>', methods=['GET'])
def api_article(article):
	file = json.load(open('articles.json'))
	article = [item for item in file["articles"] 
				if item["title"] == article]
	return jsonify(article)
	
@app.route('/articleapi', methods=['GET'])
def api():
	with open('articles.json') as input:
		articles = json.load(input)
		return jsonify(articles)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404
if __name__ == '__main__':
    app.debug = True
    app.run()