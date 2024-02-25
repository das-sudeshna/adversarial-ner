# Adversarial NER

Code used in the paper [Resilience of Named Entity Recognition Models Under Adversarial Attack](https://aclanthology.org/2022.dadc-1.1/).

## Usage

### Convert IOB/IOBES tagging scheme to IO
`python iox-to-io.py data.conll` to convert a CoNLL format file with IOB/IOBES tagging scheme into IO tagging scheme.
Generates `data-io.conll` from `data.conll`.

### Generate adversarial evaluation file
`python adversarial.py data-io.conll` to generate the CoNLL format adversarial evaluation files.
Generates:
- `data-io-ablation.conll` for Case Ablation.
- `data-io-aberration.conll` for Case Aberration.
- `data-io-perturbation.conll` for Context Perturbation.
- `data-io-alteration.conll` for Context Alteration.

### Datasets

1. [CoNLL](https://github.com/glample/tagger/tree/master/dataset)
2. [Wiki](https://github.com/juand-r/entity-recognition-datasets/tree/master/data/wikigold)
3. [IEER](https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/ieer.zip)
4. [GMB](https://gmb.let.rug.nl/data.php)

## Citing

If you find this code useful, please cite [Resilience of Named Entity Recognition Models Under Adversarial Attack](https://aclanthology.org/2022.dadc-1.1/).

```
@inproceedings{das-paik-2022-resilience,
title = {Resilience of Named Entity Recognition Models under Adversarial Attack},
author = {Das, Sudeshna and Paik, Jiaul H},
booktitle = {Proceedings of the First Workshop on Dynamic Adversarial Data Collection},
month = {jul},
year = {2022},
address = {Seattle, WA},
publisher = {Association for Computational Linguistics},
url = {https://aclanthology.org/2022.dadc-1.1},
pages = {1--6},
}
```
