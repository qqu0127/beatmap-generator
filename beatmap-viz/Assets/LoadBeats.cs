using UnityEngine;
using UnityEditor;
using System.Collections;
using System.IO;
using System.Collections.Generic;

public class LoadBeats : MonoBehaviour
{

	public BeatsData gameData;

	private string gameDataProjectFilePath = "/BeatAssets/beat_map.json";

//	[MenuItem ("Window/Game Data Editor")]
//	static void Init()
//	{
//		EditorWindow.GetWindow (typeof(GameDataEditor)).Show ();
//	}
//
//	void OnGUI()
//	{
//		if (gameData != null) 
//		{
//			SerializedObject serializedObject = new SerializedObject (this);
//			SerializedProperty serializedProperty = serializedObject.FindProperty ("gameData");
//			EditorGUILayout.PropertyField (serializedProperty, true);
//
//			serializedObject.ApplyModifiedProperties ();
//
//			if (GUILayout.Button ("Save data"))
//			{
//				SaveGameData();
//			}
//		}
//
//		if (GUILayout.Button ("Load data"))
//		{
//			LoadGameData();
//		}
//	}


	void Start () {
		LoadGameData();
//		Debug.Log(gameData.num_track);
//		Debug.Log(gameData.beat_cnt);
//		Debug.Log(gameData.mapped);
		instantiateBeats();
	}

	void instantiateBeats () {

		int x = 0;
		int initial_distance = 20;

		for (int p = 0; p < gameData.length; p++) {
//			for (int q = 0; q < gameData.num_track; q++) {
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
//			}
			x += 1;
		}
		Debug.Log(x);


//		for (int y = 0; y < 4; y++) {
//
//			if (y == 0) {
//				for (int x = 0; x < 5; x++) {
//					Instantiate (Resources.Load("BeatOne"), new Vector3 (x+25, 1, 3), Quaternion.identity);
//				}
//			} 
//			else if (y == 1) {
//				for (int x = 0; x < 5; x++) {
//					Instantiate (Resources.Load("BeatTwo"), new Vector3 (x+25, 1, 1), Quaternion.identity);
//				}
//			} 
//			else if (y == 2) {
//				for (int x = 0; x < 5; x++) {
//					Instantiate (Resources.Load("BeatThree"), new Vector3 (x+25, 1, -1), Quaternion.identity);
//				}
//			} 
//			else if (y == 3) {
//				for (int x = 0; x < 5; x++) {
//					Instantiate (Resources.Load("BeatFour"), new Vector3 (x+25, 1, -3), Quaternion.identity);
//				}
//			}
//		}
	}

	private void LoadGameData()
	{
		string filePath = Application.dataPath + gameDataProjectFilePath;

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
//	public List<string> mapped;

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
//	public List<int> stamp;
//	public string[] t;
}