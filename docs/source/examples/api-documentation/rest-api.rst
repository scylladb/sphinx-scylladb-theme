:toc-depth: 4

REST API (Redocly)
==================

The ScyllaDB Cloud documentation uses `Redocly <https://redocly.com/>`_ to render OpenAPI/Swagger specifications as interactive API documentation.

.. note::

   Currently, only `ScyllaDB Cloud Docs <https://cloud.docs.scylladb.com/stable/api.html>`_ uses REST API documentation with Redocly.

   **Interested in making this a reusable extension?** Let us know in this `issue #722 <https://github.com/scylladb/sphinx-scylladb-theme/issues/722>`_.

How it works
------------

The extension:

1. Downloads the OpenAPI specification from the configured URL
2. Generates code snippets (e.g., curl examples) using ``snippet-enricher-cli``
3. Saves the enriched spec to ``_static/swagger.json``
4. Renders the API documentation using Redocly at ``/api.html``

Prerequisites
-------------

Install the required dependencies:

.. code-block:: bash

   poetry add requests
   npm install -g snippet-enricher-cli

Configuration
-------------

Add to ``conf.py``
~~~~~~~~~~~~~~~~~~

Configure the OpenAPI extension and specify the spec URL:

.. code-block:: python

   extensions = [
       # ... other extensions
       "scylladb_openapi"
   ]

   # Additional pages
   html_additional_pages = {'api': 'api.html'}

   # Additional static paths
   html_static_path = ['openapi']

   # Custom CSS
   html_css_files = [
       'custom.css',
   ]

   # OpenAPI configuration
   scylladb_openapi_url = 'https://api.cloud.scylladb.com/api-docs.json'
   scylladb_openapi_server_url = 'https://api.cloud.scylladb.com'
   scylladb_openapi_output_file = '/_static/swagger.json'

Create the extension
~~~~~~~~~~~~~~~~~~~~

Create ``_ext/scylladb_openapi.py``:

.. code-block:: python

   # -*- coding: utf-8 -*-
   import json
   import requests
   import subprocess

   def build_openapi_spec(app, exception) -> None:
       config = app.config
       output_file = app.outdir + config.scylladb_openapi_output_file
       spec_url = config.scylladb_openapi_url
       server_url = config.scylladb_openapi_server_url

       download_openapi_spec(output_file, spec_url, server_url)
       generate_code_snippets(output_file)

   def download_openapi_spec(output_file, spec_url, server_url) -> None:
       print("Downloading OpenAPI spec from: " + spec_url)
       response = requests.get(spec_url, allow_redirects=True)
       content = json.loads(response.text)

       # Set the production URL
       content["servers"][0]["url"] = server_url

       with open(output_file, "w+") as file:
           json.dump(content, file)
           print("OpenAPI document downloaded to: " + output_file)

   def generate_code_snippets(output_file) -> None:
       cmd = f"snippet-enricher-cli --targets='shell_curl' --input={output_file}"

       process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

       out, err = process.communicate()
       errcode = process.returncode

       if errcode != 0:
           raise Exception("Error generating code snippets: " + str(err))

       # Decode URL-encoded placeholders
       modified_content = out.decode().replace('%7B', '{').replace('%7D', '}')

       with open(output_file, "w+") as file:
           file.write(modified_content)
           print("Code snippets generated to: " + output_file)

   def setup(app):
       app.connect('build-finished', build_openapi_spec)
       app.add_config_value(
           "scylladb_openapi_url",
           default="https://api.cloud.scylladb.com/api-docs.json",
           rebuild="html",
       )
       app.add_config_value(
           "scylladb_openapi_server_url",
           default="https://api.cloud.scylladb.com",
           rebuild="html",
       )
       app.add_config_value(
           "scylladb_openapi_output_file",
           default="/_static/swagger.json",
           rebuild="html",
       )

Create the template
~~~~~~~~~~~~~~~~~~~

Create ``_templates/api.html``:

.. code-block:: jinja

   {% extends "!layout.html" %}

   {% block title %} API Reference | Scylla Docs {% endblock %}

   {% set openapi_path = pathto('_static/swagger.json', 1) %}

   {% block scripts %}
   <script type="text/javascript" src="{{ pathto('_static/js/runtime.bundle.js', 1) }}"></script>
   <script type="text/javascript" src="{{ pathto('_static/js/main.bundle.js', 1) }}"></script>
   {% include 'scylladb-scripts.html' %}
   {% include 'local-scripts.html' %}
   {% endblock %}

   {% set hide_pre_content = "true" %}
   {% set hide_post_content = "true" %}
   {% set hide_sidebar = "true" %}
   {% set hide_secondary_sidebar = "true" %}
   {% set full_width = "true" %}

   {% set body ="<div id='redoc'></div>
   <script src='https://cdn.redoc.ly/redoc/v2.1.3/bundles/redoc.standalone.js'></script>
   <script>
       function getCssVariableValue(variable) {
           return getComputedStyle(document.documentElement)
               .getPropertyValue(variable).trim();
       }

       function calculateScrollOffset(element1Selector, element2Selector) {
           const element1 = document.querySelector(element1Selector);
           const element2 = document.querySelector(element2Selector);
           const element1Height = element1 ? element1.offsetHeight : 0;
           const element2Height = element2 ? element2.offsetHeight : 0;
           return element1Height + element2Height;
       }

       function initializeRedoc() {
           const textColor = getCssVariableValue('--text-color');
           const primaryColor = getCssVariableValue('--primary-color');
           const linkColor = getCssVariableValue('--link-color');
           const sidebarBackgroundColor = getCssVariableValue('--navigation-bg');
           const borderColor = getCssVariableValue('--border-color');
           const scrollOffset = calculateScrollOffset('.header', '.promo-banner');

           Redoc.init('" + openapi_path + "', {
               scrollYOffset: scrollOffset,
               hideDownloadButton: true,
               theme: {
                   sidebar: {
                       backgroundColor: sidebarBackgroundColor,
                       width: '357px',
                       textColor: textColor,
                   },
                   colors: {
                       primary: { main: textColor },
                   },
                   typography: {
                       fontFamily: 'Roboto, sans-serif',
                       fontSize: '16px',
                   },
               },
           }, document.getElementById('redoc'));
       }

       document.addEventListener('DOMContentLoaded', function() {
           document.documentElement.classList.add('openapi-page');
           initializeRedoc();
       });
   </script>
   " %}

Custom styling
~~~~~~~~~~~~~~

Create ``_static/custom.css`` to style Redocly:

.. code-block:: css

   /* Reset scroll padding */
   .openapi-page {
       scroll-padding-top: 0 !important;
   }

   .openapi-page .content-body {
       padding: 0;
   }

   /* Sidebar styling */
   #redoc .menu-content .scrollbar-container > ul {
       padding: 30px 40px;
   }

   #redoc .menu-content ul ul {
       border-left: 1px solid var(--link-color);
       margin-left: 20px;
   }

   #redoc .menu-content label.active,
   #redoc .menu-content label:hover {
       color: var(--link-color);
       background: transparent;
   }

   /* Right panel */
   #redoc .http-verb {
       border-radius: 4px;
   }

   #redoc code {
       color: inherit;
       background: transparent;
   }
