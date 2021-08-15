# face-recognition
This is a simple python project to detect known faces in real-time using a webcam and the face-recogintion library.

Compatible with both windows and linux.
Windows users should use Anaconda and create a new environment before proceeding. <br/>
If you dont know how to use Anaconda you may proceed with the default python installation.

## Dependencies
Make sure you have dlib installed with your python bindings. If not, try running <code>pip3 install dlib</code>. If dlib install fails, refer to <a href="https://github.com/ageitgey/face_recognition/issues/175#issue-257710508" target="_blank">this guide.</a>
To install the dependencies run the following commands in your command line/terminal:<br/>
<code>
pip3 install face_recognition
</code><br/>
<code>
pip3 install numpy
</code><br/>
<code>
pip install opencv-python
</code>

## Demo
For a quick demo clone/download the face-recognition.py file from this repository and put it in a folder with images of people to be recognised and name them accordingly. 
Also change the names and paths in the "KnownNames.txt" and "PathToImages.txt" file separated by "\n" respectively. Make sure to preserve the order while entering names.
i.e. If first line in KnownNames.txt is "Barack Obama" then first line in in PathToImages.txt should have the path to Barack Obama's image. <br/>
Once done, launch face-recognition.py from command line by using <br/>
<code>
python face-recognition.py
</code>
