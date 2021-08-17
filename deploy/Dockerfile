FROM pandoc/latex

# switch to qinghua respository
RUN tlmgr option repository https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/tlnet
RUN tlmgr update --self --all --reinstall-forcibly-removed

RUN tlmgr install quoting ctex fandol || exit 1
COPY template/*.tex /data/template/
#COPY fonts/fandol/*.otf /usr/share/fonts/

RUN rm -rf /opt/texlive/texdir/texmf-dist/doc  \
       /opt/texlive/texdir/readme-html.dir \
       /opt/texlive/texdir/readme-txt.dir  \
       /opt/texlive/texdir/install-tl*