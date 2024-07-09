FROM sphinxdoc/sphinx:7.1.2

RUN apt-get update && apt-get install -y --no-install-recommends plantuml doxygen

RUN pip install sphinx_rtd_theme==2.0.0

RUN pip install sphinxcontrib-plantuml==0.30

RUN pip install breathe==4.35.0

COPY download_releases.py /usr/local/bin
COPY build.sh /usr/local/bin/build.sh

ENTRYPOINT [ "/usr/local/bin/build.sh" ]
