using UnityEngine;
using UnityEditor;
using System.Collections;
using System.IO;
using System.Collections.Generic;

public class LoadBeats : MonoBehaviour
{

	public BeatsData gameData;
	public AudioSource music;
	public string auidoFileName;
	public string jsonFileName;

	public AudioSource[] allMyAudioSources;
	private string gameDataProjectFilePath = "/BeatAssets/";

	[MenuItem ("Window/Game Data Editor")]
	static void Init()
	{
		EditorWindow.GetWindow (typeof(LoadBeats)).Show ();
	}

	void OnGUI()
	{
		if (GUILayout.Button ("Load data"))
		{
			LoadGameData();
			instantiateBeats();
			AudioClip audioToPlay = Resources.Load<AudioClip>("AudioAssets/" + auidoFileName);
			Debug.Log (auidoFileName);
			Debug.Log (jsonFileName);
			music = allMyAudioSources[0];
			music.clip = audioToPlay;
			music.PlayDelayed(1);
		}
	}


	void Start () {
		allMyAudioSources = GetComponents<AudioSource>();
	}

	public void getJsonInput(string intputJson) {
		jsonFileName = intputJson;
	}

	public void getAudioInput(string inputAudio) {
		auidoFileName = inputAudio;
	}

	void instantiateBeats () {

		int x = 1;
		int initial_distance = 100;

		for (int p = 0; p < gameData.length; p++) {
			if (gameData.mapped[p].a == 1) {
				Instantiate (Resources.Load("BeatOne"), new Vector3 (x+initial_distance, 1, 3), Quaternion.identity);
			} 
			if (gameData.mapped[p].b == 1) {
				Instantiate (Resources.Load("BeatTwo"), new Vector3 (x+initial_distance, 1, 1), Quaternion.identity);
			} 
			if (gameData.mapped[p].c == 1) {
				Instantiate (Resources.Load("BeatThree"), new Vector3 (x+initial_distance, 1, -1), Quaternion.identity);
			} 
			if (gameData.mapped[p].d == 1) {
				Instantiate (Resources.Load("BeatFour"), new Vector3 (x+initial_distance, 1, -3), Quaternion.identity);
			}
			if (gameData.num_track == 5 && gameData.mapped[p].e == 1) {
				Instantiate (Resources.Load("BeatFive"), new Vector3 (x+initial_distance, 1, -5), Quaternion.identity);
			}
			if (gameData.num_track == 6 && gameData.mapped[p].f == 1) {
				Instantiate (Resources.Load("BeatSix"), new Vector3 (x+initial_distance, 1, -7), Quaternion.identity);
			}
			x += 1;
		}
		Debug.Log(x);
	}
		
	private void LoadGameData()
	{
		string filePath = Application.dataPath + gameDataProjectFilePath + jsonFileName + ".json";

		if (File.Exists (filePath)) {
			string dataAsJson = File.ReadAllText (filePath);
			gameData = JsonUtility.FromJson<BeatsData> (dataAsJson);
		} else 
		{
			gameData = new BeatsData();
		}
	}

	private void SaveGameData()
	{

		string dataAsJson = JsonUtility.ToJson (gameData);
		string filePath = Application.dataPath + gameDataProjectFilePath;
		File.WriteAllText (filePath, dataAsJson);

	}
}


[System.Serializable]
public class BeatsData
{
	public int num_track;
	public float time_interval;

	public int beat_cnt;
	public int length;
	public List<timestamp> mapped;
}


[System.Serializable]
public class timestamp
{
	public int a;
	public int b;
	public int c;
	public int d;
	public int e;
	public int f;
}