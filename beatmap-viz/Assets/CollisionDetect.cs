using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CollisionDetect : MonoBehaviour {

	AudioSource kickSource;
	AudioSource snareSource;
	AudioSource closehatSource;
	AudioSource openhatSource;
	AudioSource music;

	void Start() {
		AudioSource[] allMyAudioSources = GetComponents<AudioSource>();
//		kickSource = allMyAudioSources[0];
//		snareSource = allMyAudioSources[1];
//		closehatSource = allMyAudioSources[2];
//		openhatSource = allMyAudioSources[3];
		music = allMyAudioSources[4];
		music.Play ();

	}

	void OnCollisionEnter (Collision col)
	{
//		if(col.gameObject.name == "beat")
//		{
//		if (col.gameObject.transform.position.z == -3) {
//			kickSource.Play();
//		} 
//		if (col.gameObject.transform.position.z == -1) {
//			snareSource.Play();
//		} 
//		if (col.gameObject.transform.position.z == 1) {
//			closehatSource.Play();
//		} 
//		if (col.gameObject.transform.position.z == 3) {
//			openhatSource.Play();
//		} 
//		kickSource.Play();
//		snareSource.Play();
//		closehatSource.Play();
//		openhatSource.Play();
		Destroy(col.gameObject);
//		}
	}

}
