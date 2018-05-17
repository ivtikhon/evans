## EVANS

### In late 1780's Oliver Evans, an American inventor, engineer and entrepreneur, designed and built an automatic flour mill. That was the first implementation of a completely automated industrial process.

This project is an attempt to design a programming language (which will be named *Evans* upon arrival), that would allow software developers to reduce time they spend on coding by employing capabilities of *Automatic Planning* for code generation.

Automatic planning is a branch of *Artificial Intelligence* that studies search algorithms in application to automated problem solving. *Planning Domain Definition Language (PDDL)* is the language that was designed for *International Planning Competition* in 1990's, and became de-facto standard for the planning community.

Our goal is to extend PDDL with some execution functionality, empowering PDDL planners to not only generate plans, but also execute them. PDDL itself, though, has some disadvantages that we would like to address:
* archaic hard to read syntax;
* global scope of variables (predicates);
* boolean (true/false) nature of variables (predicates);
* lack of practical usefulness of the generated plan.
