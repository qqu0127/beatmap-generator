using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveBeats : MonoBehaviour {

	public float speed = 8.0f;
	public string tag = "name";

	// Use this for initialization
	void Start () {
		speed = 60.0f;
//		transform.Translate (Vector2.right * speed * Time.deltaTime);
	}
	
	// Update is called once per frame
	void Update () {
		transform.Translate (-Vector2.right * speed * Time.deltaTime);
	}
}
