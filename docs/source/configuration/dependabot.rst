Dependabot support
==================

`Dependabot <https://docs.github.com/en/code-security/getting-started/dependabot-quickstart-guide>`_ is a GitHub-native service that helps you automatically check and manage dependency updates.
This is especially useful in environments like our toolchain, where frequent and consistent updates to critical dependencies (such as Sphinx-related packages) are needed to ensure the toolchain remains current and secure.

This page explains how to configure the Dependabot file to manage dependency updates specifically for ScyllaDB documentation projects.
You will find information on customizing update intervals, limiting updates to specific dependencies, and responding to vulnerability alerts.

Enable dependabot
-----------------

To enable Dependabot for your project, create a ``.github/dependabot.yml`` file in the root directory of your repository.
Dependabot will read this configuration and manage dependency updates as specified.

Below is an example configuration file for limiting updates to specific dependencies within the Sphinx toolchain:

.. literalinclude:: /upgrade/_partials/dependabot_template.yml

Customize update frequency
--------------------------

- **Interval options:** You can adjust the ``interval`` setting to specify how often Dependabot checks for updates. Options include ``"daily"``, ``"weekly"``, or ``"monthly"``.

- **Allowed dependencies:** By listing specific dependencies under ``allow``, you limit updates only to those dependencies, preventing unwanted notifications for other updates.

Handle vulnerability alerts
---------------------------

In case of a vulnerability alert, projects are responsible for keeping dependencies secure and up-to-date.
Generally, this can be handled by frequently merging new Sphinx Theme versions through automated pull-requests, which will include the latest versions of direct dependencies.

For dependencies that do not strictly depend on the theme, you may need to run a manual update.

To update all dependencies to the latest versions, use:

.. code-block:: bash

   cd docs
   make update

Then, commit the updated ``poetry.lock`` file and push the changes to the repository.
