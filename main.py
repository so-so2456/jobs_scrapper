from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("Scrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    from_db = db.get(word)
    if from_db:
      jobs = from_db
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")

  return render_template(
    "report.html",
    searching_by=word,
    result_number=len(jobs),
    jobs=jobs
  )

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file(
      'jobs.csv',
      mimetype='text/csv',
      attachment_filename='jobs.csv',
      as_attachment=True
    )
  except:
    return redirect("/")

app.run(host="0.0.0.0")