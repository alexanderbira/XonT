import React from "react";

import formStyles from "./form.module.css";

export default function Form() {
  const [objects, setObjects] = React.useState([""]);

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

  return (
    <form
      action="submit-form"
      method="POST"
      encType="multipart/form-data"
    >
      <p>What objects would you like to generate models for?</p>
      <div className={formStyles.textBoxes} id="inputBoxes">
        {
          objects.map((object, i) =>
            <input
              type="text"
              key={i}
              name={`object-${i}`}
              value={object}
              onChange={e => {
                const newObjects = [...objects];
                newObjects[i] = e.target.value;
                setObjects(newObjects);
              }}
              onKeyDownCapture={e => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  addBox();
                }
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
