import React from "react";

import { Socket } from 'socket.io-client';

import resultsStyles from "./results.module.css";

interface ResultsProps {
  socket: Socket;
}

export default function Results({ socket }: ResultsProps) {
  const [resultNames, setResultNames] = React.useState<String[]>([]);
  const [allLoaded, setAllLoaded] = React.useState(false);

  React.useEffect(() => {
    socket.on("next_completed", ({ object }) => {
      setResultNames(currNames => [...currNames, object]);
      socket.emit("create_results");
    });

    socket.on("all_completed", () => setAllLoaded(true));

    socket.emit("create_results");
  }, []);

  return (
    <div>
      {
        !allLoaded && <p>Generating image {resultNames.length + 1}...</p>
      }
      <div className={resultsStyles.imageContainer}>
        {
          resultNames.map((name, i) =>
            <img
              src={`/result-${name}.png`}
              key={i}
              className={resultsStyles.resultImage}
            />
          )
        }
      </div>
    </div>
  );
}
