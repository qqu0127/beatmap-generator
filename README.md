# Beatmap Generator and Visualization System
Automatic beatmap generator and visualization tools for rhythm games.  

## Getting Started

### Prerequisites
Please refer to dockerfile for environment setup.  
#### System dependencies:  
* python 3.6.3  
* cycler 0.10.0  
* Cython 0.28.2  
* kiwisolver 1.0.1  
* madmom 0.15.1  
* matplotlib 2.2.2  
* nose 1.3.7  
* numpy 1.14.3  
* PyAudio 0.2.11  
* pyparsing 2.2.0  
* python-dateutil 2.7.2  
* pytz 2018.4  
* scikit-learn 0.19.1  
* six 1.11.0  
* scipy 1.0.1  
* Unity3D 2017.3.1f1 Personal  

### Running the Program
* A quick start  
'''
python beat_map_generate.py --input='../data/beat_it.mp3'
'''
This will generate the beatmap in current folder named "beat_map.json"  
You can also specify more arguments for advanced setting, refer to full usage as following.  
'''
python beat_map_generate.py
	--input=[AUDIO_PATH]
	--num_tracks=[NUM_TRACKS]
	--output=[OUTPUT_PATH]
	--method=[DETECTION_METHOD]
	--free_beat_range=[FREE_BEAT_RANGE]
'''
* Visualization tool  

TBD  

## Contribution
TBD  

## License
TBD  





