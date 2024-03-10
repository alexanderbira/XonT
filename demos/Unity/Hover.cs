using UnityEngine;
using UnityEngine.SceneManagement;

/* note to dev: add a mesh collider component where the mesh is set to the 3d object */

public class Hover : MonoBehaviour
{
    public float amplitude = 0.5f; // adjust this to change the height of the hover
    public float speed = 1.5f; // adjust this to change the speed of the hover
    private float startY;
    private bool isHovering = false;
    public string newScene; // adjust this to change what scene the object redirects to

    private void Start()
    {
        startY = transform.position.y;
    }

    private void Update()
    {
        if (isHovering)
        {
            // calculate the new Y position using a sine wave
            float newY = startY + amplitude * Mathf.Sin(Time.time * speed);
            // update the object's position only on the Y axis
            transform.position = new Vector3(transform.position.x, newY, transform.position.z);
        }
    }
    
    private void OnMouseOver()
    {
        isHovering = true;
    }

    private void OnMouseDown()
    {
        SceneManager.LoadScene(newScene);
    }

    private void OnMouseExit()
    {
        isHovering = false;
        // reset the object's Y position to the original height
        transform.position = new Vector3(transform.position.x, startY, transform.position.z);
    }
}
