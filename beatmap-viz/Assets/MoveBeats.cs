using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveBeats : MonoBehaviour {

	public float speed = 4.0f;

	// Use this for initialization
	void Start () {
//		transform.Translate (Vector2.right * speed * Time.deltaTime);
	}
	
	// Update is called once per frame
	void Update () {
		transform.Translate (-Vector2.right * speed * Time.deltaTime);
	}
}
