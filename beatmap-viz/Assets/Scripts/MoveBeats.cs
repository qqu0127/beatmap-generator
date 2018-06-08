using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveBeats : MonoBehaviour {

	public float speed = 8.0f;

	// Use this for initialization
	void Start () {
		speed = 100.0f;
	}
	
	// Update is called once per frame
	void Update () {
		transform.Translate (-Vector2.right * speed * Time.deltaTime);
	}
}
