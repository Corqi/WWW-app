from flask import render_template


def page_not_found(e):
    return render_template('error404.html'), 404
