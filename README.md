# ShapeWorld

### Getting started

```bash
git clone --recursive https://github.com/AlexKuhnle/ShapeWorld.git
pip3 install -e ShapeWorld  # optional: ShapeWorld[full] or ShapeWorld[full-gpu]
```


### Recently added features

- Support for Mac OS X (ACE, grammar)
- New agreement baseline models
- Generator option `-F` for extraction of image features (ResNet-101)
- Generator option `-C` for alternative CLEVR output format
- More complex quantification captions
- Abstract caption model as sequence in reverse Polish notation
- Improved sampling strategy for more balanced / less biased data
- Generator option `-H` to create an HTML file displaying the generated data (e.g. see in (examples))
- Various new and extended caption agreement datasets


### Table of content

- [About ShapeWorld](#about-shapeworld)
- [Example data](#example-data)
- [Integration into Python code](#integration-into-python-code)
- [Stand-alone data generation](#stand-alone-data-generation)
- [Loading extracted data](#loading-extracted-data)
- [CLEVR and NLVR interface](#clevr-and-nlvr-interface)
- [Evaluation and example models](#evaluation-and-example-models)



## About ShapeWorld

ShapeWorld is a framework which allows to specify generators for abstract, visually grounded language data (or just visual data).

The main motivation behind ShapeWorld is to provide a new testbed and evaluation methodology for visually grounded language understanding, particularly aimed at deep learning models. It differs from standard evaluation datasets in two ways: Firstly, data is randomly sampled during training and evaluation according to constraints specified by the experimenter. Secondly, its focus of evaluation is on linguistic understanding capabilities of the type investigated by formal semantics. In this context, the ShapeWorld tasks can be thought of as unit-testing multimodal models for specific linguistic generalization abilities -- similar to, for instance, the [bAbI tasks](https://research.fb.com/projects/babi/) of [Weston et al. (2015)](https://arxiv.org/abs/1502.05698) for text-only understanding.

The code is written in Python 3 (but should be compatible to Python 2). The data can either be obtained within a Python module as [NumPy](http://www.numpy.org/) arrays, and hence integrates into deep learning projects based on common frameworks like [TensorFlow](https://www.tensorflow.org/), [PyTorch](http://pytorch.org/) or [Theano](http://deeplearning.net/software/theano/), or it can be extracted into separate files. Both options are described further below. For language generation, the Python package [pydmrs](https://github.com/delph-in/pydmrs) [(Copestake et al., 2016)](http://www.lrec-conf.org/proceedings/lrec2016/pdf/634_Paper.pdf) is required.

**The ShapeWorld framework is still under active development.**

I am interested in hearing about any applications you plan to use the ShapeWorld data for. In particular, let me know if you have a great idea in mind that you are interested in investigating with such abstract data, but which the current setup does not allow to realize -- I am happy to collaboratively find a way to make it happen.

Contact: aok25 (at) cam.ac.uk

If you use ShapeWorld in your work, please cite:

> **ShapeWorld: A new test methodology for multimodal language understanding** ([arXiv](https://arxiv.org/abs/1704.04517)).
> *Alexander Kuhnle and Ann Copestake* (April 2017).



## Example data

#### Caption agreement datasets

- [Oneshape](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/agreement/oneshape/data.html)
- [Multishape](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/agreement/multishape/data.html)
- [Spatial](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/agreement/spatial/data.html)
- [Relational](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/agreement/relational/data.html)
- [Quantification (simple)](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/agreement/quantification_simple/data.html)
- [Quantification](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/agreement/quantification/data.html)
- [Quantification (complex)](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/agreement/quantification_complex/data.html)
- [Combination](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/agreement/combination/data.html)

#### Classification datasets

- [Oneshape](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/classification/oneshape/data.html)
- [Multishape](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/classification/multishape/data.html)
- [Countshape](https://rawgit.com/AlexKuhnle/ShapeWorld/master/examples/classification/countshape/data.html)



## Integration into Python code

The easiest way to use the ShapeWorld data in your Python project is to directly call it from the code. Whenever a batch of training/evaluation instances is required, `dataset.generate(...)` is called with the respective arguments. This means that generation happens simultaneously to training/testing. Below an example of how to generate a batch of 128 training instances. See also the example models below.

```python
from shapeworld import Dataset

dataset = Dataset.create(dtype='agreement', name='multishape')
generated = dataset.generate(n=128, mode='train', include_model=True)

print('world shape:', dataset.world_shape())
print('caption shape:', dataset.vector_shape(value_name='caption'))
print('vocabulary size:', dataset.vocabulary_size(value_type='language'))
print('vocabulary:', dataset.vocabulary)

# caption surface forms
print('captions:')
print('\n'.join(dataset.to_surface(value_type='language', word_ids=generated['caption'])))

# given to the image caption agreement model
batch = (generated['world'], generated['caption'], generated['caption_length'], generated['agreement'])

# can be used for more specific evaluation
world_model = generated['world_model']
caption_model = generated['caption_model']
```



## Stand-alone data generation

The `shapeworld/generate.py` module provides options to generate ShapeWorld data in separate files via the command line. Use cases include:

* for using the ShapeWorld data for deep learning projects based on other programming languages than Python,
* for quicker pre-evaluation of models in development stage -- however, it is one of the important principles of the ShapeWorld evaluation methodology and hence recommended to use newly generated data for the final evaluation phase,
* for manual investigation of the generated data,
* for entirely different applications like, e.g., a user study.

The following command line arguments are available:

* `-d`, `--directory`:  Directory for generated data, with automatically created sub-directories unless `--unmanaged`, hence should be non-existing or empty since it will be overwritten (**required**)
* `-a`, `--archive`:  Store generated data in (compressed) archives, either `zip[:mode]` or `tar[:mode]` with one of `none`, `deflate` (only zip), `gzip` (only tar), `bzip2`, `lzma` (default: `none`)
* `-U`, `--unmanaged`:  Do not automatically create sub-directories (implied if --shards not specified)
* `-t`, `--type`:  Dataset type (**required**)
* `-n`, `--name`:  Dataset name (**required**)
* `-l`, `--language`:  Dataset language, if available (default: `none`, i.e. English)
* `-c`, `--config`:  Dataset configuration file, otherwise use default configuration
* `-s`, `--shards`:  Optional number of shards to split data into (not specified implies --unmanaged), either a number (with `--mode`) or a tuple of 3 comma-separated numbers (without `--mode`), for `train`, `validation` and `test` data respectively
* `-i`, `--instances`:  Number of instances per shard (default: `128`)
* `-m`, `--mode`:  Mode, one of `train`, `validation` or `test`, requires `--shards` to be a single number (default: `none`)
* `-A`, `--append`:  Append to existing data (when used without `--unmanaged`)
* `-b`, `--begin`: Optional begin from shard number (requires `--append`), same format as `--shards`
* `-M`, `--include-model`:  Include world/caption model (as json file)
* `-H`, `--html`:  Create HTML file (`data.html`) visualizing the generated data
* `-T`, `--tf-records`:  Additionally store data as TensorFlow records
* `-F`, `--features`:  Additionally extract image features (`conv4` of `resnet_v2_101`)
* `-C`, `--clevr-format`:  Output in CLEVR format
* `-O`, `--concatenate-images`:  Concatenate images per part into one image file
* `-Y`, `--yes`:  Confirm all questions with yes
* `--config-values`:  Additional dataset configuration values passed as command line arguments

When creating larger amounts of ShapeWorld data, it is advisable to store the data in a compressed archive (for example `-a tar:bz2`). For instance, the following command line generates one million *training* instances of the `multishape` configuration file included in this repository:

```bash
python generate.py -d [DIRECTORY] -a tar:bzip2 -t agreement -n multishape -m train -f 100 -i 10k -M
```

For the purpose of this introduction, we generate a smaller amount of *all* training (TensorFlow records and raw), validation and test instances using the default configuration of the dataset:

```bash
python generate.py -d examples/readme -a tar:bzip2 -t agreement -n multishape -f 3,2,1 -i 128 -M -T
```



## Loading extracted data

Extracted data can be loaded and accessed with the same `Dataset` interface as before, just define the `config` argument as `[DIRECTORY]`. However, to be able to do this, we need to extract all of training, validation and test data, as is done in the last command line.

```python
from shapeworld import Dataset

dataset = Dataset.create(dtype='agreement', name='multishape', config='examples/readme')
generated = dataset.generate(n=128, mode='train')
```

Loading the data in Python and then feeding it to a model is relatively slow. By using TensorFlow (TF) records (see above for how to generate TF records) and consequently the ability to load data implicitly within TensorFlow, models can be trained significantly faster. ShapeWorld provides utilities to access TF records as generated/loaded data would be handled:

```python
from shapeworld import Dataset, tf_util

dataset = Dataset.create(dtype='agreement', name='multishape', config='examples/readme')
generated = tf_util.batch_records(dataset=dataset, mode='train', batch_size=128)
```

The `generated` Tensor cannot be immediately evaluated as it requires the Tensorflow graph to start shard reading queues. Basic data reading can be performed as:

```python
with tf.Session() as session:
	coordinator = tf.train.Coordinator()
	queue_threads = tf.train.start_queue_runners(sess=session, coord=coordinator)
	batch = session.run(generated)
	coordinator.request_stop()
	coordinator.join(threads=queue_threads)
```

## CLEVR and NLVR interface

CLEVR can be obtained as follows (alternatively, replace `CLEVR_v1.0` with `CLEVR_CoGenT_v1.0` for the CLEVR CoGenT dataset):

```bash
wget https://s3-us-west-1.amazonaws.com/clevr/CLEVR_v1.0.zip
unzip CLEVR_v1.0.zip
rm CLEVR_v1.0.zip
```

ShapeWorld then provides a basic interface to load the CLEVR instances **in order of their appearance** in the dataset. It is hence recommended to *'pre-generate'* the entire dataset (70k training, 15k validation and 15k test instances) once through the ShapeWorld interface, either as `clevr_classification` or `clevr_answering` dataset type, and subsequently access it as you would load other pre-generated ShapeWorld datasets:

```bash
python generate.py -d [SHAPEWORLD_DIRECTORY] -a tar:bzip2 -t clevr_classification -n clevr -f 140,30,30 -i 500 -M -T --config-values --directory CLEVR_v1.0
rm -r CLEVR_v1.0
```

Accordingly, in the case of CLEVR CoGenT:

```bash
python generate.py -d [SHAPEWORLD_DIRECTORY] -a tar:bzip2 -t clevr_classification -n clevr -f 140,30,30 -i 500 -M -T --config-values --directory CLEVR_CoGenT_v1.0 --parts A,A,A
python generate.py -d [SHAPEWORLD_DIRECTORY] -a tar:bzip2 -t clevr_classification -n clevr -f 0,30,30 -i 500 -M -T --config-values --directory CLEVR_CoGenT_v1.0 --parts A,B,B
rm -r CLEVR_CoGenT_v1.0
```

As `clevr_classification` dataset, it provides:
- a `'world'` and optional `'world_model'` value,
- an integer `'alternatives'` value which gives the number of questions per image (usually 10),
- a `'question'`, `'question_length'` and optional `'question_model'` value array/list containing the respective number of actual question values,
- an `'answer'` integer array specifying the corresponding answers.

As `clevr_answering` dataset, the last value is replaced by:
- an `'answer'` and `'answer_length'` value array containing the corresponding answer values.

Equivalently, NLVR can be obtained via:

```bash
git clone https://github.com/cornell-lic/nlvr.git
```

Again, one should *'pre-generate'* the entire dataset (75k training, 6k validation and 6k test instances) as `nlvr_agreement` dataset type, and subsequently access it via the ShapeWorld load interface:

```bash
python generate.py -d [SHAPEWORLD_DIRECTORY] -a tar:bzip2 -t nlvr_agreement -n nlvr -f 25,2,2 -i 3k -M -T --config-values --directory nlvr
rm -r nlvr
```

The dataset provides:
- `'world1'`, `'world2'`, `'world3'` and optional `'world_model1'`, `'world_model2'`, `'world_model3'` values,
- a `'description'`, `'description_length'` and optional `'description_model'` values,
- an `'agreement'` value.



## Evaluation and example models

The `models/` directory contains a few exemplary models based on [TFMacros](https://github.com/AlexKuhnle/TFMacros), my collection of TensorFlow macros. The scripts `train.py` and `evaluate.py` provide the following command line arguments to train and evaluate these models ((t) train-only, (e) evaluate-only):

* `-t`, `--type`:  Dataset type (**required**)
* `-n`, `--name`:  Dataset name (**required**)
* `-l`, `--language`:  Dataset language, if available (default: `none`, i.e. English)
* `-c`, `--config`:  Dataset configuration file, otherwise use default configuration
* `-m`, `--model`:  Model, one in `models/[TYPE]/` (**required**)
* `-y`, `--hyperparams-file`:  Model hyperparameters file (default: hyperparams directory)
* `-R`, `--restore` (t):  Restore model, requires `--model-file`
* `-b`, `--batch-size`:  Batch size (default: `64`)
* `-i`, `--iterations`:  Number of iterations (default: `1000`)
* `-e`, `--evaluation-iterations` (t):  Evaluation iterations (default: `10`) (*)
* `-f`, `--evaluation-frequency` (t):  Evaluation frequency (default: `100`) (*)
* `-q`, `--query`:  Additional values to query, separated by commas (default: `none`)
* `-s`, `--serialize` (e):  Values to serialize, separated by commas (default: `none`) (**)
* `-T`, `--tf-records` (t):  Use TensorFlow records (*)
* `--model-dir`:  TensorFlow model directory, storing the model computation graph and parameters (default: `none`)
* `--save-frequency` (t):  Save frequency, in hours (default: `3`)
* `--summary-dir` (t):  TensorFlow summary directory for TensorBoard (default: `none`)
* `--report-file`:  CSV file reporting the training results throughout the learning process (default: `none`)
* `-v`, `--verbosity'`:  Verbosity, one of `0` (no messages), `1` (default), `2` (plus TensorFlow messages) (default: `1`)
* `-Y`, `--yes` (t):  Confirm all questions with yes
* `--config-values`:  Additional dataset configuration values passed as command line arguments

For instance, the following command line trains an image caption agreement system on the dataset specified by the `multishape` configuration file included in this repository:

```bash
python train.py -t agreement -n multishape -m cnn_bow -i 5k
```

The previously generated data (here: TF records) can be loaded in the same way as was explained for loading the data in Python code:

```bash
python train.py -t agreement -n multishape -c examples/readme -m cnn_bow -i 10 -T
```




```bash
python evaluate.py -t agreement -n multishape -c examples/readme -m cnn_bow -i 10
```
