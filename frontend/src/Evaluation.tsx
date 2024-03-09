import React from "react";

import evaluationStyles from "./evaluation.module.css";

import { Socket } from 'socket.io-client';

import { useNavigate } from "react-router-dom";

interface EvaluationProps {
  socket: Socket;
}

export default function Evaluation({ socket }: EvaluationProps) {
  const [loaded, setLoaded] = React.useState(false);

  const navigate = useNavigate();

  socket.on("evaluate_image", () => setLoaded(true));

  const acceptImage = () => {
    navigate("/results");
  }

  const rejectImage = () => {
    const extraPrompt = (
      document.getElementById("extraPrompt")! as HTMLTextAreaElement
    ).value;
    fetch("/reject-image",
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({ prompt: extraPrompt })
      }).then(() => setLoaded(false))
  }

  return (
    <div>
      {
        loaded ?
          <div>
            <h1>Image Style Check</h1>
            <img
              src={`/evaluate-img.png?${new Date().getTime()}`}
              alt="sample style reference"
              className={evaluationStyles.refImage}
            />
            <p className={evaluationStyles.question}>
              Is this an acceptable style for your project?
            </p>
            <div className={evaluationStyles.judgeButtons}>
              <button onClick={acceptImage}>Yes</button>
              <button onClick={rejectImage}>No</button>
            </div>
            <p>
              (If <u>no</u>, you can optionally specify what you want 
              the image to look like):
            </p>
            <textarea
              id="extraPrompt"
              className={evaluationStyles.extraPrompt}
              placeholder="comma-separated descriptive words"
              rows={4}
            ></textarea>
          </div>
          :
          <p>Please wait while we generate an image for you to evaluate...</p>
      }
    </div>
  );
}
