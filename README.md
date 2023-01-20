# compilers

En el presente proyecto se implementó un conjunto de herramientas para la creación de gramáticas, reconocimiento de expresiones regulares, generador de parsers (LL(1), SLR(1) y LR(1)) y generador de Lexer, todo con fines didácticos.

**NOTA**: Los archivos `pycompiler.py` y `visitor.py` fueron las únicas herramientas extras que se utilizaron para hacer la librería. Una contiene definición de tipos como `Grammar`, `Token`, `Item` y `State` necesarios para la implementación general, las cuales fueron proporcionadas por los profesores de Compilación de la facultad de Matemática y Computación de la Universidad de la Habana, nuevamente con fines didácticos. El otro es un patron de diseño implementado por .

## Expreseiones regulares

Para el diseño de expresiones regulares se creó una gramatica LL(1) de la siguiente manera:

```
E   -> TX
X   -> |E
    -> epsilon
T   -> FY
Y   -> T
    -> epsilon
F   -> AZ
Z   -> *
    -> +
    -> epsilon
A   -> t
    -> (E)
    -> ε
```

Donde solo se reconocen expresiones regulares con operaciones de `Union`, `Concatenacion`, `Clausura` y `Clausura Positiva`. Para el reconocimiento de estas luego de la tokenización respectiva y el parseo, se construye un autómata Finito No Determinista que reconozca cualquier expresión regular con dicha forma. Este automata se convierte a un automata Finito Determinista, el cual será quien finalmente reconozca la expresión

Es necesario tener en cuenta que las operaciones permitidas antes mencionadas se hacen a nivel de autómata, es decir, se `unen` los autómatas, se `concatenan`, etc. A continuación se muestran ejemplos de cómo se construye el autómata de cada operación

#### Union
![Union](/img/union.svg)

#### Concatenación
![Concatenación](/img/concatenacion.svg)

#### Clausura
![Clausura](/img/clausura.svg)

#### Clausura Positiva
![Clausura](/img/clausurapositiva.svg)

## Generador de Lexer

Para hacer un generador de lexer necesitamos un reconocedor de gramaticas regulares, por ello utilizamos la implementación anterior. Un Lexer se encargará de reconocer el lexema de una cadena, extrayendo secciones de esta y tokenizándolas.

La forma usual de hacer esto es crear un autómata unión de los autómatas de cada una de las expresiones regulares que deben ser reconocidas por el Lexer. Este autómata reconocerían cada token que pueda ser creado, sin embargo tiene una peculariedad. La cadena se va reconociendo desde el principio hasta que el autómata se `trabe`. Y luego y que decide qué token generar, ya que a medidad que se va reconociendo una de las expresiones finales, se guarda cuál fue la última (o últimas), subcadena reconocida, y de estas se decide una para tokenizarla: la que mayor prioridad tenga. De esta manera un generador de Lexer debe recibir en orden de prioridad las expresiones regulares que son capaces de reconocer y funcionar de esta forma.

En el archivo `lexer.py` está la implementación de nuestro generador de `Lexer`.

## Parsers

El proceso luego de tokenizar una cadena, es el de parsearla para verificar su estructura sintáctica. Para ello se pueden usar distintos tipos de parser. Actualmente implementamos 3.

### Parser LL(1)

Este parser es una estrategia top-down, en la que se va construyendo la cadena de izquierda a derecha viendo que producciones de la gramática son posibles de aplicar. Suele usarse en gramáticas muy simples ya que un impedimento que tiene es ta gramática es que no puede tener recurisividad izquiera, ni factores comunes, por lo que lograr una gramática de este estilo puede ser algo muy engorroso, difícil y sobre todo, poco legible.

En la práctica se deben calcular los First y Follows de cada forma oracional y no terminal respectivamente. Estos algoritmos están implementados en nuestra librería, y son usados para crear el generador de parser LL(1). Este lo que hace es construir una tabla en función de los no terminales y los terminales, para predecir que producción es posible aplicar en cada estado. Una gramática puede no ser LL(1) aún cumpliendo las condiciones que dimos arriba. En este caso hay una ambiguedad para seleccionar la producción ha realizar. Lo que a nivel práctico sería que en la tabla, una casilla tenga más de una producción.

### Parser SLR(1)

Este parser es un poco más potente que el anterior, y su estrategia es muy diferente: es bottom-up. Este parser entra en la categoría de parsers Shift-Reduce, los cuales tienen una lógica funcional igual pero una estructura interna diferente. Tienen 2 tipos de acciones principales (que a grandes rasgos son):

- Shift: La cual le pide a la cadena el proximo token.
- Reduce: Saca del tope de la pila de `posibles producciones`, una producción válida.

Por detrás todos estos se basan en un autómata que reconoce todo prefijo viable de la gramática. El conjunto de estados de este autómata finito determinista, se le llama Colección Canónica de Items LR(0). Esta colección es hallada en primera instancia y luego se procede a rellenar las tablas `ACTION` y `GOTO` de cada parser.

En el caso de este parser `SLR(1)`:

- Cuando un Item del estado actual tiene un terminal como su próximo token, y existe una transición al estado que contiene el item luego de `comerse` el token, la sugerencia a rellenar en `ACTION` es `SHIFT`
- Cuanda el Item es reducible (es decir que ya no tiene más terminales o no terminales), solo sugiere `REDUX`, por cada uno de los Follows del No Terminal.
- La cadena se reconoce como válida cuando para la condición anterior el item del que hablamos el que contiene a la producción del Seudo Distinguido.
- En otro caso, cuando lo que viene en el Item es un No Terminal, lo que se va rellenando es la tabla `GOTO` con las prosibles transiciones que se puedan realizar.

### Parser LR(1)

En el caso del parser LR(1), los Items ahora tiene un token `lookahead` con lo que se espera ver. Estos items se llaman Items LR(1) y precisamente como esperan `ver` algo, se construyen con los Follows de la gramática.

Ahora la tabla de `ACTION` y `GOTO` cambian un poco pero ofrecen mayor potencia. Las 2 principales diferencias son:

- Cuanda el Item es reducible (es decir que ya no tiene más terminales o no terminales), solo sugiere `REDUX`, para el token de su `lookahead` y no para todo el Follow.
- Y la cadena se reconoce como valida cuando es reducible la producción del SeudoDistinguido y ya es el final de la cadena, es decir su `lookahead` es `EOF`.

## Análisis Semántico

Como el análisis semántico es particular de cada lenguaje, no ofrecemos una herramienta generica para este problema. Sin embargo para cada una de las gramáticas de ejemplo que tenemos mostramos las diferentes formas de hacer chequeo semántico usando el patrón visitor en los lenguajes: 6, 7 y 8.

## Generación de Código

La generación de Código al igual que el análisis semántico es particular de cada problema. Solo ofrecemos una implementación de una transpilación a Python para el lenguaje 7.
