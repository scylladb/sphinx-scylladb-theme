Videos
======

You can embed videos in your documentation using iframes. This is particularly useful for YouTube videos or other video hosting platforms.

Basic iframe
------------

To embed a video using an iframe, use the ``raw`` directive with HTML content.

.. code-block:: rst

   .. raw:: html

      <iframe width="560" height="315" style="max-width: 100%; margin-bottom: 1rem;" src="https://www.youtube.com/embed/-nPO9KeNydM?si=nE0Tpy7wM8D6fFYU" 
              title="YouTube video player" frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
              referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
      </iframe>

Renders as:

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/-nPO9KeNydM?si=nE0Tpy7wM8D6fFYU" 
           title="YouTube video player" frameborder="0" 
           allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
           referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
   </iframe>

Responsive iframe
-----------------

To make the iframe responsive and take the full width of the container while maintaining the aspect ratio, wrap it in a container div with appropriate styling.

.. code-block:: rst

   .. raw:: html

      <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1rem;">
         <iframe src="https://www.youtube.com/embed/-nPO9KeNydM?si=nE0Tpy7wM8D6fFYU" 
                 title="YouTube video player" 
                 frameborder="0" 
                 allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                 referrerpolicy="strict-origin-when-cross-origin" 
                 allowfullscreen
                 style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
         </iframe>
      </div>

Renders as:

.. raw:: html

   <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1rem;">
      <iframe src="https://www.youtube.com/embed/-nPO9KeNydM?si=nE0Tpy7wM8D6fFYU" 
              title="YouTube video player" 
              frameborder="0" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
              referrerpolicy="strict-origin-when-cross-origin" 
              allowfullscreen
              style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
      </iframe>
   </div>

The wrapper div uses a padding-bottom trick to maintain a 16:9 aspect ratio (56.25% = 9/16 * 100%). The iframe is positioned absolutely within this container, allowing it to scale responsively while maintaining the correct proportions.

Tips
----

* **Aspect ratio**: Adjust ``padding-bottom`` to change the aspect ratio. For 16:9 use 56.25%, for 4:3 use 75%.
* **Start time**: Add ``?start=60`` to start the video at a specific time (60 seconds in this example).

