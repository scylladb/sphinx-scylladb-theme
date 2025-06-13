import os
import shutil
from urllib.parse import urlparse


def generate_template(template, **vars):
    """
    Replaces variables inside a template.

    :param template: Text with variables between brackets {}.
    :type src: str
    """

    return template.format(**vars)


def copy(src, dest):
    """
    Copies a file or a folder from src to dest.

    :param src: The path of the file to copy.
    :type src: str

    :param dest: The destination path.
    :type dest: str
    """

    if os.path.isfile(dest) or os.path.islink(dest):
        os.remove(dest)
    elif os.path.isdir(dest):
        shutil.rmtree(dest)
    if os.path.exists(src):
        try:
            shutil.copytree(src, dest)
        except Exception:
            shutil.copy(src, dest)


def build_redirect_body(path, zendesk_tag=""):
    """
    Builds the contents of the redirection file.

    :param path: Path to redirect to.
    :type path: str

    :param zendesk_tag: Zendesk tag.
    :type zendesk_tag: str

    :return: HTML body of the redirection.
    :rtype: str
    """

    zendesk_tag_html = (
        f'<meta name="zd-site-verification" content="{zendesk_tag}" />'
        if zendesk_tag
        else ""
    )

    html = generate_template(
        """
        <html>
        <head>
        {zendesk_tag_html}
        <meta http-equiv="refresh" content="0; url={path}">
        </head>
        </html>
        """,
        path=path,
        zendesk_tag_html=zendesk_tag_html,
    )
    return html


def is_url(path):
    """
    Checks if a path is an external url or a relative path.

    :param path: Path to evaluate.
    :type path: str

    :return: True if path is an external url.
    :rtype: bool
    """
    return bool(urlparse(path).netloc)


def resolve_link(link, env):
    """
    Resolves internal Sphinx links to proper URLs.
    
    :param link: The link to resolve (absolute or relative path).
    :type link: str
    
    :param env: The Sphinx environment object.
    :type env: sphinx.environment.BuildEnvironment
    
    :return: The resolved link URL.
    :rtype: str
    """
    if not link or is_url(link):
        return link
    
    # Handle anchor links
    if link.startswith('#'):
        return link
    
    if link.startswith('/'):
        # Absolute path: resolve from project root
        target_docname = link[1:]  # Remove leading slash
    else:
        # Relative path: resolve from current document's directory
        current_dir = os.path.dirname(env.docname)
        if current_dir:
            target_docname = os.path.normpath(os.path.join(current_dir, link)).replace(os.sep, '/')
        else:
            target_docname = link
    
    # Remove .html extension if present
    if target_docname.endswith('.html'):
        target_docname = target_docname[:-5]
    
    # Try to resolve the link
    if target_docname in env.found_docs:
        return env.app.builder.get_relative_uri(env.docname, target_docname)
    elif target_docname + '/index' in env.found_docs:
        return env.app.builder.get_relative_uri(env.docname, target_docname + '/index')
    else:
        # Fallback: add .html extension
        return target_docname + '.html'
