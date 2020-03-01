Data model for a social reader application
==========================================
**Topic: Data modeling**

**Learn: How to model data efficiently for Scylla using CQL**

**Audience: Application developers using CQL**

Applications for reading and sharing news and other text online are
always changing. From Slashdot to StumbleUpon to Planet, somehow it
seems like nobody quite has it right yet. The good news is that now it
seems like everyone has written some kind of social reader, so it should
be a familiar area for many, so great for sample code. And who knows?
Maybe this time we’ll get it right.

The social reader application I have in mind is something between the
late, great Google Reader and a sharing site like Digg or Reddit. Like
Google Reader, users will be able to read the text of a story, and the
application will keep track of what they’ve seen. Like Reddit they’ll be
able to vote stories up or down, and the votes will affect the order in
which other users will see the stories.

The data is pretty basic.

There are members, stories, and ratings. A member has a URL and a score.

A story has an ID and a text. Where it gets tricky is that the same
story may have multiple URLs. (usually just "http" and "https" versions
of the same URL, or the same URL with and without "www" or
"index.html".) But a story has exactly one preferred URL.

Ratings positive for a user who liked a story, negative for a user who
disliked a story, and 0 to show that a user saw the story and shouldn’t
be shown it again, but didn't rate it up or down.

We can think of ratings as coming from a “subject” who can be a user, an
outside recommender such as an RSS feed or social site, or an internal
software component such as the home page builder. Any subject can have
an up or down vote on any “object”, usually a story.

Queries for Social Reading
--------------------------

They always tell you to consider the queries when designing a CQL data
model, so what kind of queries does this application need? Because it’s
a simple application, there are only a few main ones.

-  Get recent stories.
-  Highest-scoring stories rated by a given user, since a given date.
   This will let us build a page of recent recommended by user for each
   user who wants one.
-  Highest-scoring stories that have *not* been rated by a given user.
   This is for showing a user "new stories you haven't read yet", and
   also to build the home page for logged-out users. The home page can
   be represented as just another user, who gives stories a 0 rating
   after they have appeared for a certain time.

For updates, I mainly need to be able to write new ratings and stories.
So here’s a first version of the data model.

::

    CREATE TABLE rating_by_subject (
        subject VARCHAR,
        object VARCHAR,
        score INT,
        date TIMESTAMP,
        PRIMARY KEY (subject, date)
    );

    CREATE TABLE rating_by_object (
        subject VARCHAR,
        object VARCHAR,
        score INT,
        date TIMESTAMP,
            PRIMARY KEY (object)
        );

The three versions help us quickly look up whether a given rating
exists, and to get all ratings for a given subject and object. Usually
the subject is a user and the object is a story, but it’s possible for
ratings to exist between other entities in the system. For example,
users might be able to rate each other, or an RSS feed could rate all
the stories and links that it publishes. Stories are fairly easy, mainly
just content, several kb of HTML, with a primary key of the story URL.
Most of the attributes of the story can be in the HTML, with just a
“type” to keep track of whether this URL represents a duplicate of a
story at a different preferred URL.

::

    CREATE TABLE story (
       url VARCHAR,
       date VARCHAR,
       type VARCHAR,
       content VARCHAR,
       PRIMARY KEY(url, date)
    );

The date is used as a clustering key.

The last table covers members. Members can be users, RSS feeds, or any
other source of recommendations. To avoid cluttering up this example
with extra columns, and avoid cluttering up the user’s routine with
passwords, we’ll use a third party login service such as OAuth or
Mozilla Persona. The users can log in with an existing web or email
account, and we don’t have to write password recovery.

::

    CREATE TABLE member (
       url VARCHAR,
       score INT,
       active TIMESTAMP,
       success TIMESTAMP,
       PRIMARY KEY(url)
    );

The main problem for developing this application now is that some of the
queries look hard to do in Apache Cassandra space. Something that would be easy
in SQL, our query that needs to filter out any story already seen by a
given user, is prohibitive in CQL.

But you can’t really make Cassandra work like an RDBMS. The solution is
to have Cassandra do what it does best and put the rest of the work on
the client.

Instead of having the database do the filtering, and saving bandwidth by
just sending a list of recent unseen stories, change it around. For a
social reader application, the economics matter. Post-query processing,
the kind that would get you an F on an RDBMS-backed project for school,
is not just doable for a social reader. It’s free. Because you can do it
on the client, whose battery the user is paying to charge, instead of in
the data center where the bill comes to you.

So let’s reconsider the query for unrated stories. Instead of doing the
whole query in one step, we’ll just send the URLs of new stories to the
client, then have the client request a list of seen by that user since
the earliest timestamp on a new story. The client will filter out the
already-seen stories.

We’ll keep one "don't send me anything older than this" timestamp on
each client device to keep different devices for each user synced up.

The first query would be:

::

        SELECT url FROM story WHERE date > ? LIMIT ?

Next, we use the timestamp of the earliest story returned in the first
query to get the list of URLs to filter out.

::

        SELECT object FROM rating_by_subject
              WHERE subject = ?
              AND date > ?
              LIMIT ?

This would have been unworkable in MSIE 6 days, but today’s browsers
have LocalStorage to let us do infrequent updates of the story list. We
can tweak the number of stories returned, to balance out the amount of
network traffic.

Finally, for building feeds and home pages, the main criterion in the
query is the freshness of the story. So we can use the
``rating_by_date`` table.

::

        SELECT object FROM rating_by_date
              WHERE date > ?
              LIMIT ?

NoSQL works in part because the modern client tier is awesome -- between
graphics, processing power, and localStorage, all that you need to
execute on the server is code to implement security or data consistency.
Maybe using Scylla we will never make the one true social reader
application, but the design makes it worth trying

`Knowledge Base 
</kb/>`_

Copyright
^^^^^^^^^

.. include:: /rst_include/apache-copyrights-index.rst

.. include:: /rst_include/apache-copyrights-index-all-attributes.rst
