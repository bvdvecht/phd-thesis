# Bart van der Vecht's PhD Thesis

Dissertation, propositions, and cover image of Bart van der Vecht's PhD thesis.
The LaTeX template was taken from 
https://github.com/cdelledonne/phd-thesis.

## Dissertation

To generate a PDF of the dissertation, compile the LaTeX document
`dissertation.tex`. Remember to use the class option `print` when generating a
PDF intended to be submitted for printing.

## Propositions

To generate a PDF of the propositions, compile the LaTeX document
`propositions.tex`.

## Cover

The cover image is stored inside the folder `cover/` as an Inkscape SVG file.
The following instructions require that you have Inkscape (and thus the
`inkscape` command) installed.

To generate a PDF of the full cover, including back side, front side, spine,
bookmark, and bleed margin of 2mm, run:

```sh
inkscape --export-margin=2 --export-filename=cover.pdf cover.svg
```

To generate a PDF of the front side of the cover, run:

```sh
cat cover.svg |
    sed '0,/viewBox.*/s//viewBox="180 0 170 240"/' |
    sed '0,/width.*/s//width="170mm"/' |
    inkscape --pipe --export-filename=cover-front.pdf
```

To generate a PDF of the back side of the cover, run:

```sh
cat cover.svg |
    sed '0,/viewBox.*/s//viewBox="0 0 170 240"/' |
    sed '0,/width.*/s//width="170mm"/' |
    inkscape --pipe --export-filename=cover-back.pdf
```

To generate a PDF of the bookmark, run:

```sh
cat cover.svg |
    sed '0,/viewBox.*/s//viewBox="355 0 60 240"/' |
    sed '0,/width.*/s//width="60mm"/' |
    inkscape --pipe --export-filename=bookmark.pdf
```

