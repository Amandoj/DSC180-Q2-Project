
ARG BASE_CONTAINER=ucsdets/datahub-base-notebook:2022.3-stable

FROM $BASE_CONTAINER


LABEL maintainer="UC San Diego ITS/ETS <ets-consult@ucsd.edu>"

RUN wget https://data.qiime2.org/distro/core/qiime2-2022.11-py38-linux-conda.yml
RUN conda env create -n qiime2-2022.11 --file qiime2-2022.11-py38-linux-conda.yml

CMD ["/bin/bash"]

#emersonchao/dsc180b:latest
