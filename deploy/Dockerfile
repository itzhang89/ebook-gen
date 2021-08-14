FROM pandoc/latex

RUN tlmgr install quoting || exit 1

COPY fonts/*.ttf /usr/share/fonts/