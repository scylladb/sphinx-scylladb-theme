import os
import yaml

# Generate a redirection HTML file
def write_html_redirect(redirect_to):
    html = "<html><head><meta http-equiv=\"refresh\" content=\"0; url=" + redirect_to + "\"></head></html>"
    return html

def create_redirects(app, docname):
    redirects_file = app.config.redirects_file
    if not redirects_file:
        return
    if os.path.exists('docs'):
        redirects_file = 'docs/' + redirects_file
    if not os.path.exists(redirects_file):
        return
    with open(redirects_file, 'r') as yaml_file:
        full_load = yaml.full_load(yaml_file)
        if full_load:
            for from_path, redirect_to in full_load.items():
                target_path = app.outdir + '/' + from_path
                if os.getenv("SPHINX_MULTIVERSION_NAME") is not None:
                    redirect_to = '/' + os.environ['SPHINX_MULTIVERSION_NAME'] + redirect_to
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                with open(os.path.join(target_path + '/index.html'), 'w') as t_file:
                    t_file.write(write_html_redirect(redirect_to))
                with open(os.path.join(target_path + '.html'), 'w') as t_file:
                    t_file.write(write_html_redirect(redirect_to))

def setup(app):
    app.add_config_value('redirects_file', '', 'html')
    app.connect('build-finished', create_redirects)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
