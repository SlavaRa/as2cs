# as2cs

Tiny example of converting a bit of syntax from ActionScript 3 to C# and back from C# to ActionScript 3.  Compares compatible grammars.

Typographify example of using SimpleParse is from David Mertz' copyrighted article, cited in that directory.

Installation
============

Depends on Python SimpleParse 2.2.  You can install SimpleParse here:

https://pypi.python.org/pypi/SimpleParse/

Test discovery depends on Python 2.7 or higher.

Usage
=====

ActionScript to C#:

        python as2cs.py file.as

C# to ActionScript:

        python as2cs.py file.cs

Overwrites file with corresponding extension.

Examples
========

* Convert model from game jam.  <https://github.com/ethankennerly/unconventional-weapon>
* Example conversion of game jam model and controller.  <https://github.com/ethankennerly/monster>
* Example conversion of rules from PowerPlant.  <https://github.com/ethankennerly/powerplant>

Specify collection data type
============================

Although the syntax converts, since C# is strict about explicitly typing, you probably want to explicitly type ActionScript Arrays into Vectors.  This script converts Object hashes into `Dictionary<string, object>`.  Examples of vim sed for List of integers:

        %s/Array/Vector.<int>/gIce

Literal list:

        %s/\[/new <int>[/gIce

List of list of integers:

        %s/Array/Vector.<Vector.<int>>/gIce

Access object without dot notation:

        %s/\(container\)\.\([A-Za-z0-9_]\+\)/\1["\2"]

Wrap DataUtil
=============

as2cs.py converts syntax.  Sometimes syntax is not enough information to infer a difference in idioms and functions between the languages.  For example, property 'length' of an ActionScript Array is converted to 'Count', presuming it is a generic collection.  A Vector is converted to a List.  Another way to port is to replace 'a.length' with DataUtil.Length(a).

        import com.finegamedesign.utils.DataUtil;

This vim sed command replaces the ActionScript:

        %s/\([_A-Za-z0-9\.\[\]]\+\)\.length\>/DataUtil.Length(\1)/gIce

For another example, wrap cloning an ActionScript Array:

        args test/*.as
        argdo %s/\([A-Za-z0-9\.\[\]]\+\)\.concat()/DataUtil.CloneList(\1)/gIce | update

Shifting element from head of a list:

        %s/\([A-Za-z0-9\.\[\]]\+\)\.shift()/DataUtil.Shift(\1)/gIce | update

Joining strings:

        %s/\([A-Za-z0-9\.\[\]]\+\)\.join(\([^)]\+\))/DataUtil.Join(\1, \2)/gIce

See DataUtil.as and DataUtil.cs for the supported wrappers.

* C# does not support reserved keyword 'event'.  Replace those.


Grammar Documentation
=====================

SimpleParse:
http://www.ibm.com/developerworks/linux/library/l-simple/index.html
http://blog.dowski.com/2007/12/19/simpleparse-plug/
http://www.vrplumber.com/programming/simpleparse/simpleparse.html

EBNF:
http://simpleparse.sourceforge.net/simpleparse\_grammars.html

Convert Unit Test Features
==========================

* DataUtil.as and DataUtil.cs wrapper for consistent API.
* Pass Unity 5.2 compiler check of TestSyntaxModel.cs when copied to Assets folder.

        bash test_copy_to_unity.sh

* ASUnit-to-NUnit test assert equals.  
  ActionScript:

        assertEquals(expected, got)

  C#:

        Assert.AreEqual(expected, got)

* ASUnit-to-NUnit test assert equals with message.
  ActionScript:

        assertEquals(message, expected, got)

  C#:

        Assert.AreEqual(expected, got, message)

* ASUnit-to-NUnit test function.  Expects namespace is public.
  ActionScript:

        public function testThis():void

  C#:

        [Test] public void testThis()

* ASUnit-to-NUnit test class.  Any namespace.
  ActionScript:

        internal class TestThis extends TestCase{}

  C#:

        [TestFixture] internal class TestThis{}

* ASUnit-to-NUnit import.  Any namespace.
  ActionScript:

        import asunit.framework.TestCase;

  C#:

        using NUnit.Framework;

* Other asserts not supported.  You could rewrite other asserts in assert equals format.  Example of single-dimension array equality using vim sed:

        %s/assertEqualsArrays(\(.*]\)\(, Calculate.*\)\())\)/assertEquals(\1.toString()\2.toString()\3/

Features
========

* Run discovered doctests and unit tests:

        python test.py
        # or
        python -m unittest discover

* Grammar unit test format related to gUnit.
* Merge grammar declaration files.
* Transcribe 'import' example of common base grammar.
* Replace literal 'import' with 'using' by grammar.
* Reformat an example variable declaration by grammar.
* Convert trivial package with one import.
* Markup class suffix from import.
* Convert empty base class declaration.
* Convert basic example variables bi-directionally:  C# to ActionScript.
* Convert simple namespace from C# to ActionScript.
* Comment grammar adapted from simpleparse.common.comments 
  with literals extracted and no unreported or expanded definitions
* Conform expected format in compilation unit test.
* Preserve comments around namespace and class.
* Convert function declaration.
* Convert simple local variable assignment.
* Convert floating point number suffix.
* C# float suffix in capital case 'F'.
* Convert member and static variables.
* Distinguish if C# implements or extends only by prefix.  
  Interfaces are conventionally be prefixed by "I" and uppercase letter.
  Example:

        class A : IB {}
        class A implements IB {}
        class A : B {}
        class A extends B {}
        class A : It {}
        class A extends It {}

* Convert extended class declaration.
* Example file of all of the above.
* Grammar literals in CAPITAL\_CASE following ANTLR grammar conventions.
* Grammar ordered approximately in same order as the elements appear in a file.
* Grammar names in snake\_case following simpleparsegrammar conventions.  Vim sed:

        %s/\([a-z]\)\([A-Z]\)/\1_\L\2/gIce

  http://vim.wikia.com/wiki/Switching\_case\_of\_characters
* Equality operators.
* Strictly equals to ReferenceEquals.
  http://stackoverflow.com/questions/4704388/using-equal-operators-in-c-sharp
* ActionScript undefined to C# null.
* ActionScript in operator to C# Contains only with some addresses.
* Convert simple relational expressions verbatim.
* If statement.
* Shared assignment operators.
* Array and hash access.
* Create new object.
* Ternary expression.
* ActionScript Vector to C# List data type.
  http://stackoverflow.com/questions/3487690/multidimentional-vector-in-as3
* Prefix import of C# collections.

        using System.Collections;
        using System.Collections.Generic;

* ActionScript untyped Array to C# ArrayList data type.
* ActionScript Array literal.
  http://stackoverflow.com/questions/1723112/initializing-arraylist-with-constant-literal
* For loop iteration.  Grammar is more permissive than a compiled for loop.
* While loop iteration; break and continue keywords.
* Cast some reserved data types.  ActionScript type-casting to C# type-casting by type function only for some reserved data types.  With custom data types, it is ambiguous of a type is cast or if an arbitrary function is called.  Instead the ActionScript "as" keyword is clear.  However, C# does not permit "as" used with non-nullable types, such as int or float.
* Cast type by "as" keyword.  Won't work for int or float.  Use explicit type instead.  Example:

        Assets/Scripts/Model.cs(70,79): error CS0077: The `as' operator cannot be used with a non-nullable value type `float'
 
  http://stackoverflow.com/questions/496096/casting-vs-using-the-as-keyword-in-the-clr
* Replace a few frequently used array properties and methods by pattern recognition only.
  So other instances with these same methods or properties are also replaced.
* ActionScript Vector.length to C# List.Count.
* ActionScript Vector.concat() to C# List.Clone().
* ActionScript Vector.push to C# List.Add.
* ActionScript Array.concat() to C# ArrayList.Clone().
* ActionScript Array.push to C# ArrayList.Add.
* ActionScript Array.length to C# ArrayList.Count.
* ActionScript \*.indexOf to C# IndexOf.
* ActionScript \*.splice 1 to C# RemoveRange.  NOT compatible with adding elements:

        array.splice(index, 1, added0, added1);

  Alternatively, Flash 19 supports removeAt and insertAt.
* No return type in constructor.
* Dynamic data type using local 'var' keyword, since Unity 5.3.4 compiler still does not support dynamic data type as a function parameter.  So will not support dynamic return types.
* Keyword 'is'.
  https://msdn.microsoft.com/en-us/library/dd264741.aspx
* Limited use of 'typeof' function for JavaScript basic types only.  Caveat:  In JavaScript, this returns a string.  In C# this returns a type.  So this would be portable code:

        typeof(a) == typeof("")

  This would not be:

        typeof(a) == "string"

  Since JavaScript returns all instances as "object", this is also not portable:

        var a:A = new A();
        var b:B = new B();
        typeof(a) == typeof(b)

  http://stackoverflow.com/questions/310820/how-to-check-if-two-objects-are-of-the-same-type-in-actionscript
* Parse float and parse integer.  However, C# throws exception if not perfectly formatted.
  And whitespace is not permitted inside "int.Parse" or "float.Parse".
  http://stackoverflow.com/questions/3960499/better-use-int-parse-or-convert-toint32
* Markup delegate type.  C# requires signature and return type.
  In ActionScript, some of this can be specified with a compilable convention and comment markup.
  Return type is data type.  Void is not supported data type, so use no type.
  The data type of the function object is in the preceding comment block with no whitespace.
  ActionScript:

        internal var /*<delegate>*/ ActionDelegate:/*<void>*/*;
        internal var onComplete:/*<ActionDelegate>*/Function; 

  C#:

        internal delegate /*<void>*/dynamic ActionDelegate();
        internal /*<Function>*/ActionDelegate onComplete;

  ActionScript:

        public var /*<delegate>*/ IsJustPressed:Boolean, letter:String;
        public function getPresses(justPressed:/*<IsJustPressed>*/Function):Array{}

  C#:

        public delegate bool IsJustPressed(string letter);
        public ArrayList getPresses(/*<Function>*/IsJustPressed justPressed){}

* ActionScript "trace" to Unity C# Debug.Log with a single string as the argument.
* JavaScript Math functions to Unity C# Mathf functions.
  http://help.adobe.com/en\_US/FlashPlatform/reference/actionscript/3/Math.html
  http://docs.unity3d.com/ScriptReference/Mathf.html
* Random.  Careful:  Unity C# Random.value includes 1.0.  
  Wrapping in modulus theoretically biases the distribution toward 0.
  ActionScript:

        Math.random()

  Unity C#:

        (Random.value % 1.0f)

* Context when function body not parsed.
* Return statement.
* Convert example TestSyntaxModel.as from Anagram Attack.
* Insert "using UnityEngine" if converting to Mathf or Random.
* Convert ActionScript hash to Dictionary with string-typed key.  Import generics.

        Dictionary<string, object>

 Some people are saying Unity 5 still does not support C# 4 'dynamic' keyword.
 On my test of Unity 5.2, dynamic keyword compiled.  But MonoDevelop-Unity debugger does not recognize dynamic keyword.
 http://stackoverflow.com/questions/36079609/using-c-sharp-dynamic-typing-in-unity-5-3-1f
 http://answers.unity3d.com/questions/686244/using-c-dynamic-typing-with-unity-434f1.html
* Dictionary iteration over keys:  for in with type.
  ActionScript:

        for (var key:String in items) {
            text += key;
        }

  C#:

        foreach (var item in items) {
            string key = item.Key;
            text += key;
        }

* ActionScript Dictionary to C# Hashtable data type.
* ActionScript string.toLowerCase to C# String.ToLower
* ActionScript lastIndexOf to C# LastIndexOf
* Basic chained call.
* To-string camelCase to CapitalCase.

* Unary subtraction.
* Ternary inside of parameter list.
* Delete expression with only an identifier.  Does not support "a.b.c[d]"
* Throw one kind of expression.  Error :: System.InvalidOperationException

* Optional cfg: 'is\_conform\_case' flag:  ActionScript first letter of function and namespace in camelCase to first letter C# CapitalCase.  Include all function or method calls.  Exclude casts.  Complexities would be to recognize delegates.
  ActionScript:
        function doThis():void{doThis(); b.do(); A.B.c.go(); int(a); e[i]();}
  C#:
        void DoThis(){DoThis(); b.Do(); A.B.c.Go(); (int)(a); e[i]();}

* Remove preceding sector domain from namespace.
  ActionScript:
        import com.finegamedesign.utils;
  C#:
        using Finegamedesign.Utils;

ActionScript to JavaScript
==========================

* Integer type cast:

    int(x)

    Math.floor(x)

* Declare typed variable:

    var i:uint = 0;
    var i/*<:uint>*/ = 0;

    var svar:String = "";
    var svar/*<:String>*/ = "";

* Cocos2D log.
    cc.log

* Member variable.

Not supported: ActionScript to JavaScript
=========================================

* ActionScript 3 data types to EcmaScript react flow data types:
 boolean
 number
 int
 string
 any
 Array<number>
 GenericObject<number>

<https://flowtype.org/docs/five-simple-examples.html#adding-type-annotations>
<https://flowtype.org/docs/builtins.html>

* ActionScript to ES7 experimental stage 2 class properties.
 ES7 stage 2 syntax approaches a lot of ActionScript syntax (fork of ES4).
 There is no namespace.
 Member variables have no var keyword.
 Yet this syntax is a lot closer to ActionScript than ES5 JavaScript pseudo classes.
 Example of testing ES7 react stage 2:

    $ babel test_as2js/es7.js > test_as2js/es5.js && mocha test_as2js/test_es5.js

<https://flowtype.org/docs/classes.html>

<https://babeljs.io/repl/#?babili=false&evaluate=true&lineWrap=false&presets=es2015%2Creact%2Cstage-2&code=class%20C%7B%0A%20%20constructor()%7B%0A%20%20%20%20this.a%20%3D%2010%3B%0A%20%20%7D%0A%7D%0A%0Avar%20c%20%3D%20new%20C()%3B%0Aconsole.log(c.a.toString())%3B>

<https://babeljs.io/docs/learn-es2015/>

* Compile ES2017 react, stage-2 to JavaScript (ES3).  Run babel from command line.

 Install babel to local project.

    $ npm install --save-dev babel-cli babel-preset-es2015 babel-preset-es2017 babel-preset-stage-2
    $ echo '{ presets: ["es2015", "es2017", "react", "stage-2"]}' > .babelrc
    $ babel test_as2js/es7.js > test_as2js/es5.js
    $ node test_as2js/es5.js

<https://babeljs.io/docs/plugins/preset-es2015/>
<https://babeljs.io/docs/plugins/preset-es2017/>
<http://babeljs.io/docs/plugins/preset-stage-2/>
<http://babeljs.io/docs/plugins/preset-react/>

* Method.
* Class.
* Static variable.
* Static function.
* Extract static classes from object declaration if statics are all grouped first.

    class C{static function f(){} function g(){}}
    
    var C = {g: function(){}};
    C.f = function(){};

* Define int as Math.floor in global scope.

    var int = Math.floor;
    ...
    int(x)

* Scope members.

    f(x){y = x;}
    f(x){this.y = x;}

* Default argument.

    function f(x:Number, i:int = -1){}

    f: function(x/*<:Number>*/, i/*<:int>*/){
        if (undefined === i) {i = -1;}
    }


* Extract static classes from object declaration in any order.

    class C{function f(){} static function g(){}}
    
    var C = {f: function(){}};
    C.g = function(){};

* Imports to requires.
* Unit test.

* Cocos2D super.
    var a; super(a); super.f(1);
    var a; this._super(a); super.f(1);
* Grammar specific to a difference:  as2js grammar. as2cs grammar.
* Console log.
* Define ActionScript syntax as extension of JavaScript, or vice versa.
* Extend class.
* Declare untyped variable.  You can use:

    var varj:* = cameras.length;
    var varj/*<:*>*/ = cameras.length;
* Constant keyword.
* Source conversion.  as3js has demos of that.  as3js test I ran depended on some runtimes of AS3JS.

<http://as3js.org/>


Not supported
=============

* If you'd like to request a pull or fork to add a feature, that'd be appreciated!

* Extend unit tests to include JavaScript examples.
* If JavaScript example exists, run it.  If length is short or item is None, skip.
* Convert ActionScript to JavaScript.  
 See:

<http://github.com/ethankennerly/as2js>

* Convert ActionScript ASUnit to JavaScript Mocha TDD.
* Call after an array index:
        pools["Explosion"].next()

* Constants:  These are static in C# but not necessarily static in ActionScript.  You can use variable instead.
* isNaN :: IsNaN
* Conditional expressions mixing reordered calls without parentheses.  ActionScript, C#:
        null == hash || key in hash
        null == hash || hash.ContainsKey(key)
  Instead wrap parentheses:
        (null == hash) || (key in hash)
        (null == hash) || (hash.ContainsKey(key))
* Roundtrip nested literal array of hash literals.
* Expression of call with array access suffix.
* Regular expression.
* Parenthetical expression with function call suffix.
* Match whitespace when empty array literal, hash literal and following newline.
 In C# there are curly braces.  When the curly braces are empty or a single line, put on a single line.  

  Expected:

                var selectsNow:Array = [];

  Got:

                var selectsNow:Array = [
                ]
                ;

* Overriding virtual functions in C#.
  http://stackoverflow.com/questions/1327544/what-is-the-equivalent-of-javas-final-in-c
* Interface definition.
* Delegate with variable number of arguments.
* Arbitrary number of parameters:  ActionScript "... rest" to C# "T[] params".
* Match whitespace in roundtrip conversion.  Instead there might be extra new lines.
* Call as2cs.py from a different directory than as2cs.py directory.
* Convert nested strictly equals.  Example:

        var isChanged:Boolean = g === grid[index] || g === gridPreviously[index]

  Instead you could replace with equals:

        var isChanged:Boolean = g == grid[index] || g == gridPreviously[index]

* Do not reformat braces and lines in comments.
  Recognize data type is a collection.  Only convert length to Count if so.
* ActionScript string.length to C# String.Length.  Instead DataUtil.Length is available.  Replace:
  Vim sed:

        %s/\([A-Za-z0-9\.]\+\)\.length\>/DataUtil.Length(\1)/gIce

* Split string into an array of strings without a delimiter.  
  ActionScript:

            var letters:Array;
            letters = text.split("");

  C#:

            using System.Linq;
            ...
            ArrayList letters;
            letters = text.ToCharArray().Select(c => c.ToString()).ToArray();

 http://stackoverflow.com/questions/1485237/split-string-in-c-sharp-without-delimiter-sort-of
 http://stackoverflow.com/questions/7936235/how-to-convert-a-char-array-to-a-string-array
 http://stackoverflow.com/questions/7089048/lambda-expression-for-enumerable-select
  An alternative would be to specify a C# character array in ActionScript markup:

            var letters:/*<char[]>*/Array;
            letters = text.split("");

  C#:

            char[] letters;
            letters = text.ToCharArray();

  Another alternative is a utility function:

            letters = Toolkit.split(text);

  C#:

            letters = Toolkit.split(text);

* Access ArrayList explicitly convert to type.  Instead use a vector.  ActionScript:

        var inputs:Array = [];
        var letter:String = inputs[i];

  C#:

        ArrayList inputs = new ArrayList(){};
        string letter = (string)inputs[i];

* ActionScript pop to C#.

        var letter:String = inputs.pop();

  C#:

        string letter = (string)inputs[inputs.Count - 1];
        inputs.RemoveAt(inputs.Count - 1);

* Set ActionScript array.length to C#.  Could use splice instead.

        inputs.length = 0;

        inputs.RemoveRange(0, inputs.Count);

* ActionScript join to C#.  May want string List or wrapper instead of:

        var submission:String = inputs.join("");

        string submission = string.Join("", ((string []) inputs.ToArray(typeof(string))));
        
* Explicitly cast float to int.  Example without cast that C# compiler rejects:

        int r = (Random.value % 1.0f) * (i + 1);

* Explicit type-casting on access to a ArrayList to a data type.  Instead you can use an ActionScript Vector.
* ActionScript typed Vector literal to C# typed list literal.
* ActionScript delete a to C# .Remove(a).
* ActionScript clear(d) to C# d.Clear().
* ActionScript single-quoted strings to C# double-quoted strings, with escaping subquotes.  C# reserves single-quoted strings for single-characters.  Instead, you can replace in ActionScript the single-quotes with double-quotes.  Example ActionScript:

            trial({'help': 'Hello world'});

* Post-syntax conversion, parse to replace corresponding function names and signatures.
* Notify ActionScript 'base' as identifier.  C# reserves 'base'
* Hash literal without space before value in key value pair.
* Set this property by name.  This is slow in ActionScript and C#.
 ActionScript:

        this[key] = params[key];

 C#:

        this.GetType().GetProperty(key).SetValue(this, params[key]);

 http://stackoverflow.com/questions/1196991/get-property-value-from-string-using-reflection-in-c-sharp

* Recognize if the C# owner is an array or collection, otherwise get/set property by name.  

        this[key] = params[key];

* Recognize if the instance is not a vector or array to not replace.
  The property "length" is used in a lot ways.
* C# typed Array to ActionScript typed Vector.
* ActionScript and C# wrappers for common collection actions: clone, push, length.  
  Written in target language.
* C# Hashtable literal with dot.addresses to ActionScript.
* Null check
  ActionScript:

        null != parameters["text"]

  C#:

        parameters.ContainsKey("text")

* Nested function definitions.
* Key iteration over an array (also "for in" syntax in ActionScript).
* For in hashtable without a block.
* ActionScript only allows literal keyword, string, number default in signature.
* Profile function hotspots in unit tests.
* Foreach statement.
* Reformat and reorder may insert some optional grammar, such as class base.
* Reorder with nested grammar.  Otherwise the expanded form is needed, since the raw grammar text is parsed.
  This creates redundancy.  Example:
        contains_expression := expression, ts, IS_CONTAINED_IN, ts, container_expression
        contains_not_expression := LNOT, ts?, LPAREN, ts?, expression, ts, IS_CONTAINED_IN, ts, container_expression, ts?, RPAREN
* Strict condition without whitespace around operator:
        a===b
        object.ReferenceEquals(a,b)
* Tolerate Unicode byte-order-marker at start of the file.
* Distinguish order of operators that will be translated verbatim.
* Logging.  Instead, wrap ActionScript trace and Unity C# Debug.Log in Toolkit.log.
* Nested list literals.
* Anonymous function.
  https://msdn.microsoft.com/en-us/library/0yw3tz5k.aspx
* Combine literal from multiple literals: 

        MARKUP_START := COMMENT_START, COMMENT_MARKUP_START
        MARKUP_END := COMMENT_MARKUP_END, COMMENT_END

* Dynamic (\*) input parameter. My Unity 5.2 C# did not accept dynamic input parameter.
  http://stackoverflow.com/questions/26070365/c-sharp-unity-internal-compiler-error-system-runtime-compilerservices-callsi

* C# static class to ActionScript class.
* Ungrouped ternary repetition

        i ? 1 : b ? c : 4

  Instead you could write:

        i ? 1 : (b ? c : 4)

* ActionScript dynamic class to C# class.
* Insert C# explicit cast to another data type, such as from float to integer.
* C# Generic classes and interfaces:

        class B<U,V> {...}
        class G<T>: B<string,T[]> {...}

* C# nested classes:

        class A
        {
            class B: A {}
        }

* Vim SimpleParse grammar syntax highlighter:

        / instead of |
        Comma required
        := assignment operator

* ActionScript 3 argument list '...' syntax
* Recognize if C# needs to be converted to ActionScript Dictionary, or if an Object suffices.  Recognize if iterating a dictionary with string key or a general hashtable.
* Markup ActionScript Dictionary to C# with explicit types of keys and values if possible.  Not ActionScript Dictionary to C# Dictionary\<dynamic, dynamic\>:  This was frowned upon as being slow and error-prone:
  http://stackoverflow.com/questions/13566915/dictionarydynamic-dynamic-value-items-cant-be-accessed-c-sharp
* JavaScript typeof string to C# type.
  http://stackoverflow.com/questions/310820/how-to-check-if-two-objects-are-of-the-same-type-in-actionscript
* Convert extended class declaration that has no whitespace:

        class A:B {}

* Reordering syntax from nested definitions.  
  Example:  ActionScript 3 has a colon before data type.  Formatting scans this grammar.

        argumentDeclared := identifier, (ts?, COLON, ts?, dataType)?
        argumentDeclared := dataType, ts, identifier

* Reformatting with optional parameters.  
  Instead I used two optional definitions, one which requires the option.  C# example:

        functionDeclaration := functionModified / functionDefault
        functionModified := ts, namespaceModifiers, returnType, ts, functionSignature
        functionDefault := ts, returnType, ts, functionSignature

* Member variable and function declarations without preceding whitespace.  
  Instead have at least one space or tab before the.
  Whitespace is required to retain when reformatted.
* Default data-type when omitted in ActionScript to explicit data type in C#.
* Declare multiple variables in a statement, but C# does not permit assigning them.  Instead write one per statement.  This looks messy to me.
  http://stackoverflow.com/questions/13374454/declare-and-assign-multiple-string-variables-at-the-same-time
* Omitting semicolon at end of ActionScript.
* Mixing literals and non-literals in grammar to be replaced.
* Multiple occurences of items that are reordered.  
  Instead these can be grouped, like 'digits?' instead of 'digit\*'.
* Whitespace between grammar element and occurrence indicator.
* Preprocessor directive 'include'
* Consistent prettify format that trims whitespace.
* Prettify format from optional end of line and indentation in grammar.
* Regular expressions.
* camelCase method names to CapitalCase method names.
* ActionScript only allows one public class per package and one package per file.
* ActionScript 2 instanceof keyword.
* ActionScript 2.
* Scope of variables declared a block are available outside the block in JavaScript.
* C# does not have logical assignment.  ActionScript does.  Instead bitwise assignments exist.
 http://stackoverflow.com/questions/6346001/why-are-there-no-or-operators
 http://help.adobe.com/en\_US/FlashPlatform/reference/actionscript/3/operators.html
* C# does not have bitwise unsigned shift:

        >>>
        >>>=

  nor bitwise not:

        ~=

  Both have bitwise shift:

        >>

* Validate that initializations are last in a function parameter list.
* JavaScript elision:

        var a = [, , ,];

* C# pointers.
* Compiling bytecode.
* Everything else not explicitly mentioned as a feature.

Reference code
==============

* Intro to parsing and left-recursion.
  http://www.cs.kau.se/cs/education/courses/dvgc01/lectures/Syntax.pdf
* ANTLR4 grammars
  https://github.com/antlr/grammars-v4
* ActionScript 3 grammar in ANTLR3
  http://svn.badgers-in-foil.co.uk/metaas/trunk/src/main/antlr/org/asdt/core/internal/antlr/AS3.g
  http://stackoverflow.com/questions/1839146/as3-grammar-most-accurate
* ECMAScript grammar in ANTLR3
  http://antlr3.org/grammar/1153976512034/ecmascriptA3.g
  http://stackoverflow.com/questions/1786565/ebnf-for-ecmascript
* C# grammar
  https://msdn.microsoft.com/en-us/library/aa664812(v=vs.71).aspx
  https://github.com/ChristianWulf/CSharpGrammar/blob/master/grammars/CSharp4.g
  https://antlrcsharp.codeplex.com/
* ANTLR by Terrence Parr
  https://en.wikipedia.org/wiki/ANTLR
* Meta AS for ANTLR
  http://grepcode.com/snapshot/repo1.maven.org/maven2/cc.catalysts/metaas/0.9/
* gUnit:  Grammar unit test for ANTLR
  https://theantlrguy.atlassian.net/wiki/display/ANTLR3/gUnit+-+Grammar+Unit+Testing
* as2cs:  ActionScript to C# converter in Java by weeeBox
  https://github.com/weeeBox/oldies-bc-as3converter
* as2js:  Partial ActionScript to JavaScript converter script
  https://github.com/ethankennerly/as2js
* ActionScript 3 parser in Ruby
  https://github.com/gamemachine/as3/tree/master/parser
* Program transformation system in DMS
  http://stackoverflow.com/questions/28711580/how-to-write-a-source-to-source-compiler-api
  https://en.wikipedia.org/wiki/DMS\_Software\_Reengineering\_Toolkit
