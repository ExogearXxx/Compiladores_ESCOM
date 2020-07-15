  /* Reverse polish notation calculator.  */

     %{
       #include <stdio.h>
       #include <math.h>
       int yylex (void);
       void yyerror (char const *);
     %}

     %define api.value.type {double}
     %token NUM

%% /* Grammar rules and actions follow.  */

input:
  %empty
| input line
;

line:
  '\n'
| exp '\n'      { printf ("%.10g\n", $1); }
;

exp:
  NUM           { $$ = $1;           }
| exp exp '+'   { $$ = $1 + $2;      }
| exp exp '-'   { $$ = $1 - $2;      }
| exp exp '*'   { $$ = $1 * $2;      }
| exp exp '/'   { $$ = $1 / $2;      }
| exp exp '^'   { $$ = pow ($1, $2); }  /* Exponentiation */
| exp 'n'       { $$ = -$1;          }  /* Unary minus    */
;
%%

#include <ctype.h>

     int
     yylex (void)
     {
       int c;

       /* Skip white space.  */
       while ((c = getchar ()) == ' ' || c == '\t')
         continue;
       /* Process numbers.  */
       if (c == '.' || isdigit (c))
         {
           ungetc (c, stdin);
           scanf ("%lf", &yylval);
           return NUM;
           }
       /* Return end-of-input.  */
       if (c == EOF)
         return 0;
       /* Return a single char.  */
       return c;
     }
void main()
{
  yyparse();
}

void
yyerror(char const *s)
{
  fprintf(stderr,"Creo que encontre un error :[ %s\n",s);
}




