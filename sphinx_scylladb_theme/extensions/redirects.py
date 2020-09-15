import os
import yaml

# Generate a redirection HTML file
def write_html_redirect(redirect_to):
    html = "<html><head><meta http-equiv=\"refresh\" content=\"0; url=" + redirect_to + "\"></head></html>"
    return html

def create_redirects(app, docname):
    if not app.config.redirects_file:
        return
    if not os.path.exists(app.config.redirects_file):
        return
    if not app.builder.name == 'dirhtml':
        return
    with open(app.config.redirects_file, 'r') as yaml_file:
        full_load = yaml.full_load(yaml_file)
        if full_load:
            for from_path, redirect_to in full_load.items():
                target_path = app.outdir + '/' + from_path
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                with open(os.path.join(target_path + '/index.html'), 'w') as t_file:
                    t_file.write(write_html_redirect(redirect_to))

def setup(app):
    app.add_config_value('redirects_file', '', 'html')
    app.connect('build-finished', create_redirects)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
