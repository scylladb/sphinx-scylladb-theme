# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
CQL pygments lexer
~~~~~~~~~~~~~~~~~~
Lexer for the Cassandra Query Language (CQL).
This is heavily inspired from the pygments SQL lexer (and the Postgres one in particular) but adapted to CQL
keywords and specificities.
"""

import re

from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, words
from pygments.lexers import ClassNotFound, get_lexer_by_name
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Whitespace,
)

__all__ = ["CQLLexer"]

language_re = re.compile(r"\s+LANGUAGE\s+'?(\w+)'?", re.IGNORECASE)

KEYWORDS = (
    "SELECT",
    "FROM",
    "AS",
    "WHERE",
    "AND",
    "KEY",
    "KEYS",
    "ENTRIES",
    "FULL",
    "INSERT",
    "UPDATE",
    "WITH",
    "LIMIT",
    "PER",
    "PARTITION",
    "USING",
    "USE",
    "DISTINCT",
    "COUNT",
    "SET",
    "BEGIN",
    "UNLOGGED",
    "BATCH",
    "APPLY",
    "TRUNCATE",
    "DELETE",
    "IN",
    "CREATE",
    "KEYSPACE",
    "SCHEMA",
    "KEYSPACES",
    "COLUMNFAMILY",
    "TABLE",
    "MATERIALIZED",
    "VIEW",
    "INDEX",
    "CUSTOM",
    "ON",
    "TO",
    "DROP",
    "PRIMARY",
    "INTO",
    "VALUES",
    "TIMESTAMP",
    "TTL",
    "CAST",
    "ALTER",
    "RENAME",
    "ADD",
    "TYPE",
    "COMPACT",
    "STORAGE",
    "ORDER",
    "BY",
    "ASC",
    "DESC",
    "ALLOW",
    "FILTERING",
    "IF",
    "IS",
    "CONTAINS",
    "GRANT",
    "ALL",
    "PERMISSION",
    "PERMISSIONS",
    "OF",
    "REVOKE",
    "MODIFY",
    "AUTHORIZE",
    "DESCRIBE",
    "EXECUTE",
    "NORECURSIVE",
    "MBEAN",
    "MBEANS",
    "USER",
    "USERS",
    "ROLE",
    "ROLES",
    "SUPERUSER",
    "NOSUPERUSER",
    "PASSWORD",
    "LOGIN",
    "NOLOGIN",
    "OPTIONS",
    "CLUSTERING",
    "TOKEN",
    "WRITETIME",
    "NULL",
    "NOT",
    "EXISTS",
    "MAP",
    "LIST",
    "NAN",
    "INFINITY",
    "TUPLE",
    "TRIGGER",
    "STATIC",
    "FROZEN",
    "FUNCTION",
    "FUNCTIONS",
    "AGGREGATE",
    "SFUNC",
    "STYPE",
    "FINALFUNC",
    "INITCOND",
    "RETURNS",
    "CALLED",
    "INPUT",
    "LANGUAGE",
    "OR",
    "REPLACE",
    "JSON",
    "LIKE",
)

DATATYPES = (
    "ASCII",
    "BIGINT",
    "BLOB",
    "BOOLEAN",
    "COUNTER",
    "DATE",
    "DECIMAL",
    "DOUBLE",
    "EMPTY",
    "FLOAT",
    "INET",
    "INT",
    "SMALLINT",
    "TEXT",
    "TIME",
    "TIMESTAMP",
    "TIMEUUID",
    "TINYINT",
    "UUID",
    "VARCHAR",
    "VARINT",
)


def language_callback(lexer, match):
    """
    Parse the content of a $-string using a lexer
    The lexer is chosen looking for a nearby LANGUAGE or assumed as
    java if no LANGUAGE has been found.
    """
    l = None
    m = language_re.match(lexer.text[max(0, match.start() - 100) : match.start()])
    if m is not None:
        l = lexer._get_lexer(m.group(1))
    else:
        l = lexer._get_lexer("java")

    # 1 = $, 2 = delimiter, 3 = $
    yield (match.start(1), String, match.group(1))
    yield (match.start(2), String.Delimiter, match.group(2))
    yield (match.start(3), String, match.group(3))
    # 4 = string contents
    if l:
        for x in l.get_tokens_unprocessed(match.group(4)):
            yield x
    else:
        yield (match.start(4), String, match.group(4))
    # 5 = $, 6 = delimiter, 7 = $
    yield (match.start(5), String, match.group(5))
    yield (match.start(6), String.Delimiter, match.group(6))
    yield (match.start(7), String, match.group(7))


class CQLLexer(RegexLexer):
    """
    Lexer for the Cassandra Query Language.
    """

    name = "Cassandra Query Language"
    aliases = ["cql"]
    filenames = ["*.cql"]
    mimetypes = ["text/x-cql"]

    flags = re.IGNORECASE
    tokens = {
        "root": [
            (r"\s+", Text),
            (r"--.*\n?", Comment.Single),
            (r"//.*\n?", Comment.Single),
            (r"/\*", Comment.Multiline, "multiline-comments"),
            (
                r"(" + "|".join(s.replace(" ", r"\s+") for s in DATATYPES) + r")\b",
                Name.Builtin,
            ),
            (words(KEYWORDS, suffix=r"\b"), Keyword),
            (r"[+*/<>=~!@#%^&|`?-]+", Operator),
            (r"\$\d+", Name.Variable),
            # Using Number instead of the more accurate Literal because the latter don't seem to e highlighted in most
            # styles
            (
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                Number,
            ),  # UUIDs
            (r"0x[0-9a-fA-F]+", Number),  # Blobs
            (r"([0-9]*\.[0-9]*|[0-9]+)(e[+-]?[0-9]+)?", Number.Float),
            (r"[0-9]+", Number.Integer),
            (r"((?:E|U&)?)(')", bygroups(String.Affix, String.Single), "string"),
            # quoted identifier
            (r'((?:U&)?)(")', bygroups(String.Affix, String.Name), "quoted-ident"),
            (r"(?s)(\$)([^$]*)(\$)(.*?)(\$)(\2)(\$)", language_callback),
            (r"[a-z_]\w*", Name),
            (r"[;:()\[\]{},.]", Punctuation),
        ],
        "multiline-comments": [
            (r"/\*", Comment.Multiline, "multiline-comments"),
            (r"\*/", Comment.Multiline, "#pop"),
            (r"[^/*]+", Comment.Multiline),
            (r"[/*]", Comment.Multiline),
        ],
        "string": [
            (r"[^']+", String.Single),
            (r"''", String.Single),
            (r"'", String.Single, "#pop"),
        ],
        "quoted-ident": [
            (r'[^"]+', String.Name),
            (r'""', String.Name),
            (r'"', String.Name, "#pop"),
        ],
    }

    def get_tokens_unprocessed(self, text, *args):
        # Have a copy of the entire text to be used by `language_callback`.
        self.text = text
        for x in RegexLexer.get_tokens_unprocessed(self, text, *args):
            yield x

    def _get_lexer(self, lang):
        return get_lexer_by_name(lang, **self.options)
