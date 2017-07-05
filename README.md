# s3-tools

A collection of Python tools for processing source files for S3 resources.




## Building S3 slide decks

Build "S3 - All Patterns Explained" slide deck:

    s3slides build deckset|revealjs patterns.yml src/ target.md

Build skeleton file for "S3 - All Patterns Explained" slide deck:

    s3slides sekeleton patterns.yml src/

Export pattern list in various formats:

    s3slides export list|opml|d3|translation|markdown patterns.yml (--language=de)



## Future Plans: compiling slide decks

These tools can be used to build any kind of slide deck from a repository of sections in deckset format.

A section is a markdown file with one or more slides separated by `---`.

Sections are then organized into chapters. Content for a chapter is pulled from a subfolder of the sections repository.

A YAML file describes the order of chapters, and what sections will be included in what chapter. 

Also, an title slides and closing slides can be compiled from sections kept in the 'introduction' and 'closing' folders, also described through the YAML file.

Each chapter may have an `index.md` as a preamble, title slides as text or image (or both) can be generated for each chapter with commandline options.

Between introduction and chapters a set of illustrations for each chapter can be added (used for showing all patterns in groups in "S3- All Patterns Explained", probably less useful in other slide decks.)