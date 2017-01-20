from invoke import task


@task
def serve():
    """start a development web server"""
    from creole.wsgi.app import CreoleApp
    app = CreoleApp('creole')
    app.run(host='0.0.0.0', port=8000, debug=True)
