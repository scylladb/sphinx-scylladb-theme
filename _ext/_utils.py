def generate_template(template, **vars):
    return template.format(**vars)

def generate_styles(**styles):
    return ''.join(['{}:{};'.format(k, v) for k, v in styles.items() if v])

def generate_content(*lines, line_break='\n'):
    return line_break.join([line for line in lines])
