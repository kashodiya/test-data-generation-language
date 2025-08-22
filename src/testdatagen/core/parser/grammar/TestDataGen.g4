

grammar TestDataGen;

// No import needed, we'll generate lexer separately

// Root rule
program
    : importDeclaration* schemaDeclaration EOF
    ;

importDeclaration
    : IMPORT STRING_LITERAL (AS ID)? SEMI
    ;

schemaDeclaration
    : SCHEMA ID LBRACE tableDeclaration* RBRACE
    ;

tableDeclaration
    : TABLE ID LBRACE fieldDeclaration* tableConstraint* generationDirective? RBRACE
    ;

fieldDeclaration
    : FIELD ID COLON dataType fieldModifier* fieldConstraint* SEMI
    ;

dataType
    : primitiveType
    | complexType
    | ID // Custom type reference
    ;

primitiveType
    : INTEGER
    | DECIMAL
    | STRING
    | BOOLEAN
    | DATE
    | TIMESTAMP
    | BINARY
    | UUID
    | JSON
    ;

complexType
    : primitiveType LBRACK INT_LITERAL? RBRACK // Array type
    ;

fieldModifier
    : NULL
    | NOT_NULL
    | DEFAULT defaultValue
    ;

defaultValue
    : literal
    | functionCall
    ;

fieldConstraint
    : WITH constraintExpression
    ;

tableConstraint
    : CONSTRAINT ID? constraintExpression SEMI
    ;

constraintExpression
    : primaryKeyConstraint
    | foreignKeyConstraint
    | uniqueConstraint
    | checkConstraint
    ;

primaryKeyConstraint
    : PRIMARY KEY LPAREN idList RPAREN
    ;

foreignKeyConstraint
    : FOREIGN KEY LPAREN idList RPAREN REFERENCES ID LPAREN idList RPAREN
    ;

uniqueConstraint
    : UNIQUE LPAREN idList RPAREN
    ;

checkConstraint
    : CHECK LPAREN expression RPAREN
    ;

generationDirective
    : GENERATE generationOptions SEMI
    ;

generationOptions
    : generationOption (COMMA generationOption)*
    ;

generationOption
    : ID ASSIGN generationValue
    ;

generationValue
    : literal
    | functionCall
    | LBRACE generationOptions RBRACE
    ;

functionCall
    : ID LPAREN functionArgs? RPAREN
    ;

functionArgs
    : functionArg (COMMA functionArg)*
    ;

functionArg
    : expression
    ;

expression
    : literal                                       # LiteralExpr
    | ID                                           # IdentifierExpr
    | functionCall                                 # FunctionCallExpr
    | LPAREN expression RPAREN                     # ParenExpr
    | expression DOT ID                            # MemberExpr
    | expression LBRACK expression RBRACK          # IndexExpr
    | expression op=(MUL|DIV|MOD) expression       # BinaryExpr
    | expression op=(ADD|SUB) expression           # BinaryExpr
    | expression op=(LT|GT|LE|GE) expression       # BinaryExpr
    | expression op=(EQUAL|NOTEQUAL) expression    # BinaryExpr
    | expression AND expression                    # LogicalExpr
    | expression OR expression                     # LogicalExpr
    | NOT expression                               # NotExpr
    | expression IN LPAREN expressionList RPAREN   # InExpr
    | expression BETWEEN expression AND expression # BetweenExpr
    | expression LIKE STRING_LITERAL               # LikeExpr
    ;

expressionList
    : expression (COMMA expression)*
    ;

idList
    : ID (COMMA ID)*
    ;

literal
    : INT_LITERAL
    | DECIMAL_LITERAL
    | STRING_LITERAL
    | TRUE
    | FALSE
    | NULL
    | arrayLiteral
    | objectLiteral
    ;

arrayLiteral
    : LBRACK (literal (COMMA literal)*)? RBRACK
    ;

objectLiteral
    : LBRACE (objectField (COMMA objectField)*)? RBRACE
    ;

objectField
    : ID COLON literal
    ;

