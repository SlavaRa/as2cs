"""
Converts a trivial example of an empty class.
Usage: 
    cd as2cs
    python as2cs.py [file.as ...]
"""


import codecs
from os import path
from pprint import pformat
from pretty_print_code.pretty_print_code import format_text
from simpleparse.parser import Parser
from simpleparse.simpleparsegrammar import declaration
from simpleparse.common import strings, comments, numbers, chartypes, SOURCES


cfg = {
    'source': 'as',
    'to': 'cs',
    'is_formats': ['compilationUnit'],
}


ebnf_parser = Parser(declaration, 'declarationset')


source_keys = [key for source in SOURCES 
    for key in source.keys()]
source_keys.sort()
## print pformat(source_keys)


def merge_declarations(declarations):
    r"""
    B augments A.
    Normalize whitespace before and after assignment.
    Expects definition fits on one line.
    >>> a = "whitespace     := [ \t\r\n]+"
    >>> b = "import := 'import'"
    >>> merge_declarations([a, b])
    "whitespace     := [ \t\r\n]+\nimport := 'import'"

    B overwrites A.
    >>> a = "import  \t := 'import'"
    >>> b = "import := \t 'using'"
    >>> merge_declarations([a, b])
    "import := \t 'using'"
    """
    names = {}
    def new_declarations(parser, input):
        text = ''
        taglist = parser.parse(input)
        for tag, begin, end, parts in taglist[1]:
            if tag == 'declaration':
                name_begin, name_end = parts[0][1:3]
                name = input[name_begin:name_end]
                if not name in names:
                    names[name] = True
                    text += input[begin:end]
        ## text += pformat(taglist)
        return text
    texts = []
    for input in reversed(declarations):
        text = new_declarations(ebnf_parser, input)
        if text:
            texts.insert(0, text)
    return '\n'.join(texts)


def merge_declaration_paths(paths):
    texts = []
    for path in paths:
        texts.append(open(path).read())
    return merge_declarations(texts)


def set_tags(tags, grammar_text, value):
    r"""
    >>> grammar_text = "a := b\nb := '.'"
    >>> tags = {}
    >>> set_tags(tags, grammar_text, True)
    >>> print pformat(tags)
    {'a': True, 'b': True}
    >>> set_tags(tags, 'spacechar := " "', False)
    >>> print pformat(tags)
    {'a': True, 'b': True, 'spacechar': False}
    """
    taglist = ebnf_parser.parse(grammar_text)
    for tag, begin, end, parts in taglist[1]:
        if tag == 'declaration':
            name_begin, name_end = parts[0][1:3]
            name = grammar_text[name_begin:name_end]
            tags[name] = value


def find_text(text, names, parts):
    """
    >>> parts = [('name', 0, 6, []), ('seq_group', 9, 18, [('element_token', 10, 18, [('literal', 10, 17, [('CHARNOSNGLQUOTE', 11, 16, None)])])])]
    >>> find_text("import := 'using'", ['digit'], parts)
    >>> find_text("import := 'using'", ['literal'], parts)
    "'using'"
    >>> find_text('import := "using"', ['CHARNODBLQUOTE', 'CHARNOSNGLQUOTE'], parts)
    'using'
    """
    found = ''
    if parts:
        for tag, begin, end, part in parts:
            if tag in names:
                found += text[begin:end]
                break
            else:
                found_part = find_text(text, names, part)
                if found_part:
                    found += found_part
    if found:
        return found


def find_texts(text, name, parts, not_followed_by = None):
    """
    >>> parts = [('variableDeclarationKeyword', 0, 3, None),
    ...  ('whitespacechar', 3, 4, None),
    ...  ('identifier',
    ...   4,
    ...   8,
    ...   [('alphaunder', 4, 5, [('letter', 4, 5, None)]),
    ...    ('alphanums',
    ...     5,
    ...     8,
    ...     [('letter', 5, 6, None),
    ...      ('letter', 6, 7, None),
    ...      ('letter', 7, 8, None)])]),
    ...  ('COLON', 8, 9, None),
    ...  ('dataType', 9, 15, [('string', 9, 15, None)]),
    ...  ('SEMI', 15, 16, None)]
    >>> as_code = 'var path:String;';
    >>> find_texts(as_code, 'digit', parts)
    []
    >>> find_texts(as_code, 'letter', parts)
    ['p', 'a', 't', 'h']
    >>> find_texts(as_code, 'letter', parts, ':')
    ['p', 'a', 't']
    >>> find_texts(as_code, 'letter', parts, 't')
    ['p', 't', 'h']
    """
    found = []
    if parts:
        for tag, begin, end, part in parts:
            if name == tag:
                is_match = True
                if not_followed_by is not None:
                    following = text[end:]
                    for not_followed in not_followed_by:
                        if following.startswith(not_followed):
                            is_match = False
                            break
                if is_match:
                    found.append(text[begin:end])
            else:
                found_part = find_texts(text, name, part, not_followed_by)
                if found_part:
                    found.extend(found_part)
    return found


def find_literal_text(text, parts):
    return find_text(text, ['CHARNOSNGLQUOTE', 'CHARNODBLQUOTE'], parts)


def find_literals(grammar_text):
    literals = {}
    taglist = ebnf_parser.parse(grammar_text)[1]
    for tag, begin, end, parts in taglist:
        if tag == 'declaration':
            name_begin, name_end = parts[0][1:3]
            name = grammar_text[name_begin:name_end]
            literal = find_literal_text(grammar_text, parts)
            if literal:
                literals[name] = literal
    return literals


def replace_literals(a_grammar, b_grammar, literals = None):
    """
    >>> replaces = replace_literals(as_grammar, cs_grammar, literals['cs'])
    >>> replaces.get('import')
    'using'
    >>> replaces.get('alphaunder')
    >>> replaces = replace_literals(as_grammar, cs_grammar)
    >>> replaces.get('import')
    'using'
    >>> replaces.get('alphaunder')
    >>> replaces.get('STRING')
    'string'
    """
    if literals is None:
        literals = find_literals(b_grammar)
    def replace_declaration(replaces, original_strings, grammar_text):
        taglist = ebnf_parser.parse(grammar_text)[1]
        for tag, begin, end, parts in taglist:
            if tag == 'declaration':
                name_begin, name_end = parts[0][1:3]
                name = grammar_text[name_begin:name_end]
                text = grammar_text[begin:end]
                if name in original_strings and text != original_strings[name]:
                    literal = literals.get(name)
                    if literal:
                        replaces[name] = literal
                original_strings[name] = text
    replaces = {}
    original_strings = {}
    replace_declaration(replaces, original_strings, a_grammar)
    replace_declaration(replaces, original_strings, b_grammar)
    return replaces


def tag_order(grammar_text):
    """
    >>> cs_var = 'variableDeclaration := whitespace?, dataType, whitespacechar+, identifier, whitespace*, SEMI'
    >>> tag_order(cs_var)
    ['dataType', 'whitespacechar', 'identifier', 'SEMI']
    >>> as_var = 'variableDeclaration := whitespace?, variableDeclarationKeyword, whitespacechar+, identifier, (COLON, dataType)?, whitespace*, SEMI'
    >>> tag_order(as_var)
    ['variableDeclarationKeyword', 'whitespacechar', 'identifier', 'COLON', 'dataType', 'SEMI']
    """
    taglist = ebnf_parser.parse(grammar_text)[1]
    optional_occurences = ['*', '?']
    order = find_texts(grammar_text, 'name', taglist, optional_occurences)[1:]
    return order


def tags_to_reorder(a_grammar, b_grammar):
    """
    For grammar tags of the same name.
    Order of tags in definition B where they differ from order in A
    >>> cs_var = 'variableDeclaration := whitespace?, dataType, whitespacechar+, identifier, whitespace*, SEMI'
    >>> as_var = 'variableDeclaration := whitespace?, variableDeclarationKeyword, whitespacechar+, identifier, (COLON, dataType)?, whitespace*, SEMI'
    >>> reorder_tags = tags_to_reorder(as_var, cs_var)
    >>> reorder_tags.get('variableDeclaration')
    ['dataType', 'whitespacechar', 'identifier', 'SEMI']
    >>> reorder_tags = tags_to_reorder(cs_var, as_var)
    >>> reorder_tags.get('variableDeclaration')
    ['variableDeclarationKeyword', 'whitespacechar', 'identifier', 'COLON', 'dataType', 'SEMI']
    >>> tags_to_reorder('namespace := "package"', 'namespace := "namespace"')
    {}
    """
    def reorder_declaration(reorders, original_strings, grammar_text):
        taglist = ebnf_parser.parse(grammar_text)
        ## print pformat(taglist)
        for tag, begin, end, parts in taglist[1]:
            if tag == 'declaration':
                name_begin, name_end = parts[0][1:3]
                name = grammar_text[name_begin:name_end]
                text = grammar_text[begin:end]
                if name in original_strings and text != original_strings[name]:
                    order_tags = tag_order(text)
                    if order_tags:
                        reorders[name] = order_tags
                original_strings[name] = text
    reorders = {}
    original_strings = {}
    reorder_declaration(reorders, original_strings, a_grammar)
    reorder_declaration(reorders, original_strings, b_grammar)
    return reorders


def insert(source_str, insert_str, pos):
    """
    answered Sep 22 '14 at 15:45 Sim Mak
    http://stackoverflow.com/questions/4022827/how-to-insert-some-string-in-the-given-string-at-given-index-in-python
    """
    return source_str[:pos] + insert_str + source_str[pos:]


def reorder_taglist(taglist, tag, input, source, to):
    """
    Inserts tags of target grammar not found in the source grammar.
    Example:  see test_syntax.py
    Does not handle multiple occurences.
    Instead group those together in the grammar, such as 'digits' instead of ('digit', 'digit')
    >>> input = 'b22'
    >>> order = ['digits', 'letter']
    >>> taglist = [('letter', 0, 1, None), ('digits', 1, 3, None)]
    >>> reorder_taglist(taglist, order, input, 'as', 'cs')
    '22b'
    >>> order = ['digit', 'letter']
    >>> taglist = [('letter', 0, 1, None), ('digit', 1, 2, None), ('digit', 2, 3, None)]
    >>> reorder_taglist(taglist, order, input, 'as', 'cs')
    '2b'
    """
    def add(unordered, r, length):
        row = unordered[r]
        t, b, e, parts = row
        b += length
        e += length
        unordered[r] = (t, b, e, parts)
        if parts:
            for p, part in enumerate(parts):
                add(parts, p, length)
    ordered = []
    unordered = taglist[:]
    used_indexes = {}
    reorders = reorder_tags[source][to]
    if isinstance(tag, basestring):
        order_tags = reorders[tag]
    else:
        order_tags = tag
    end = 0
    row_index = 0
    for order_tag in order_tags:
        for r, row in enumerate(unordered):
            unordered_tag = row[0]
            if order_tag == unordered_tag and not r in used_indexes:
                ordered.append(unordered[r])
                used_indexes[r] = True
                end = row[2]
                row_index = r
                break
        else:
            for verbatim in literals, reorder_defaults:
                if order_tag in verbatim[to]:
                    insert_text = verbatim[to][order_tag]
                    length = len(insert_text)
                    ordered.append((order_tag, end, end + length, None))
                    input = insert(input, insert_text, end)
                    for r in range(row_index, len(unordered)):
                        if not r in used_indexes:
                            add(unordered, r, length)
                    end += length
                    break
    text = _recurse_tags(ordered, input, source, to)
    return text


def _last(latest, parts, is_pre):
    for t, b, e, sub in parts:
        if sub:
            latest = _last(latest, sub, is_pre)
        elif is_pre:
            latest = max(latest, b)
        else:
            latest = min(latest, e)
    return latest


def affix(begin, end, parts, input, is_pre):
    if is_pre:
        at = begin
    else:
        at = end
    text = ''
    latest = _last(at, parts, is_pre)
    if begin < latest and latest < end:
        if is_pre:
            text = input[:latest]
        else:
            text = input[latest:]
    return text


def _recurse_tags(taglist, input, source, to):
    """
    Reorder tags.
    Transcribe common tags and literal tags.
    Visit sub-parts.
    """
    reorders = reorder_tags[source][to]
    replaces = replace_tags[source][to]
    text = ''
    for tag, begin, end, parts in taglist:
        if tag in replaces:
            text += replaces.get(tag)
        elif tag in literals[to]:
            text += input[begin:end]
        elif tag in reorders:
            text += reorder_taglist(parts, tag, input, source, to)
        elif tag in source_keys:
            text += input[begin:end]
        elif parts:
            text += _recurse_tags(parts, input, source, to)
        else:
            text += input[begin:end]
    return text


def newline_after_braces(text):
    return text.replace('{', '{\n').replace('}', '}\n').replace('\n\n', '\n')


def format(text):
    text = newline_after_braces(text)
    text = format_text(text)
    return text


def may_format(definition, text):
    if definition in cfg['is_formats']:
        text = format(text)
    return text


def convert(input, definition = 'compilationUnit'):
    """
    Example of converting syntax from ActionScript to C#.

    >>> print convert('import com.finegamedesign.anagram.Model;', 'importDefinition')
    using com.finegamedesign.anagram.Model;

    Related to grammar unit testing specification (gUnit)
    https://theantlrguy.atlassian.net/wiki/display/ANTLR3/gUnit+-+Grammar+Unit+Testing
    """
    source = cfg['source']
    to = cfg['to']
    parser = Parser(grammars[source], definition)
    taglist = parser.parse(input)
    taglist = [(definition, 0, taglist[-1], taglist[1])]
    text = _recurse_tags(taglist, input, source, to)
    text = may_format(definition, text)
    return text


def format_taglist(input, definition):
    source = cfg['source']
    parser = Parser(grammars[source], definition)
    taglist = parser.parse(input)
    return pformat(taglist)


def convert_file(source_path, to_path):
    text = codecs.open(source_path, 'r', 'utf-8').read()
    str = convert(text)
    f = codecs.open(to_path, 'w', 'utf-8')
    f.write(str)
    f.close()


def analogous_paths(source_paths):
    path_pairs = []
    for source_path in source_paths:
        root, ext = path.splitext(source_path)
        to_path = '%s.%s' % (root, cfg['to'])
        path_pairs.append([source_path, to_path])
    return path_pairs


def convert_files(source_paths):
    for source_path, to_path in analogous_paths(source_paths):
        convert_file(source_path, to_path)


def compare_file(source_path, to_path):
    text = codecs.open(source_path, 'r', 'utf-8').read()
    got = convert(text)
    expected = codecs.open(to_path, 'r', 'utf-8').read()
    return [expected, got]


def compare_files(source_paths):
    expected_gots = []
    for source_path, to_path in analogous_paths(source_paths):
        expected_gots.append(compare_file(source_path, to_path))
    return expected_gots


def realpath(a_path):
    """
    http://stackoverflow.com/questions/4934806/python-how-to-find-scripts-directory
    """
    return path.join(path.dirname(path.realpath(__file__)), a_path)


# Cache global variables for speed
as_grammar = merge_declaration_paths(['as_and_cs.g', 'as.g'])
cs_grammar = merge_declaration_paths(['as_and_cs.g', 'cs.g'])
grammars = {'as': as_grammar, 'cs': cs_grammar}
literals = {'as': {}, 'cs': {}}
literals['as'] = find_literals(as_grammar)
literals['cs'] = find_literals(cs_grammar)
replace_tags = {'as': {}, 'cs': {}}
replace_tags['as']['cs'] = replace_literals(as_grammar, cs_grammar, literals['cs'])
replace_tags['cs']['as'] = replace_literals(cs_grammar, as_grammar, literals['as'])

reorder_defaults = {'as': {}, 'cs': {}}
reorder_defaults['cs']['ts'] = literals['cs']['SPACE']
reorder_defaults['as']['ts'] = literals['as']['SPACE']
reorder_tags = {'as': {}, 'cs': {}}
reorder_tags['as']['cs'] = tags_to_reorder(as_grammar, cs_grammar)
reorder_tags['cs']['as'] = tags_to_reorder(cs_grammar, as_grammar)

different_tags = {}
set_tags(different_tags, open('as.g').read(), True)
set_tags(different_tags, open('cs.g').read(), True)
for key in source_keys:
    different_tags[key] = False
set_tags(different_tags, open('as_and_cs.g').read(), False)

if '__main__' == __name__:
    import sys
    if len(sys.argv) <= 1:
        print __doc__
    if 2 <= len(sys.argv) and '--test' != sys.argv[1]:
        convert_files(sys.argv[1:])
    import doctest
    doctest.testmod()
