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
04. alerts may be activated (ranking, arbitration, instruction, edition),
05. instruction forms (add, delete, modify, end),
06. neat worked pdf reports,
07. conformity check at the end of each process cycle,
08. full integrated workflow,
09. activity tracking chart,
10. cross-search by serial and library,
11. users management,
12. authentication controls,
13. parameterization of derogation reasons,
14. administration of faulty card cases,
15. internationalization (English and German in progress, possible extension to other languages),
16. contact forms : to contact either the webmaster(s) or the developer(s),
17. csv export for the main lists,
18. autonomous password management,
19. private / public setting for simple edition.

# Démo :

https://seafile.unistra.fr/f/c2e9ec44798f490087f7/

# Other services :

* Bug tracking tool (Launchpad) : https://bugs.launchpad.net/eplouribousse
* eplouribousse newsletter (Renater list) : https://groupes.renater.fr/sympa/info/eplouribousse-newsletter (french)
* User Forum (Renater list) : https://groupes.renater.fr/sympa/info/eplouribousse

# More information :

See the app manual in Doc repertory

Videos (in french ; please download if you cannot fully view) :
01. Assumptions and definitions : https://seafile.unistra.fr/f/dd5b8a16b1a5440389e5/
02. Méthod : https://seafile.unistra.fr/f/590ba4359f3e4b73b60e/
03. Database preparation : https://seafile.unistra.fr/f/9581ffba08f24e849b08/
04. Example of end-to-end processing : https://seafile.unistra.fr/f/b87faa2857ee42bab57f/
05. Site administration : https://seafile.unistra.fr/f/d3f6a23f94804dfabddd/
06. Credits : https://seafile.unistra.fr/f/579d874730604579b073/

# How to take advantage of eplouribousse?

The scope of version 2 was to make the institutions free from any deployment operation for its own instance. The institutions only have to make their project database available on a server of their choice and to authorize the write access to the instance on which their project depends.

As it has not yet been tested in a real-life production environment, this version should be considered a private beta test version as defined in the Wikipedia article "Software release life cycle": "Software beta releases can be either public or private, depending on whether they are openly available or only available to a limited audience. Beta version software is often useful for demonstrations and previews within an organization and to prospective customers. Some developers refer to this stage as a preview, preview release, prototype, technical preview or technology preview (TP),[14] or early access."

(For now, the stable version is version 1, but its deployment has proved tricky, which was the main reason for the development of version 2).

The main objectives of the beta test phase are the following:
- To highlight possible bugs
- To correct possible major defects of the user interface
- Observe the effect of an increase in the volume of projects supported by a single instance (in theory, an instance can support up to 100 projects, i.e. 100 databases)

Candidate beta testers will benefit from free online training (users and administrators), full online assistance in populating their database, advice on setting up the database on a server of their choice, remote assistance to users and, if the institution so wishes and where possible, the recovery of work already done during the transition to the final version.

Visit the beta test instance: https://sbu-eplouribousse.unistra.fr/

If you have a project to deduplicate paper journals in your institution, take advantage of this opportunity to apply. If you do not have a specific project but are interested in participating in the test, contact us (see contact at the bottom of this page).

# Credits :

French version uses data under etalab license (Open License) provided by Abes (Abes : Bibliographic Agency for Higher Education is a french public institution, located in Montpellier supervised by the Ministry for Higher Education Research, Innovation)

# Contact :

See https://github.com/GGre/eplouribounistra/blob/master/contact.txt
