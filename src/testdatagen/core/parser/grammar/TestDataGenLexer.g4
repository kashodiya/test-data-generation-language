
lexer grammar TestDataGenLexer;

// Keywords
SCHEMA:     'schema';
TABLE:      'table';
FIELD:      'field';
TYPE:       'type';
CONSTRAINT: 'constraint';
IMPORT:     'import';
AS:         'as';
FROM:       'from';
WITH:       'with';
NULL:       'null';
NOT_NULL:   'not null';
DEFAULT:    'default';
PRIMARY:    'primary';
KEY:        'key';
FOREIGN:    'foreign';
REFERENCES: 'references';
UNIQUE:     'unique';
CHECK:      'check';
GENERATE:   'generate';
USING:      'using';
WHERE:      'where';
AND:        'and';
OR:         'or';
IN:         'in';
BETWEEN:    'between';
LIKE:       'like';

// Primitive types
INTEGER:    'integer';
DECIMAL:    'decimal';
STRING:     'string';
BOOLEAN:    'boolean';
DATE:       'date';
TIMESTAMP:  'timestamp';
BINARY:     'binary';
UUID:       'uuid';
JSON:       'json';

// Literals
TRUE:       'true';
FALSE:      'false';

// Symbols
LPAREN:     '(';
RPAREN:     ')';
LBRACE:     '{';
RBRACE:     '}';
LBRACK:     '[';
RBRACK:     ']';
SEMI:       ';';
COLON:      ':';
COMMA:      ',';
DOT:        '.';
ASSIGN:     '=';
GT:         '>';
LT:         '<';
BANG:       '!';
QUESTION:   '?';
EQUAL:      '==';
LE:         '<=';
GE:         '>=';
NOTEQUAL:   '!=';
ADD:        '+';
SUB:        '-';
MUL:        '*';
DIV:        '/';
MOD:        '%';
CARET:      '^';
TILDE:      '~';

// Identifiers and literals
ID:         [a-zA-Z_][a-zA-Z0-9_]*;
INT_LITERAL: [0-9]+;
DECIMAL_LITERAL: [0-9]+ '.' [0-9]+;
STRING_LITERAL: '"' (~["\r\n\\] | '\\' .)* '"' | '\'' (~['\r\n\\] | '\\' .)* '\'';

// Whitespace and comments
WS:         [ \t\r\n\u000C]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
