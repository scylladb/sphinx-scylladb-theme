Contributing to Scylla
======================
Scylla developers use patches and email to share and discuss changes. Setting up can take a little time, but once you have done it the first time, it’s easy.

The basic steps are:

* Join Scylla community - `Contributor License Agreement <http://www.scylladb.com/opensource/cla>`_
* Create a Git branch to work on
* Commit your work with clear commit messages and sign-offs.
* Use ``git format-patch`` and ``git send-email`` to send to the list

Commit locally to your git tree and then prepare patches that you send to the mailing list.

First, make your name and email address are configured for git:

.. code-block:: shell

   git config user.name "Your Name"
   git config user.email "your@mail.com"

Also configure git to detect renames and copies to make ``git format-patch`` output easier to review:

.. code-block:: shell

   git config --global diff.renames copies

Then, make your modifications in your own private branch:

.. code-block:: shell

   git checkout -b features/foo # branches from master

To commit changes, do:

.. code-block:: shell

   git commit -a -s # commit everything, signoff the patches

Commit messages and Signed-Off-By
---------------------------------
Please prepare a commit message for every commit. See `A Note About Git Commit Messages <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_ for information on how to write a good commit message.

Your commit message should begin with a short (50 characters or fewer) summary line.

Commit messages should have a Signed-Off-By line. Your Signed-Off-By is your certification that you agree to a Certification of Origin.

   “By making a contribution to this project, I certify that:

   The contribution was created in whole or in part by me and I have the right to submit it under the open source license indicated in the file; or

   The contribution is based upon previous work that, to the best of my knowledge, is covered under an appropriate open source license and I have the right under that license to submit that work with modifications, whether created in whole or in part by me, under the same open source license (unless I am permitted to submit under a different license), as indicated in the file; or

   The contribution was provided directly to me by some other person who certified (a), (b) or (c) and I have not modified it.

   I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.”

This sign-off procedure is taken from the `Linux Kernel Certificate of Origin <https://developercertificate.org/>`_, version 1.1.

Sending commits as patches
--------------------------
Once you have commits you want to send out, use git format-patch to generate them.

For multiple patches, use:

.. code-block:: shell

   git format-patch -n --cover-letter master

for a single patch:

.. code-block:: shell

   git format-patch -1

Verify the generated patch files and then use git send-email to send them out:

.. code-block:: shell

   git send-email  --to scylladb-dev@googlegroups.com 00*.patch

If you need to send more than one revision of the patch, please remember to use patch versioning:

.. code-block:: shell

   git format-patch --subject-prefix="PATCH v2"

**protip**: To save time, you can also combine the ``format-patch`` and ``send-email`` steps.

``git send-email --to ... --cover-letter --annotate -v1 origin/master..``

Contributor Agreement

If you have not already signed a `Contributor Agreement <http://www.scylladb.com/opensource/cla>`_, you will need to send in a signed copy before your patches can be applied.

References
----------
* `Man page for git send-email <https://kernel.org/pub/software/scm/git/docs/git-send-email.html>`_
* You can find information on how to configure git to use gmail here: `Configuring git send-email to use Gmail SMTP <http://morefedora.blogspot.se/2009/02/configuring-git-send-email-to-use-gmail.html>`_

Questions?
----------
Ask on the `scylladb-dev <https://groups.google.com/d/forum/scylladb-dev>`_ list
