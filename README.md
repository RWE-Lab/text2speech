# Text to Speech

Google Text2Speech is a Google AI product to converts text into human-like speech. We implemented this application and provided an interactive interface for researchers to quickly start and deploy this AI function.

**Usages**
```python
$ python text2speech.py
```
Check our demo:

# Set up

1. Clone text2speech and change directory to the sample directory you want to use.
```
git clone https://github.com/RWE-Lab/text2speech.git
```

2. Create a virtualenv or use [Anaconda](https://www.anaconda.com) to create an environment 
```
$ virtualenv your_env
$ source your_env/bin/activate
```

3. Please follow the steps to [set up your Google Cloud Platform project and authorization](https://cloud.google.com/text-to-speech/).

4. Install the dependencies needed to run the samples.
```
pip install --upgrade google-cloud-texttospeech
```





