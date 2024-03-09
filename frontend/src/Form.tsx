import React from "react";

import formStyles from "./form.module.css";
import { useNavigate } from "react-router-dom";

export default function Form() {
  const [objects, setObjects] = React.useState([""]);

  const navigate = useNavigate();

  const addBox = () => {
    const newObjects = [...objects];
    newObjects.push("");
    setObjects(newObjects);
    setTimeout(() => (
      document
        .getElementById("inputBoxes")
        ?.lastChild as HTMLElement
    )?.focus()
    );
  }

  const submitForm: React.FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();
    const formData = new FormData(
      document.getElementById("form")! as HTMLFormElement
    );
    fetch("/submit-form", {
      method: "post",
      body: formData
    }).then(res => {
      if (!res.ok) {
        alert("an unexpected error was encountered")
        return
      }
      res.json().then(json => {
        if (json["success"]) {
          if (json["success"] === "generating style image...") {
            navigate("/evaluate-image");
          } else {
            navigate("/results");
          }
        } else {
          alert("err: " + JSON.stringify(json));
        }
      })
    });
  }

  return (
    <form
      onSubmit={submitForm}
      method="POST"
      encType="multipart/form-data"
      id="form"
    >
      <p>What objects would you like to generate models for?</p>
      <div className={formStyles.textBoxes} id="inputBoxes">
        {
          objects.map((object, i) =>
            <input
              placeholder={i === 0 ? "e.g. tree" : ""}
              required={i === 0}
              type="text"
              key={i}
              name={`object-${i}`}
              value={object}
              onChange={e => {
                const newObjects = [...objects];
                newObjects[i] = e.target.value;
                setObjects(newObjects);
              }}
            />
          )
        }
      </div>
      <button
        type="button"
        className={formStyles.addObject}
        onClick={e => {
          e.preventDefault();
          addBox();
        }}
      >+</button>

      <hr />

      <p>Style reference image (optional)</p>
      <div className={formStyles.imgInputWrapper} id="imgInputWrapper">
        <p className={formStyles.imgInputText}>
          Click here or drop to add image
        </p>
        <input
          type="file"
          id="style-image"
          className={formStyles.imgInput}
          accept="image/png, image/jpeg"
          name="style-image"
          onChange={e => {
            if (e.target.files) {
              const url = URL.createObjectURL(e.target.files[0]);
              const fr = new FileReader();
              fr.onload = function () {
                const img = new Image();
                img.onload = function () {
                  const imgInputWrapper = document
                    .getElementById("imgInputWrapper")!;
                  imgInputWrapper.style.aspectRatio =
                    `${img.width}/${img.height}`;
                  imgInputWrapper.style.backgroundImage = `url(${url})`;
                };
                img.src = fr.result as string;
              };
              fr.readAsDataURL(e.target.files[0]);
            }
          }}
        />
      </div>

      <button type="submit" className={formStyles.submitButton}>
        Let's do this
      </button>
    </form>
  )
}
