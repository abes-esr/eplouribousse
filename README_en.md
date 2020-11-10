# Collaborative WebApp to manage serials deduplication in libraries.

Save space by eliminating duplicates, provide better readability of your collections by restoring for each of them a unique collection as clean as possible resulting from the aggregation of scattered items available in your libraries.

# Method:

For a given resource (Catalog Unit without filiations), "eplouribousse" allows libraries, each in turn, to indicate its bound elements contributing to the resulting collection, then in a second cycle of instructions and according to the same logic, its not bound complementary elements.

The order of processing is significant: The first library is normally the one already holding the most important collection (the one that claims conservation in the event that the collection is finally grouped). It is the same logic of importance that must prevail normally for the place claimed by the following libraries. It may happen that a library wants to subtract its collection to the reconstitution of the resultant (The typical case is that of a collection of the legal deposit) The positioning module of "eplouribousse" makes this derogation possible.

The sheets obtained describe the resulting collection ; the eliminated elements are deduced from this description (all that doesn't contribute to the resulting collection) The elements which contributes to the resulting collection may be grouped together or not, as desired. Physical treatments and catalog updates are expected.

See illustration here : https://seafile.unistra.fr/f/163d60a568e2482092e3/

# Features:

01. edition of the candidates for each taking part library,
02. positioning form (including derogations),
03. edition of the resources whose instruction of the resulting collection may begin,
04. alert when its turn came to continue the instruction of the resulting collection,
05. instruction forms (add, delete, modify, end),
06. neat worked pdf reports,
07. conformity check at the end of each process cycle,
08. full integrated workflow,
09. activity tracking chart,
10. cross-search by serial and library
11. users management,
12. authentication controls,
13. parameterization of derogation reasons,
14. administration of faulty card cases,
15. multilingual support (French, English, German, extensible to other languages)

# More information :

See the app manual in Doc repertory

Videos (in french ; please download if you cannot fully view) :
01. Assumptions and definitions : https://seafile.unistra.fr/f/dd5b8a16b1a5440389e5/
02. Méthod : https://seafile.unistra.fr/f/590ba4359f3e4b73b60e/
03. Database preparation : https://seafile.unistra.fr/f/9581ffba08f24e849b08/
04. Example of end-to-end processing : https://seafile.unistra.fr/f/b87faa2857ee42bab57f/
05. Site administration : https://seafile.unistra.fr/f/d3f6a23f94804dfabddd/
06. Credits : https://seafile.unistra.fr/f/579d874730604579b073/

# How to get eplouribousse?

In order to have an idea of what it turns about and what it looks, we first recommand to take a tour on one of these real instances :
01. https://eplouribousse1.di.unistra.fr/
02. https://eplouribousse2.di.unistra.fr/
03. https://eplouribousse3.di.unistra.fr/

----------------

It looks good ? Let's try it on your desktop with the Django development server ; this will allow you to test all features (Mail alerts will be edited in the console).

Debian Linux users : follow the step-by-step instructions in Doc/howto.txt

----------------

You're OK and you want the real one with all the conveniences ?
We recommend that you first approach your IT team for a test installation.

If you want to use eplouribousse for a firm project, there are three possibilities at the moment :
- Entrust the deployment to your IT department by indicating the address of this site
- Entrust the deployment to a host indicating the address of this site
- We entrust the deployment (subject to agreement)

In all cases, let us know that you're interested (see contact below)

# Credits :

French version uses data under etalab license (Open License) provided by Abes (Abes : Bibliographic Agency for Higher Education is a french public institution, located in Montpellier supervised by the Ministry for Higher Education Research, Innovation)

# Contact :

See https://github.com/GGre/eplouribounistra/blob/master/contact.txt
